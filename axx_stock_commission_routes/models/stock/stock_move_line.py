# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    _order = "sequence, result_package_id desc, location_id asc, location_dest_id asc, picking_id asc, id"

    sequence = fields.Integer(
        'Sequence',
        related="move_id.sequence",
        store=True
    )
