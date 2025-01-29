from odoo import fields, models, api


class AxxStandardLocationSelectWizard(models.TransientModel):
    _name = 'axx.standard.location.select.wizard'
    _description = "Wizard to select standard location"

    axx_standard_location_id = fields.Many2one('stock.location', 'Destination Location')
    axx_product_id = fields.Many2one('product.product', 'Product')
    
    @api.onchange('axx_standard_location_id', 'axx_product_id')
    def _onchange_axx_standard_location_id(self):
        if self.axx_standard_location_id and not self.axx_product_id:
            self.axx_product_id = self.env['product.product'].search([('axx_standard_location_id', '=', self.axx_standard_location_id.id)])
        elif not self.axx_standard_location_id and self.axx_product_id:
            self.axx_standard_location_id = self.axx_product_id.axx_standard_location_id

    def action_confirm(self):
        if self.axx_standard_location_id and self.axx_product_id:
            action = self.env['ir.actions.actions']._for_xml_id('axx_barcode_replenishment.stock_quant_package_action')
            action['domain'] = [('location_id', '=', self.axx_standard_location_id.id),('product_id','=',self.axx_product_id.id)]
            return action
