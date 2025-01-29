# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def get_barcode_nomenclature(self):
        if self.picking_type_id.axx_nomenclature_id:
            return [self.picking_type_id.axx_nomenclature_id.id]
        return []


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    axx_nomenclature_id = fields.Many2one('barcode.nomenclature', 'Barcode Nomenclature')
