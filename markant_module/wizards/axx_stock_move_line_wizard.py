from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMoveLineWizard(models.TransientModel):
    _name = 'stock.move.line.wizard'
    _description = 'Stock Move Line Wizard'

    target_location_id = fields.Many2one(
        'stock.location',
        string='Target Location',
        domain=[('usage', '=', 'internal')],
        required=True
    )

    def action_create_move(self):
        self.ensure_one()
        active_model = self.env.context.get('active_model')
        if active_model != 'stock.move.line':
            raise UserError("The active model must be 'stock.move.line'.")

        move_line_id = self.env.context.get('active_id')
        move_line = self.env['stock.move.line'].browse(move_line_id)
        move_line.write({'target_location_id': self.target_location_id.id})
        new_move = move_line._axx_create_new_move()

        moves_history_action = self.sudo().env.ref('markant_module.stock_move_line_action_pid_in')
        return {
            'type': moves_history_action.type,
            'name': moves_history_action.name,
            'res_model': moves_history_action.res_model,
            'view_mode': moves_history_action.view_mode,
            'target': moves_history_action.target,
            'context': moves_history_action.context,
            'views': moves_history_action.views,
        }

