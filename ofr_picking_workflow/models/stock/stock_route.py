# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockRoute(models.Model):
    _inherit = "stock.route"

    ofr_kom_type = fields.Selection([('pal', 'Palette'), ('kom', 'Kom')], string="KoM Type")
