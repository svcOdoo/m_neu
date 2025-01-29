from odoo import api, fields, models, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    axx_default_package_move = fields.Boolean(
        string='Picking used for moving packages'
    )

    @api.model
    def action_open_einlagern(self):
        action = self.env.ref('markant_module.stock_move_line_action_pid_in').read()[0]
        action['target'] = 'main'
        return action
