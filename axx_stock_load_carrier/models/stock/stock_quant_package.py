from odoo import api, fields, models, _


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    axx_sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', name='Sale Order Line')

    def write(self, vals):
        res = super(StockQuantPackage, self).write(vals)
        if 'package_type_id' in vals:
            move_lines = self.env['stock.move.line'].search([('result_package_id', '=', self.id)])
            for move_line in move_lines:
                if move_line.picking_id and move_line.picking_id.sale_id:
                    move_line.picking_id._axx_create_sale_line_carrier(self)
        return res
