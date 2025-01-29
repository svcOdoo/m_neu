# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    axx_standard_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Standard Location",
        related="product_id.axx_standard_location_id",
        readonly=True
    )

    @api.constrains('product_id', 'location_dest_id', 'picking_type_id')
    def _check_location_dest_id(self):
        for move in self:
            if move.picking_type_id and move.picking_type_id.code == 'incoming':
                if move.product_id.axx_reserve_location_id and move.product_id.axx_reserve_location_id.id != move.location_dest_id.id:
                    move.location_dest_id = move.product_id.axx_reserve_location_id.id
