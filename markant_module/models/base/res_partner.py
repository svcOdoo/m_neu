# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    axx_trading_partner_name = fields.Char(
        string="Contact Person HP"
    )
    axx_trading_partner_email = fields.Char(
        string="E-Mail HP"
    )
    axx_trading_partner_phone = fields.Char(
        string="Phone HP"
    )
    axx_trading_partner_mobile = fields.Char(
        string="Mobile HP"
    )
    axx_trading_partner_fax = fields.Char(
        string="Fax HP"
    )
    axx_gln = fields.Char(
        string="GLN"
    )
