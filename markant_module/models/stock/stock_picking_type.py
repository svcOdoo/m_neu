from odoo import api, fields, models, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    axx_default_package_move = fields.Boolean(
        string='Picking used for moving packages'
    )
