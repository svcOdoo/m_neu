from odoo import api, models
from odoo.tools import float_compare, float_is_zero


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        rounding = product_id.uom_id.rounding
        self = self.with_context(ofr_qty_need=quantity)
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id,
                              strict=strict)
        available_quantity = sum(
            quants.filtered(lambda q: float_compare(q.quantity, 0, precision_rounding=rounding) > 0).mapped(
                'quantity')) - sum(quants.mapped('reserved_quantity'))
        if not float_is_zero(available_quantity, precision_rounding=rounding):
            quantity = min(available_quantity, quantity)
        return super(StockQuant, self)._update_reserved_quantity(product_id, location_id, quantity,
                                                                 lot_id, package_id, owner_id, strict)

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        quants = super(StockQuant, self)._gather(product_id, location_id, lot_id, package_id, owner_id, strict)
        standard_loc_id = product_id.axx_standard_location_id.id if product_id.axx_standard_location_id else False
        if self.env.context.get('ofr_palette_picking', 'kom') == 'pal' and not self.env.context.get('import_file', False):
            package_quants = self.env['stock.quant']
            if standard_loc_id:
                quants = quants.filtered(lambda q: q.location_id.id != standard_loc_id)
            if self.env.context.get('ofr_qty_need') and self.env.context.get('ofr_qty_need') > 0:
                for quant in quants:
                    if quant.quantity > self.env.context.get('ofr_qty_need'):
                        continue
                    package_quants |= quant
                return package_quants
        return quants
