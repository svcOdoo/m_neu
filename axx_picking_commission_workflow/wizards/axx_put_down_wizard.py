# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AxxPutDownWizard(models.TransientModel):
    _name = "axx.put.down.wizard"
    _description = 'Put Down'

    axx_location_dest_name = fields.Char(
        string="WA-Bahn",
    )

    @api.model
    def default_get(self, fields):
        res = super(AxxPutDownWizard, self).default_get(fields)
        if self.env.context.get('active_id'):
            picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id'))
            if picking_id.id:
                res['axx_location_dest_name'] = picking_id.location_dest_id.name
        return res
