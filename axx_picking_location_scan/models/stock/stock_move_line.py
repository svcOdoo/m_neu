# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    axx_barcode = fields.Char(
        string="Barcode / Check Digit"
    )
    axx_is_barcode_required = fields.Boolean(
        string="Is Barcode Required?",
        compute="compute_axx_is_barcode_required"
    )

    def compute_axx_is_barcode_required(self):
        for move in self:
            barcode_required = False
            # we use barcode app instead
            # prod_standard_loc = move.product_id.axx_standard_location_id
            # if prod_standard_loc and prod_standard_loc.axx_picking_location_scan and prod_standard_loc.axx_check_digit:
            #     barcode_required = True
            move.axx_is_barcode_required = barcode_required

    @api.onchange("axx_barcode", "product_id")
    def onchange_axx_barcode(self):
        if self.axx_barcode and self.axx_is_barcode_required:
            prod_standard_loc = self.product_id.axx_standard_location_id
            picking_loc_scan = prod_standard_loc.axx_picking_location_scan
            if (picking_loc_scan == 'check_digit' and self.axx_barcode != prod_standard_loc.axx_check_digit) or (picking_loc_scan == 'barcode' and self.axx_barcode != prod_standard_loc.barcode):
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _('Incorrect Barcode/Check Digit for product %s! Scanned barcode: %s. Expected barcode: %s!') % (
                            self.product_id.name, self.axx_barcode, prod_standard_loc.axx_check_digit
                        ),
                    }
                }

    @api.constrains("axx_barcode", "product_id")
    def check_axx_barcode(self):
        for move in self:
            if move.axx_barcode and move.axx_is_barcode_required:
                prod_standard_loc = move.product_id.axx_standard_location_id
                picking_loc_scan = prod_standard_loc.axx_picking_location_scan
                if (picking_loc_scan == 'check_digit' and move.axx_barcode != prod_standard_loc.axx_check_digit) or (picking_loc_scan == 'barcode' and move.axx_barcode != prod_standard_loc.barcode):
                    raise ValidationError(_('Incorrect Barcode/Check Digit for product %s! Scanned barcode: %s. Expected barcode: %s!') % (
                        self.product_id.name, self.axx_barcode, prod_standard_loc.axx_check_digit
                    ))
