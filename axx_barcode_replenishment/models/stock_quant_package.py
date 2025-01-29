
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    @api.model
    def axx_get_package_info(self, product_id):
        stock_quants = self.env['stock.quant'].search([('product_id', '=', product_id), ('package_id', '!=', False),
                                                       ('quantity', '>', 0)])
        packages = []
        for quant in stock_quants:
            packages.append({
                'id': quant.package_id.id,
                'quantity': quant.quantity,
                'name': quant.package_id.name,
                'location': quant.location_id.display_name
            })
        return packages

    @api.model
    def axx_get_package_info_form(self, product_id, dest_location_id):
        main_stock_location = self.env.ref('stock.stock_location_stock')
        stock_quants = self.env['stock.quant'].search(
            [('product_id', '=', product_id),
             ('location_id', 'child_of', main_stock_location.id),
             ('location_id', '!=', main_stock_location.id),
             ('location_id', '!=', dest_location_id),
             ('package_id', '!=', False),
             ('quantity', '>', 0),
             ], order='in_date asc'
        )
        # dest_location_id = self.env['stock.location'].browse(dest_location_id)
        packages = []
        for quant in stock_quants:
            use_date = quant.lot_id.use_date if quant.lot_id and quant.lot_id.use_date else ''
            lot = quant.lot_id.name if quant.lot_id else ''
            packages.append({
                'id': quant.package_id.id,
                'quantity': quant.quantity,
                'name': quant.package_id.name,
                'location': quant.location_id.display_name,
                'useDate': str(use_date)[:10] if use_date else '',
                'lot': lot,  # Include the Lot field
            })
        packages = sorted(packages, key=lambda x: x['useDate'] or '9999-12-31')  # Use a far-future date as a default
        return packages

    @api.model
    def axx_get_product_info(self, barcode):
        product_id = self.env['product.product'].search([('barcode', '=', barcode)])
        if product_id:
            location_id = product_id.axx_standard_location_id
            return {
                'product_id': product_id.id,
                'location_id': location_id.id,
                'name': product_id.display_name,
                'location_name': location_id.display_name
                    }
        else:
            location_id = self.env['stock.location'].search([('barcode', '=', barcode)])
            if location_id:
                product_id = self.env['product.product'].search([('axx_standard_location_id', '=', location_id.id)])
                return {
                    'product_id': product_id.id,
                    'location_id': product_id.axx_standard_location_id.id,
                    'name': product_id.display_name,
                    'location_name': location_id.display_name
                }
        return {}

    def action_move_unpack(self, dest_location_id=False):
        picking_id = False
        for rec in self:
            if len(self.quant_ids.mapped('product_id').mapped('id')) > 1:
                raise UserError(_('We can move and unpack only one product!'))
            if not rec.quant_ids:
                continue
            product_id = rec.quant_ids.mapped('product_id')
            quant_ids = rec.quant_ids.filtered(lambda l: l.quantity > 0)
            quantity = sum(quant_ids.mapped('quantity'))
            lot_id = quant_ids.mapped('lot_id') and quant_ids.mapped('lot_id')[0] or False
            if not dest_location_id:
                dest_location_id = product_id.axx_standard_location_id
            else:
                dest_location_id = self.env['stock.location'].browse(dest_location_id)
            src_location_id = rec.location_id
            # make sure to unreserve
            rec._unreserve_moves(src_location_id)
            # create picking
            picking_id = rec._create_picking(src_location_id, dest_location_id)
            rec._create_moves(picking_id, product_id, quantity, src_location_id, dest_location_id, lot_id=lot_id)
            # mark as done picking
            picking_id.action_assign()
            picking_id._action_done()
            # unpack the package
            rec.unpack()
        if picking_id:
            return True
        return picking_id

    def _unreserve_moves(self, src_location_id):
        """
        Try to unreserve moves that they has reserved quantity before moving
        """
        product_id = self.quant_ids.mapped('product_id')
        move_lines = self.env['stock.move.line'].search(
                [
                    ('state', '=', 'assigned'),
                    ('product_id', '=', product_id.id),
                    ('location_id', '=', src_location_id.id),
                    ('package_id', '=', self.id),
                    ('qty_done', '>', 0.0),
                ]
            )
        moves_to_unreserve = move_lines.mapped('move_id')
        # Unreserve in old location
        moves_to_unreserve._do_unreserve()

    def _create_picking(self, src_location_id, dest_location_id):
        picking_type_id = self.env['stock.picking.type'].search([('axx_default_package_move', '=', True)],limit=1)
        if not picking_type_id:
            raise UserError(_('Please set a default picking type to move packages!'))
        if not src_location_id.id:
            raise UserError(_('No src location is selected!'))
        if not dest_location_id.id:
            raise UserError(_('No destination location is selected!'))
        
        return self.env['stock.picking'].create(
            {
                'picking_type_id': picking_type_id.id,
                'location_id': src_location_id.id,
                'location_dest_id': dest_location_id.id,
            }
        )

    def _create_moves(self, picking, product_id, quantity, src_location_id, dest_location_id, lot_id=False):
        move_vals = {
            'name': product_id.name,
            'product_id': product_id.id,
            'product_uom_qty': quantity,
            'quantity_done': quantity,
            'product_uom': product_id.uom_id.id,
            'picking_id': picking.id,
            'location_id': src_location_id.id,
            'location_dest_id': dest_location_id.id,
        }

        move = self.env['stock.move'].create(move_vals)
        move._action_confirm()
        move._action_assign()
