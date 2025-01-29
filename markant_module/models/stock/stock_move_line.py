from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    axx_show_put_in_pack = fields.Boolean("Show Put in pack", default=False, compute='_compute_show_put_in_pack')
    axx_target_location_barcode = fields.Char(
        string="Target Location Barcode"
    )
    target_location_id = fields.Many2one(
        'stock.location',
        string='Target Location',
        domain=[('usage', '=', 'internal')],
        required=False
    )
    axx_is_already_rebooked = fields.Boolean(
        string="Already Rebooked?",
        readonly=True
    )

    @api.onchange("axx_target_location_barcode")
    def onchange_axx_target_location_barcode(self):
        if self.axx_target_location_barcode:
            location = self.env['stock.location'].search([
                ('usage', '=', 'internal'),
                ('barcode', '=', self.axx_target_location_barcode)
            ], limit=1)
            self.target_location_id = location and location.id or False
        else:
            self.target_location_id = False

    # def action_use_dummy_lot_and_reload(self):
    #     self.ensure_one()
    #     self.picking_id.action_use_dummy_lot()
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }
    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        if self.axx_check_use_dummy_lot():
            if not self.lot_name and 'axx_reference' in vals and vals['axx_reference'] and 'lot_name' not in vals:
                self.axx_assign_dummy_lot()
        return res

    def axx_check_use_dummy_lot(self):
        if not self or len(self) > 1:
            return False
        use_dummy_lots = False
        if self.picking_id.picking_type_code == 'incoming' and self.product_id.tracking == 'lot' and not self.lot_name:
            use_dummy_lots = True
        return use_dummy_lots

    def axx_assign_dummy_lot(self):
        self.ensure_one()
        ir_seq_env = self.env['ir.sequence']
        if self.product_id.tracking == 'lot' and not self.lot_name:
            self.write({'lot_name': ir_seq_env.next_by_code('dummy.lots')})

        return True

    def axx_put_in_pack(self):
        self.ensure_one()
        if self.axx_check_use_dummy_lot():
            self.axx_assign_dummy_lot()
        return self.picking_id.action_put_in_pack()

    def _compute_show_put_in_pack(self):
        for rec in self:
            if len(rec.picking_id.move_ids) > 1 or rec.picking_code != 'incoming':
                rec.axx_show_put_in_pack = False
            elif not rec.result_package_id:
                rec.axx_show_put_in_pack = True
            else:
                rec.axx_show_put_in_pack = False

    def _get_fields_stock_barcode(self):
        return super()._get_fields_stock_barcode() + ['axx_reference', 'axx_standard_location_name']

    def _axx_create_new_move(self):
        """
        Create and confirm a new stock move line and validate the associated picking.

        This method creates a new internal transfer picking, creates a new stock move line with
        the same product, package, lot, and quantity as the original move line, and validates
        the new picking. It also sets the 'axx_reference' field of the original move line to 'verbucht'.
        :return (stock.move.line): The new stock move line created.
        """
        self.ensure_one()

        picking_env = self.env['stock.picking']
        stock_move_line_env = self.env['stock.move.line']

        # Create a new internal transfer picking
        picking_type = self.env.ref('stock.picking_type_internal')
        new_picking = picking_env.create({
            'partner_id': self.picking_partner_id and self.picking_partner_id.id or False,
            'picking_type_id': picking_type.id,
            'location_id': self.location_dest_id.id,
            'location_dest_id': self.target_location_id.id,
        })

        is_done = self.state == 'done'

        line_dict = {
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'qty_done': self.qty_done,
            'package_id': self.result_package_id and self.result_package_id.id or False,
            'result_package_id': self.result_package_id and self.result_package_id.id or False,
            'location_id': self.location_dest_id.id,
            'location_dest_id': self.target_location_id.id,
            'axx_reference': self.axx_reference,
            'picking_id': new_picking.id
        }
        if is_done:
            line_dict['lot_id'] = self.lot_id and self.lot_id.id or False
        else:
            line_dict['lot_name'] = self.lot_name

        new_move_line = stock_move_line_env.create(line_dict)
        new_picking.action_confirm()
        new_picking.with_context(skip_expired=True, bypass_entire_pack=True).button_validate()

        self.write({'axx_reference': 'verbucht'})

        return new_move_line

    def action_create_move(self):
        self.ensure_one()
        if self.axx_is_already_rebooked:
            raise UserError(_('Already rebooked!'))

        new_move = self._axx_create_new_move()
        self.write({
            'axx_is_already_rebooked': True
        })

        moves_history_action = self.sudo().env.ref('markant_module.stock_move_line_action_pid_in')
        return {
            'type': moves_history_action.type,
            'name': moves_history_action.name,
            'res_model': moves_history_action.res_model,
            'view_mode': moves_history_action.view_mode,
            'target': moves_history_action.target,
            'context': moves_history_action.context,
            'views': moves_history_action.views,
        }

    def action_cancel_create_move(self):
        self.ensure_one()
        if self.axx_is_already_rebooked:
            raise UserError(_('Already rebooked!'))
        self.write({
            'axx_target_location_barcode': '',
            'target_location_id': False,
        })
        moves_history_action = self.sudo().env.ref('markant_module.stock_move_line_action_pid_in')
        return {
            'type': moves_history_action.type,
            'name': moves_history_action.name,
            'res_model': moves_history_action.res_model,
            'view_mode': moves_history_action.view_mode,
            'target': moves_history_action.target,
            'context': moves_history_action.context,
            'views': moves_history_action.views,
        }

    def _axx_identifier(self):
        return f"{self.product_id.id}-{self.lot_id}-{self.reserved_uom_qty}"

    def axx_zubuchen(self):
        """
        move the product from the original source location to the standard location of the product
        """
        self.ensure_one()
        stock_move_line_env = self.env['stock.move.line']
        picking_env = self.env['stock.picking']
        quant_env = self.env['stock.quant']

        source_location = self.location_id
        standard_location = self.axx_standard_location_id
        product = self.product_id
        if not standard_location:
            raise ValidationError("Standard-Lagerplatz fehlt im Produkt! %s" % product.name)
        if source_location == standard_location:
            raise ValidationError("Bestand bereits auf Standard-Lagerplatz!")

        # Create a new internal transfer picking
        picking_type = self.env.ref('stock.picking_type_internal')
        new_picking = picking_env.create({
            'picking_type_id': picking_type.id,
            'location_id': source_location.id,
            'location_dest_id': standard_location.id,
        })

        source_quants = quant_env.search([
            ('location_id', '=', source_location.id),
            ('product_id', '=', product.id),
            ("quantity", ">", 0.0),
        ])
        other_moves = stock_move_line_env.search([
            ('state', '=', 'assigned'),
            ('product_id', '=', product.id),
            ('location_id', '=', source_location.id),
        ])
        other_moves = other_moves - self
        qty_done_map = {}

        for move in other_moves:
            qty_done_map[move._axx_identifier()] = move.qty_done
        other_pickings = other_moves.mapped("picking_id")
        for quant in source_quants:
            stock_move_line_env.create(
                {
                    'product_id': product.id,
                    'product_uom_id': self.product_uom_id.id,
                    'qty_done': quant.quantity,
                    'lot_id': quant.lot_id and quant.lot_id.id or False,
                    'package_id': quant.package_id and quant.package_id.id or False,
                    'result_package_id': False,
                    'location_id': source_location.id,
                    'location_dest_id': standard_location.id,
                    'picking_id': new_picking.id
                }
            )

        # update self to make sure the originator move will actually take stock from our standard location
        self.write({'location_id': standard_location.id})
        move = self.move_id

        new_picking.action_confirm()
        new_picking.with_context(skip_expired=True).button_validate()

        move._merge_moves()
        move.picking_id.action_assign()
        move_lines_to_delete = move.move_line_ids.filtered(lambda ml: not ml.reserved_uom_qty and not ml.qty_done)
        move_lines_to_delete.sudo().unlink()

        # other pickings will lose the reservation, need to assign again
        for picking in other_pickings:
            picking.action_assign()
        # workaround
        # the qty done will be set to reserved qty if we don't do this, not sure why this is needed, but it is...
        other_moves_reloaded = stock_move_line_env.search([
            ('state', '=', 'assigned'),
            ('product_id', '=', product.id),
            ('location_id', '=', standard_location.id),
        ])
        other_moves_reloaded = other_moves_reloaded - self
        for move in other_moves_reloaded:
            identifier = move._axx_identifier()
            if identifier in qty_done_map.keys():
                move.write({'qty_done': qty_done_map[identifier]})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
