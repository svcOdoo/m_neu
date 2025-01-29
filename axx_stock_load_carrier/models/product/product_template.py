# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplateInherited(models.Model):
    _inherit = "product.template"

    axx_is_loading_aid = fields.Boolean(string='Loading Aid')
