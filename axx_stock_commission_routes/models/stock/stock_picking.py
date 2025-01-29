# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    axx_is_loc_seq_broken = fields.Boolean(
        string="Is Product Standard Location Sequence Broken?",
        copy=False
    )

    def re_order_operation_lines(self):
        for picking in self:
            move_seq = 1
            for line in picking.move_ids_without_package.sorted(lambda l: l.axx_loc_full_seq):
                line.with_context(no_break_loc_seq=True).sequence = move_seq
                move_seq += 1
        return True
