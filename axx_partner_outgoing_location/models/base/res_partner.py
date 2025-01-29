# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    axx_outgoing_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Outgoing Location",
        domain="[('usage', '=', 'internal')]",
        help="The location (WA-Bahn) where products to be sent out to the customer are collected and packed, waiting to be picked up by a truck."
    )
