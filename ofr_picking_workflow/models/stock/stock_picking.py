# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def apply_palette_picking(self):
        self.ensure_one()
        return self.picking_type_id.ofr_kom_type == 'pal'

    def axx_find_open_backorder(self):
        backorder_id = super(StockPicking, self).axx_find_open_backorder()
        if self.apply_palette_picking() and backorder_id:
            backorder_open = self.env['stock.picking'].browse(backorder_id)
            backorder_open_rec = backorder_open.exists() and backorder_open.state == 'assigned' or False
            return {'backorder_id': backorder_id, 'skip_pid': True, 'open_backorder': backorder_open_rec}
        return super(StockPicking, self).axx_find_open_backorder()

    def get_need_pack_action_ignore_pid(self):
        if self.apply_palette_picking():
            return False
        return super(StockPicking, self).get_need_pack_action_ignore_pid()

    def _action_done(self):
        for rec in self:
            if rec.apply_palette_picking() and\
                    any(line.qty_done and line.reserved_uom_qty != line.qty_done for line in rec.move_line_ids):
                raise ValidationError(_("You cannot transfer partial packages"))
        return super(StockPicking, self)._action_done()

