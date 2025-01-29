# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    ofr_kom_type = fields.Selection([('pal', 'Palette'), ('kom', 'Kom')], string="KoM Type", default='kom')
