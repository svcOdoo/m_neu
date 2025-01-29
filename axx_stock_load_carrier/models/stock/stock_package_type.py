# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    axx_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Loading Aid",
        domain=[('axx_is_loading_aid', '=', True)]
    )
