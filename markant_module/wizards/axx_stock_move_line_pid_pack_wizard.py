from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockMoveLinePidPackWizard(models.TransientModel):
    _name = 'stock.move.line.pid.pack.wizard'
    _description = 'Stock Move Line PID Pack Wizard'

    target_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Target Location',
        domain="[('usage', '=', 'internal')]",
    )
    set_quantity = fields.Boolean(string='Set Quantity?', default=True)
    validate_picking = fields.Boolean(string='Validate Picking?', default=True)

    def _update_move_line_location_qty(self, move_line):
        to_write = {}
        if self.target_location_id:
            to_write['location_dest_id'] = self.target_location_id.id

        if self.set_quantity or self.validate_picking:
            to_write['qty_done'] = move_line.reserved_uom_qty

        move_line.write(to_write)

    def _update_package_location(self, move_line):
        if self.target_location_id and move_line.package_level_id:
            move_line.package_level_id.write({'location_dest_id': self.target_location_id.id})

    def action_confirm(self):
        allowed_states = ['assigned', 'partially_available']
        move_line_ids = self._context.get('active_ids') and self._context.get('active_model') == 'stock.move.line' \
            and tuple(self._context.get('active_ids'))
        move_lines = self.env['stock.move.line'].browse(move_line_ids)

        if any(ml.state not in allowed_states for ml in move_lines):
            raise ValidationError("Diese Aktion ist ausschließlich für Positionen im Status 'Verfügbar' vorgesehen!")

        pickings = move_lines.mapped("move_id").mapped("picking_id")
        package_levels = move_lines.mapped("package_level_id")

        for move_line in move_lines:
            self._update_move_line_location_qty(move_line)
            self._update_package_location(move_line)

        if self.set_quantity:
            package_levels.write({'is_done': True})

        if self.validate_picking:
            for picking in pickings:
                picking.with_context(skip_expired=True).button_validate()
