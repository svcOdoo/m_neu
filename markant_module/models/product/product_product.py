from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    axx_standard_location_full_seq = fields.Char(related="axx_standard_location_id.axx_full_seq")

    def _get_fields_stock_barcode(self):
        return super()._get_fields_stock_barcode() + ['axx_standard_location_full_seq']
