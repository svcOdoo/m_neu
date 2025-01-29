# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockMoveLineInherited(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        """
        To update the corresponding sale order with proper loading aid quantity
        which used for delivery loading
        """
        res = super(StockMoveLineInherited, self).write(vals)
        for move_line in self:
            if move_line.product_id.axx_is_loading_aid and move_line.move_id.product_uom_qty != \
                    move_line.move_id.quantity_done:
                if move_line.move_id.sale_line_id:
                    move_line.move_id.sudo().sale_line_id.write({
                        'product_uom_qty': move_line.move_id.quantity_done
                    })
        return res
