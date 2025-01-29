# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockLocation(models.Model):
    _inherit = "stock.location"

    axx_picking_location_scan = fields.Selection([
        ('barcode', 'Barcode'),
        ('check_digit', 'Check Digit'),
    ], string="Picking Location Scan?")
    axx_check_digit = fields.Char(
        string="Check Digit"
    )

    @api.model
    def _get_fields_stock_barcode(self):
        fields = super(StockLocation, self)._get_fields_stock_barcode()
        fields.extend(['axx_picking_location_scan', 'axx_check_digit'])
        return fields
