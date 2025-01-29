# -*- coding: utf-8 -*-
from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def ofr_update_stock_rule_type(self, picking_type='outgoing'):
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)

        picking_type_mapping = {
            'outgoing': warehouse.out_type_id.id,
            'packing': warehouse.pack_type_id.id,
        }
        self.picking_type_id = picking_type_mapping.get(picking_type, warehouse.out_type_id.id)
        self.warehouse_id = warehouse.id
