# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    axx_is_packing_zone_dest_loc = fields.Boolean(
        string="Is Outgoing Destination Location?",
        compute="compute_axx_is_packing_zone_dest_loc"
    )

    def compute_axx_is_packing_zone_dest_loc(self):
        packing_zone_loc = self.env.ref("stock.location_pack_zone")
        packing_zone_locs = self.env['stock.location'].search([('id', 'child_of', packing_zone_loc.ids)]) | packing_zone_loc
        for move in self:
            move.axx_is_packing_zone_dest_loc = move.location_dest_id.id in packing_zone_locs.ids

