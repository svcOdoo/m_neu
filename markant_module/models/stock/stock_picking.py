from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_next_backorder_name(self, picking_name):
        """ Compute the next backorder name based on the provided picking name. """
        name_parts = picking_name.rsplit('-', 1)

        # Determine the base name
        if len(name_parts) == 1 or not name_parts[1].isdigit():
            base_name = picking_name
        else:
            base_name = name_parts[0]

        # Find the highest suffix for this base name
        pickings_with_suffix = self.env['stock.picking'].search(
            [('name', 'like', f"{base_name}-%")],
            order='name desc',
            limit=1
        )
        if pickings_with_suffix:
            last_suffix = pickings_with_suffix.name.rsplit('-', 1)[1]
            if last_suffix.isdigit():
                next_suffix = int(last_suffix) + 1
            else:
                next_suffix = 1
        else:
            next_suffix = 1

        return f"{base_name}-{next_suffix}"

    def _create_backorder(self):
        """
        OVERRIDE
        This method is called when the user chose to create a backorder. It will create a new
        picking, the backorder, and move the stock.moves that are not `done` or `cancel` into it.
        """
        backorders = self.env['stock.picking']
        bo_to_assign = self.env['stock.picking']
        for picking in self:
            moves_to_backorder = picking.move_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            if moves_to_backorder:
                # START CHANGES BY AXXELIA
                backorder_name = self._get_next_backorder_name(picking.name)
                # END CHANGES BY AXXELIA
                backorder_picking = picking.copy({
                    'name': backorder_name,
                    'move_ids': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id
                })
                picking.message_post(
                    body=_('The backorder %s has been created.', backorder_picking._get_html_link())
                )
                moves_to_backorder.write({'picking_id': backorder_picking.id})
                moves_to_backorder.move_line_ids.package_level_id.write({'picking_id':backorder_picking.id})
                moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                backorders |= backorder_picking
                if backorder_picking.picking_type_id.reservation_method == 'at_confirm':
                    bo_to_assign |= backorder_picking
        if bo_to_assign:
            bo_to_assign.action_assign()
        return backorders

    def check_use_dummy_lot(self):
        self.ensure_one()
        use_dummy_lots = False
        if self.picking_type_code == 'incoming':
            not_lot_move_lines = self.move_line_nosuggest_ids.filtered(
                lambda l: l.product_id.tracking == 'lot' and not l.lot_name
            )
            if not_lot_move_lines:
                use_dummy_lots = True
        return use_dummy_lots

    def action_use_dummy_lot(self):
        self.ensure_one()
        not_lot_move_lines = self.move_line_nosuggest_ids.filtered(
            lambda l: l.product_id.tracking == 'lot' and not l.lot_name
        )
        ir_seq_env = self.env['ir.sequence']
        for ml in not_lot_move_lines:
            ml.write({
                'lot_name': ir_seq_env.next_by_code('dummy.lots')
            })
        return True

    def action_put_in_pack(self):
        """OVERRIDE to get rid of this commit:
        https://github.com/odoo/odoo/commit/e03c1a836f2d1dd0ffad27df75fc4779fd1368de
        """
        self.ensure_one()
        if self.state not in ('done', 'cancel'):
            picking_move_lines = self.move_line_ids
            if (
                not self.picking_type_id.show_reserved
                and not self.immediate_transfer
                and not self.env.context.get('barcode_view')
            ):
                picking_move_lines = self.move_line_nosuggest_ids

            move_line_ids = picking_move_lines.filtered(lambda ml:
                float_compare(ml.qty_done, 0.0, precision_rounding=ml.product_uom_id.rounding) > 0
                and not ml.result_package_id
            )
            # OVERRIDE: we do not want this
            # if not move_line_ids:
            #     move_line_ids = picking_move_lines.filtered(lambda ml: float_compare(ml.reserved_uom_qty, 0.0,
            #                          precision_rounding=ml.product_uom_id.rounding) > 0 and float_compare(ml.qty_done, 0.0,
            #                          precision_rounding=ml.product_uom_id.rounding) == 0)
            if move_line_ids:
                res = self._pre_put_in_pack_hook(move_line_ids)
                if not res:
                    res = self._put_in_pack(move_line_ids)
                return res
            else:
                raise UserError(_("Please add 'Done' quantities to the picking to create a new pack."))
