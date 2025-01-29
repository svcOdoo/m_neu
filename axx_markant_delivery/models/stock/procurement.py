# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression


class ProcurementGroupInherited(models.Model):
    _inherit = "procurement.group"

    def get_existing_rule(self, product_id, location_src_id, location_dest_id, values):
        """
        Find the proper stock rule considering source location as well!
        """
        domain = self._get_rule_domain(location_dest_id, values)
        source_loc_domain = [('location_src_id', '=', location_src_id.id)]
        domain = expression.AND([domain, source_loc_domain])
        rule_id = self._search_rule(values.get('route_ids', False), values.get('product_packaging_id', False),
                                    product_id, values.get('warehouse_id', False), domain)
        return rule_id

    @api.model
    def _get_rule(self, product_id, location_id, values):
        """
        To crosscheck the rule selected with customer outgoing location selected.
        Create new rules, if not exists.
        """
        rule = super(ProcurementGroupInherited, self)._get_rule(product_id, location_id, values)
        if values.get('sale_line_id'):
            order_id = self.env['sale.order.line'].browse(values.get('sale_line_id')).order_id
            high_rule_id = self.env['stock.rule'].search([('company_id', '=', rule.company_id.id)],
                                                         order='sequence desc', limit=1)
            sequence = high_rule_id and high_rule_id.sequence or 0
            if order_id:
                output_loc_id = order_id.warehouse_id.wh_output_stock_loc_id
                partner_outgoing_loc_id = order_id.partner_id.axx_outgoing_location_id
                packaging_rule_id = self.get_existing_rule(product_id, partner_outgoing_loc_id,
                                                           output_loc_id, values)
                if not packaging_rule_id:
                    packaging_rule_id = rule.sudo().copy()
                    packing_type_id = self.env['stock.picking.type'].search([
                        ('sequence_code', '=', 'PACK'), ('code', '=', 'internal'),
                        ('company_id', '=', rule.company_id.id)], limit=1)
                    name = packaging_rule_id.warehouse_id.code + ': ' + partner_outgoing_loc_id.name + '->' + \
                        output_loc_id.name
                    sequence += 1 if sequence else rule.sequence + 1
                    packaging_rule_id.write({
                        'name': name,
                        'location_src_id': partner_outgoing_loc_id.id,
                        'location_dest_id': output_loc_id.id,
                        'picking_type_id': packing_type_id and packing_type_id.id,
                        'sequence': sequence,
                    })

                pick_location = order_id.warehouse_id.lot_stock_id
                picking_rule_id = self.get_existing_rule(product_id, pick_location, partner_outgoing_loc_id, values)
                if not picking_rule_id:
                    picking_rule_id = rule.sudo().copy()
                    picking_type_id = self.env['stock.picking.type'].search([
                        ('sequence_code', '=', 'PICK'), ('code', '=', 'internal'),
                        ('company_id', '=', rule.company_id.id)], limit=1)
                    name = picking_rule_id.warehouse_id.code + ': ' + pick_location.name + '->' + \
                        partner_outgoing_loc_id.name
                    sequence += 1 if sequence else high_rule_id.sequence + 1
                    picking_rule_id.write({
                        'name': name,
                        'location_src_id': pick_location and pick_location.id,
                        'location_dest_id': partner_outgoing_loc_id and partner_outgoing_loc_id.id,
                        'procure_method': 'make_to_stock',
                        'picking_type_id': picking_type_id and picking_type_id.id,
                        'sequence': sequence
                    })
        return rule
