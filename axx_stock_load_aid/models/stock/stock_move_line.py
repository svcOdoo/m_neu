# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockMoveLineInherited(models.Model):
    _inherit = "stock.move.line"

    # def write(self, vals):
    #     """
    #     To update the corresponding sale order with proper loading aid quantity
    #     which used for delivery loading
    #     """
    #     if 'qty_done' in vals:
    #         if self.product_id.axx_is_loading_aid and self.picking_id.sale_id:
    #             if self.move_id.sale_line_id:
    #                 self.move_id.write({
    #                     'product_uom_qty': sum(self.move_id.mapped('move_line_ids').filtered(
    #                         lambda line: line.id != self.id).mapped('qty_done')) + vals.get('qty_done') or 0
    #                 })
    #                 self.move_id.sudo().sale_line_id.write({
    #                     'product_uom_qty': sum(self.move_id.mapped('move_line_ids').filtered(
    #                         lambda line: line.id != self.id).mapped('qty_done')) + vals.get('qty_done') or 0
    #                 })
    #             else:
    #                 sale_line_values = {
    #                     'product_id': self.product_id.id,
    #                     'product_uom_qty': sum(self.move_id.mapped('move_line_ids').filtered(
    #                         lambda line: line.id != self.id).mapped('qty_done')) + vals.get('qty_done') or 0,
    #                     'price_unit': self.product_id.lst_price or 0,
    #                     'order_id': self.picking_id.sale_id.id,
    #                     'move_ids': [(6, 0, self.move_id.ids)],
    #                 }
    #                 self.env['sale.order.line'].create(sale_line_values)
    #     res = super(StockMoveLineInherited, self).write(vals)
    #     return res
