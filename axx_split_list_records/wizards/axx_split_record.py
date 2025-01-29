from odoo import models, fields, api, _


class AxxSplitRecordWizard(models.Model):
    _name = 'axx.split.record.wizard'
    _description = 'Split Record'

    axx_split_count = fields.Integer("Split To", default=2)
    axx_lines_count = fields.Integer("Lines Count", default=0)

    def axx_action_split(self):
        record = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_ids'))
        action = record.axx_split_pickings(self.axx_split_count)
        return action

    def axx_action_open(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': self.env.context.get('active_id'),
            'target': 'current',
            'context': self.env.context,
        }

    def axx_action_disable(self):
        self.env['ir.config_parameter'].sudo().set_param('split.limit', "0")
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': self.env.context.get('active_id'),
            'target': 'current',
            'context': self.env.context,
        }

