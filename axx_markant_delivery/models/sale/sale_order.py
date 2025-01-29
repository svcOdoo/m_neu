# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderInherited(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        To check customer outgoing location configuration, update pick location and verify the stock rules
        """
        for order in self:
            if not order.partner_id.axx_outgoing_location_id:
                raise UserError(_('Customer outgoing location is not set! Please select one!'))
        res = super(SaleOrderInherited, self).action_confirm()
        for order in self:
            for picking_id in order.picking_ids:
                picking_id = picking_id.sudo()
                if picking_id.picking_type_id.sequence_code == 'PICK' or picking_id.picking_type_id.ofr_kom_type == 'pal':
                    picking_id.write({
                        'location_dest_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    picking_id.move_ids.write({
                        'location_dest_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    picking_id.move_line_ids and picking_id.move_line_ids.write({
                        'location_dest_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    self.update_rule_existing(picking_id, 'pick')
                if picking_id.picking_type_id.sequence_code == 'PACK':
                    picking_id.write({
                        'location_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    picking_id.move_ids.write({
                        'location_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    picking_id.move_line_ids and picking_id.move_line_ids.write({
                        'location_id': order.partner_id.axx_outgoing_location_id.id
                    })
                    self.update_rule_existing(picking_id, 'pack')
        return res

    def update_rule_existing(self, picking_id, rule_type):
        rule_id = False
        for move_id in picking_id.move_ids:
            if not rule_id or rule_id != move_id.rule_id.id:
                new_rule_id = False
                if rule_type == 'pick':
                    new_rule_id = self.env['procurement.group'].get_existing_rule(
                        move_id.product_id, move_id.location_id, move_id.location_dest_id,
                        {'warehouse_id': move_id.warehouse_id, 'company_id': move_id.company_id})
                elif rule_type == 'pack':
                    new_rule_id = self.env['procurement.group'].get_existing_rule(
                        move_id.product_id, move_id.location_id, move_id.location_dest_id,
                        {'warehouse_id': move_id.warehouse_id, 'company_id': move_id.company_id})
                if not new_rule_id:
                    high_seq_rule_id = self.env['stock.rule'].search(
                        [('company_id', '=', picking_id.company_id.id)], order='sequence desc', limit=1)
                    sequence = high_seq_rule_id and high_seq_rule_id.sequence or move_id.rule_id.sequence or 0

                    new_rule_id = move_id.rule_id.copy()
                    new_warehouse = new_rule_id.warehouse_id and new_rule_id.warehouse_id.code or 'WH'
                    new_src_name = new_rule_id.location_src_id.name
                    new_dest_name = new_rule_id.location_dest_id.name
                    name = new_warehouse + ': ' + new_src_name + '->' + new_dest_name
                    vals = False
                    if rule_type == 'pick':
                        vals = {
                            'name': name,
                            'location_dest_id': move_id.location_dest_id.id,
                            'sequence': sequence + 1
                        }
                    elif rule_type == 'pack':
                        vals = {
                            'name': name,
                            'location_src_id': move_id.location_id.id,
                            'sequence': sequence + 1
                        }
                    if vals:
                        new_rule_id.update(vals)
                rule_id = move_id.rule_id.id
                move_id.update({
                    'rule_id': new_rule_id and new_rule_id.id
                })
