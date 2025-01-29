# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockLocation(models.Model):
    _inherit = "stock.location"

    axx_is_outgoing_loc = fields.Boolean(
        string="Is Outgoing Location",
        compute="compute_axx_is_outgoing_loc",
        readonly=True
    )

    def compute_axx_is_outgoing_loc(self):
        partner_env = self.env['res.partner']
        for loc in self:
            partners = partner_env.search([
                ('axx_outgoing_location_id', '=', loc.id)
            ])
            loc.axx_is_outgoing_loc = True if partners else False
