from odoo import models, fields, api, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    ofr_palette_picking = fields.Boolean("Palette picking", compute='_compute_palette_picking')

    def _compute_palette_picking(self):
        for rec in self:
            rec.ofr_palette_picking = rec.picking_id.apply_palette_picking()

    def _get_fields_stock_barcode(self):
        return super()._get_fields_stock_barcode() + ['ofr_palette_picking']