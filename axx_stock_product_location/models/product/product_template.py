# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    axx_standard_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Standard Location",
        domain="[('usage', '=', 'internal')]",
        compute='_compute_axx_standard_location_id',
        inverse='_set_axx_standard_location_id',
        readonly=False,
        store=True
    )
    axx_reserve_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Reserve Location",
        domain="[('usage', '=', 'internal')]",
        compute='_compute_axx_reserve_location_id',
        inverse='_set_axx_reserve_location_id',
        readonly=False,
        store=True
    )
    detailed_type = fields.Selection(default='product')

    @api.depends('product_variant_ids', 'product_variant_ids.axx_standard_location_id')
    def _compute_axx_standard_location_id(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.axx_standard_location_id = template.product_variant_ids.axx_standard_location_id
        for template in (self - unique_variants):
            template.axx_standard_location_id = False

    def _set_axx_standard_location_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.axx_standard_location_id = template.axx_standard_location_id

    @api.depends('product_variant_ids', 'product_variant_ids.axx_reserve_location_id')
    def _compute_axx_reserve_location_id(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.axx_reserve_location_id = template.product_variant_ids.axx_reserve_location_id
        for template in (self - unique_variants):
            template.axx_reserve_location_id = False

    def _set_axx_reserve_location_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.axx_reserve_location_id = template.axx_reserve_location_id
