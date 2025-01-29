from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    axx_reference = fields.Char(string='PID In')

    def copy(self, default=None):
        res = super().copy(default)
        # with our current use case of axx_reference we can use this logic in warehouse out as well
        if self.env.context.get('axx_receipt_pack') or True:
            # stock.picking#_put_in_pack is using copy() to create new move lines
            # in receipts, we might enter the reference before using put in pack, therefore we need to apply the
            # axx_reference to the new record only.
            res.axx_reference = self.axx_reference
            self.axx_reference = False
        return res
