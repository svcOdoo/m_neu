# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

MAX_SEQUENCE_DIGITS = 4
MAX_SEQUENCE = 9999


class StockLocation(models.Model):
    _inherit = "stock.location"

    axx_seq = fields.Integer(
        string="Sequence",
        help="""The sequence of the operations in the picking follows the sequence of the Standard Location of the products.
        It is grouped according to the parent location. 
        Example: Aisle A and Aisle B each have 100 locations with sequence 1-100. In Picking, all locations from Aisle A come first, then Aisle B.""",
        default=1,
    )
    axx_full_seq = fields.Char(
        string="Full Sequence",
        compute="compute_axx_full_seq",
        readonly=True,
        store=True,
        recursive=True,
        index=True
    )

    @api.constrains("axx_seq")
    def _check_axx_seq(self):
        for loc in self:
            if loc.axx_seq and loc.axx_seq > MAX_SEQUENCE:
                raise ValidationError(_('The sequence cannot be greater than %s!') % (
                    str(MAX_SEQUENCE)
                ))

    @api.depends('axx_seq', 'location_id', 'location_id.axx_seq', 'location_id.axx_full_seq')
    def compute_axx_full_seq(self):
        for loc in self:
            formatted_seq = str(loc.axx_seq)
            len_formatted_seq = len(formatted_seq)
            if len_formatted_seq < MAX_SEQUENCE_DIGITS:
                for i in range(MAX_SEQUENCE_DIGITS - len_formatted_seq):
                    formatted_seq = '0' + formatted_seq
            if loc.location_id:
                loc.axx_full_seq = '.'.join([loc.location_id.axx_full_seq or '0000', formatted_seq])
            else:
                loc.axx_full_seq = formatted_seq
