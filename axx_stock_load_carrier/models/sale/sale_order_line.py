
from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    axx_stock_quant_package_ids = fields.One2many(
        comodel_name='stock.quant.package',
        inverse_name='axx_sale_order_line_id',
        name='Picking Packages'
    )
