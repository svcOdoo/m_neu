# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"
    _order = 'sequence, id'

    axx_loc_full_seq = fields.Char(
        string="Location Full Sequence",
        compute="compute_axx_loc_full_seq"
    )

    def compute_axx_loc_full_seq(self):
        for move in self:
            loc_full_seq = '0'
            if move.product_id.axx_standard_location_id and move.product_id.axx_standard_location_id.axx_full_seq:
                loc_full_seq = move.product_id.axx_standard_location_id.axx_full_seq
            move.axx_loc_full_seq = loc_full_seq

    @api.model_create_multi
    def create(self, vals_list):
        moves = super(StockMove, self).create(vals_list)
        moves.filtered(
            lambda m: m.picking_id and not m.picking_id.axx_is_loc_seq_broken).mapped(
            "picking_id").re_order_operation_lines()
        return moves

    def write(self, vals):
        context = dict(self._context) or {}
        res = super(StockMove, self).write(vals)
        if 'sequence' in vals and not context.get('no_break_loc_seq', False):
            self.mapped("picking_id").write({
                'axx_is_loc_seq_broken': True
            })
        if 'product_id' in vals:
            self.mapped("picking_id").filtered(lambda p: not p.axx_is_loc_seq_broken).re_order_operation_lines()
        return res
