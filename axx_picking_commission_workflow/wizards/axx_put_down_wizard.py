# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AxxPutDownWizard(models.TransientModel):
    _name = "axx.put.down.wizard"
    _description = 'Put Down'

    axx_location_dest_name = fields.Char(
        string="WA-Bahn",
    )

    axx_partner_dest_name = fields.Char(
        string="Kunde"
    )

    axx_partner_dest_street = fields.Char(
        string="Strasse"
    )

    axx_partner_dest_zip = fields.Char(
        string="Postleitzahl"
    )

    axx_partner_dest_city = fields.Char(
        string="Ort"
    )

    @api.model
    def default_get(self, fields):
        res = super(AxxPutDownWizard, self).default_get(fields)
        if self.env.context.get('active_id'):
            picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id'))
            if picking_id.id:
                res['axx_location_dest_name'] = picking_id.location_dest_id.name
                res['axx_partner_dest_name'] = picking_id.partner_id.name
                res['axx_partner_dest_street'] = picking_id.partner_id.street
                res['axx_partner_dest_zip'] = picking_id.partner_id.zip
                res['axx_partner_dest_city'] = picking_id.partner_id.city
        return res
