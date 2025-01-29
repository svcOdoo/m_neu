# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockPicking(models.Model):
    _inherit = "stock.picking"

    axx_pack_pid = fields.Char(
        string="Current PID",
        copy=False,
    )
    axx_package_type_id = fields.Many2one(
        comodel_name="stock.package.type",
        string="Package type",
    )
    # axx_wa_bahn_was_shown = fields.Boolean(
    #     string='Drive to WA-Bahn',
    #     help='Technical field to make sure that the wizard has been displayed',
    #     copy=False
    # )

    def axx_get_action_picking_tree_ready_kanban(self):
        action = self.picking_type_id._get_action('stock_barcode.stock_picking_action_kanban')
        return action

    def _axx_pack_pid_wizard_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("axx_picking_commission_workflow.action_add_pack_pid_wizard")
        action['res_id'] = self.id
        return action

    def action_open_picking_client_action(self):
        """
        adjustment to overwrite the behavior when clicking the name of a picking in the kanban view:
        we always want to execute the custom onGlobalClick from our javascript adjustment
        :return:
        """
        if not self.env.context.get('axx_force_client_action') and self.get_need_pack_action_ignore_pid():
            return False
        action = super(StockPicking, self).action_open_picking_client_action()
        return action

    def action_open_picking_pid_action(self):
        if not self.axx_pack_pid and not self.env.context.get('save_and_close'):
            return self._axx_pack_pid_wizard_action()
        return self.with_context(axx_force_client_action=True).action_open_picking_client_action()

    def get_need_pack_action(self):
        if all(move_line_id.result_package_id for move_line_id in self.move_line_ids) or self.axx_pack_pid or\
                self.picking_type_code not in ['internal']:
            return False
        return True

    def get_need_pack_action_ignore_pid(self):
        if all(move_line_id.result_package_id for move_line_id in self.move_line_ids) or \
                self.picking_type_code not in ['internal']:
            return False
        return True

    def action_confirm_packaging(self):
        if self.env.context.get('open_record'):
            return self.action_open_picking_pid_action()
        return False

    def axx_find_open_backorder(self):
        backorder = self.search(
            [('backorder_id', '=', self.id), ('state', 'not in', ['done', 'cancel'])], limit=1)
        return backorder.id if backorder else 0

    def action_get_backorder(self):
        backorder_id = self.search([('backorder_id', '=', self.id)], limit=1)
        if backorder_id:
            backorder_id.write({
                'axx_package_type_id': self.axx_package_type_id,
            })
            action = backorder_id.with_context(save_and_close=True, axx_force_client_action=True).action_open_picking_client_action()
            return action
        return False

    def _put_in_pack(self, move_line_ids, create_package_level=True):
        # RECEIPTS ###
        if self[0].picking_type_code == 'incoming':
            package = super(StockPicking, self)._put_in_pack(move_line_ids, create_package_level)
            if len(self) == 1 and self[0].picking_type_code == 'incoming':
                pid_receipt = move_line_ids[0].axx_reference
                if pid_receipt:
                    package.write({'name': pid_receipt})
            return package

        # OTHER ###
        if not self.env.context.get('save_and_close') and self.get_need_pack_action():
            return self.action_open_picking_pid_action()
        if not self.axx_pack_pid and self.env.context.get('barcode_view'):
            raise ValidationError(_("Bitte zuerst PID eingeben!"))
        # if self.axx_pack_pid:
        #     self.action_confirm_packaging()
        package = False
        for pick in self:
            move_lines_to_pack = self.env['stock.move.line']
            package = self.env['stock.quant.package'].create({
                'name': self.axx_pack_pid,
                'package_type_id': self.axx_package_type_id.id if self.axx_package_type_id else False
            })
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            if float_is_zero(move_line_ids[0].qty_done, precision_digits=precision_digits):
                for line in move_line_ids:
                    line.qty_done = line.reserved_uom_qty

            for ml in move_line_ids:
                if float_compare(ml.qty_done, ml.reserved_uom_qty,
                                 precision_rounding=ml.product_uom_id.rounding) >= 0:
                    move_lines_to_pack |= ml
                else:
                    quantity_left_todo = float_round(
                        ml.reserved_uom_qty - ml.qty_done,
                        precision_rounding=ml.product_uom_id.rounding,
                        rounding_method='HALF-UP')
                    done_to_keep = ml.qty_done
                    new_move_line = ml.copy(
                        default={'reserved_uom_qty': 0, 'qty_done': ml.qty_done})
                    vals = {'reserved_uom_qty': quantity_left_todo, 'qty_done': 0.0}
                    if pick.picking_type_id.code == 'incoming':
                        if ml.lot_id:
                            vals['lot_id'] = False
                        if ml.lot_name:
                            vals['lot_name'] = False
                    ml.write(vals)
                    new_move_line.write({'reserved_uom_qty': done_to_keep})
                    move_lines_to_pack |= new_move_line
            if not package.package_type_id:
                package_type = move_lines_to_pack.move_id.product_packaging_id.package_type_id
                if len(package_type) == 1:
                    package.package_type_id = package_type
            if len(move_lines_to_pack) == 1:
                default_dest_location = move_lines_to_pack._get_default_dest_location()
                move_lines_to_pack.location_dest_id = default_dest_location._get_putaway_strategy(
                    product=move_lines_to_pack.product_id,
                    quantity=move_lines_to_pack.reserved_uom_qty,
                    package=package)
            move_lines_to_pack.write({
                'result_package_id': package.id,
            })
            if create_package_level:
                package_level = self.env['stock.package_level'].create({
                    'package_id': package.id,
                    'picking_id': pick.id,
                    'location_id': False,
                    'location_dest_id': move_lines_to_pack.mapped('location_dest_id').id,
                    'move_line_ids': [(6, 0, move_lines_to_pack.ids)],
                    'company_id': pick.company_id.id,
                })
            # empty the current package
            pick.write({
                    'axx_pack_pid': '',
            })
        if not self.env.context.get('save_and_close') and self.get_need_pack_action():
            action = self.action_open_picking_pid_action()
            action['context'] = {'save_and_close': True}
            return action
        return package

    def _get_fields_stock_barcode(self):
        fields_list = super(StockPicking, self)._get_fields_stock_barcode()
        fields_list.append('axx_pack_pid')
        return fields_list
