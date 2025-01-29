# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    axx_standard_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Standard Location",
        related="product_id.axx_standard_location_id",
        readonly=True,
    )
    axx_standard_location_name = fields.Char(related='axx_standard_location_id.name', readonly=True)
