from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrderLine, self).create(vals_list)
        for rec in res:
            if rec.order_id.ofr_kom_route and not rec.route_id:
                rec.route_id = rec.order_id.ofr_kom_route.id
        return res
