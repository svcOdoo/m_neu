# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    ofr_kom_type = fields.Selection(related='picking_type_id.ofr_kom_type')

    def _action_assign(self, force_qty=False):
        ofr_palette_picking = self.mapped('picking_type_id.ofr_kom_type')
        ofr_palette_picking = ofr_palette_picking and ofr_palette_picking[0] or False
        res = super(StockMove, self.with_context(ofr_palette_picking=ofr_palette_picking))._action_assign(force_qty=force_qty)
        return res
