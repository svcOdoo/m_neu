from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ofr_kom_type = fields.Selection([('pal', 'Palette'), ('kom', 'Kom')], string="KoM Type", default='kom')
    ofr_kom_route = fields.Many2one('stock.route', string="KoM Route")

    def update_kom_route(self):
        for rec in self:
            route_id = self.env['stock.route'].search([('ofr_kom_type', '=', rec.ofr_kom_type)], limit=1)
            rec.ofr_kom_route = route_id.id

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get('ofr_kom_type'):
            self.update_kom_route()
        if 'ofr_kom_route' in vals:
            self.mapped('order_line').write({
                'route_id': vals.get('ofr_kom_route')
            })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)
        for rec in res:
            if rec.ofr_kom_type and not rec.ofr_kom_route:
                rec.update_kom_route()
            rec.order_line.filtered(lambda l: not l.route_id).write({
                'route_id': rec.ofr_kom_route
            })
        return res
