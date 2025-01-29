from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import math


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def axx_action_split_open_wizard(self):
        self.ensure_one()
        if self.move_line_ids.filtered(lambda x: x.qty_done > 0):
            if self.env.context.get('form_view_action', False):
                raise ValidationError(_("Auftrag %s ist bereits in Bearbeitung!") % self.name)
            return False
        context = dict(self.env.context)
        context.update({'active_id': self.id, 'active_model': self._name, 'active_ids': self.ids,
                        'client_action': self.env.context.get('axx_client_action', True),
                        'default_axx_lines_count': len(self.move_ids)})
        return {
            'name': _("Split %s") % self._description,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'axx.split.record.wizard',
            'target': 'new',
            'context': context,
        }

    @api.model
    def get_param_split_limit(self):
        split_limit = self.env['ir.config_parameter'].sudo().get_param('split.limit', 0)
        return int(split_limit)

    def get_split_action(self, limit):
        self.ensure_one()
        if len(self.move_ids) > limit:
            return self.with_context(axx_client_action=False).axx_action_split_open_wizard()
        return False

    @api.model
    def _axx_get_backorder_name(self, picking_name, iteration_number, existing_picking_names):
        """
        Compute the next backorder name based on the given picking name.

        Naming Conventions:
        - If the provided picking name does not have a suffix in the format '-X', where 'X' is a number
        (e.g., 'OUT/123'), the returned name will append '-1' to it, resulting in 'OUT/123-1'.
        - If the provided picking name already has a number suffix (e.g., 'OUT/345-1'), the suffix number will be
          incremented. For instance, 'OUT/345-1' will yield 'OUT/345-2'.

        Returns:
        - str: The computed name for the backorder.
        """
        name_parts = picking_name.rsplit('-', 1)
        iteration_number += 1

        if len(name_parts) == 2 and name_parts[1].isdigit():
            target_number = iteration_number + int(name_parts[1])
            base_name = name_parts[0]
        else:
            target_number = iteration_number
            base_name = picking_name

        while True:
            new_name = f"{base_name}-{target_number}"
            if new_name not in existing_picking_names:
                return new_name, iteration_number
            target_number += 1

    def axx_create_backorder(self, axx_split_count=1):
        """ This method is called when the user chose to create a backorder after splitting the picking.
        """
        if axx_split_count <= 1:
            return self
        backorders = self
        bo_to_assign = self.env['stock.picking']
        for picking in self.filtered(lambda p: p.state not in ['done', 'cancel']):
            if picking.move_line_ids.filtered(lambda x: x.qty_done > 0):
                raise ValidationError(_("Auftrag %s ist bereits in Bearbeitung!") % picking.name)
            moves_to_backorder = picking.move_ids
            existing_picking_names = self.search([('name', 'like', picking.name + '%')]).mapped('name')
            if moves_to_backorder:
                parts_count = math.ceil(len(moves_to_backorder) / axx_split_count)
                iteration_number = 0
                for part in range(parts_count, len(moves_to_backorder), parts_count):
                    moves_to_split = moves_to_backorder[part: part + parts_count]
                    backorder_name, iteration_number = (
                        self._axx_get_backorder_name(picking.name, iteration_number, existing_picking_names))
                    backorder_picking = picking.copy({
                        'name': backorder_name,
                        'move_ids': [],
                        'move_line_ids': [],
                        'backorder_id': picking.id
                    })
                    picking.message_post(
                        body=_('The backorder (SPLIT) %s has been created.', backorder_picking._get_html_link())
                    )
                    moves_to_split.write({'picking_id': backorder_picking.id})
                    moves_to_split.move_line_ids.package_level_id.write({'picking_id': backorder_picking.id})
                    moves_to_split.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                    backorders |= backorder_picking
                    if backorder_picking.picking_type_id.reservation_method == 'at_confirm':
                        bo_to_assign |= backorder_picking
        if bo_to_assign:
            bo_to_assign.action_assign()
        return backorders

    def axx_split_pickings(self, axx_split_count=1):
        backorders = self.axx_create_backorder(axx_split_count)
        return {
            'name': self._description,
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'tree,kanban,form,calendar,map',
            'res_model': 'stock.picking',
            'domain': [('id', '=', backorders.ids)],
            'target': 'current',
            'context': self.env.context,
        }


