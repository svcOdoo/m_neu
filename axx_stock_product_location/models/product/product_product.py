# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    axx_standard_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Standard Location",
        domain="[('usage', '=', 'internal')]"
    )
    axx_reserve_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Reserve Location",
        domain="[('usage', '=', 'internal')]"
    )
