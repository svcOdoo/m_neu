from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _sanity_check(self, separate_pickings=True):
        """ Sanity check for `button_validate()`
            :param separate_pickings: Indicates if pickings should be checked independently for lot/serial numbers or not.
        """
        res = super(StockPicking, self)._sanity_check(separate_pickings)

        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        pickings_without_pids = self.browse()
        products_without_lots = self.env['product.product']

        no_quantities_done_ids = set()
        for picking in self:
            if all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel'))):
                no_quantities_done_ids.add(picking.id)

        pickings_using_pids = self.filtered(lambda p: p.picking_type_id.code == 'incoming')
        if pickings_using_pids:
            lines_to_check = pickings_using_pids._get_lot_move_lines_for_sanity_check(
                no_quantities_done_ids, separate_pickings)
            for line in lines_to_check:
                if not line.axx_reference:
                    pickings_without_pids |= line.picking_id
                    products_without_lots |= line.product_id

        if not self._should_show_transfers():
            if pickings_without_pids:
                raise UserError(_('You need to supply a PID number for products %s.') %
                                ', '.join(products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_pids:
                message += _('\n\nTransfers %s: You need to supply a PID number for products %s.') % (
                               ', '.join(pickings_without_pids.mapped('name')),
                               ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())
        return res
