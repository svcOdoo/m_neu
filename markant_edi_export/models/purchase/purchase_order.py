from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'axx.export.data.source']

    axx_is_export = fields.Boolean(
        string='Is EDI CSV Export?',
        copy=False,
        default=False,
        help='Purchase Order Lines will be transferred to EDI CSV when the Purchase Order is confirmed.'
    )
    axx_export_count = fields.Integer(string='Export Count', compute='_compute_axx_export_count')

    # --------------
    # EXPORT SECTION
    # --------------
    def _compute_axx_export_count(self):
        data_export_env = self.env['axx.data.export']
        for record in self:
            record.axx_export_count = data_export_env.search_count(self._get_axx_export_domain())

    def axx_data_export_name(self):
        return "EDI CSV Order"

    @api.model
    def axx_fields_to_export(self):
        return [
            "partner_id.axx_gln",                               # ILNLIEFERANT
            "company_id.partner_id.axx_gln",                    # ILNKAEUFER
            "picking_type_id.warehouse_id.partner_id.axx_gln",  # ILNLIEFERANSCHRIFT
            # None,                                               # ILNRECHNUNGSEMPFAENGER  # TODO TDB
            # None,                                               # KENNZEICHENWAEHRUNG
            "name",                                             # KUNDENAUFTRAGSNUMMER
            "date_planned",                                     # LIEFERDATUM
            "date_approve",                                     # DATUMKUNDENAUFTRAG
            # None,                                               # VALUTADATUM
            "picking_type_id.warehouse_id.partner_id.name",     # NAME1LIEFERADRESSE
            # None,                                               # NAME2LIEFERADRESSE
            # None,                                               # NAME3LIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.street",   # STRASSELIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.zip",      # PLZLIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.city",     # ORTLIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.country_id.code",  # LANDLIEFERADRESSE
            {
                "order_line": [
                    'sequence',                                 # POSITIONSNUMMER
                    'product_qty',                              # BESTELLMENGE
                    'product_packaging_qty',                    # BESTELLMENGE
                    'product_id.axx_gtin_vpe',                  # EAN
                    'product_id.axx_supplier_article_number',   # ARTIKELLIEFERANTENNUMMER
                    'product_id.name',                          # ARTIKELBESCHREIBUNG
                    # None,                                       # BESTELLMENGENEINHEIT
                    # None,                                       # NATURALRABATT
                    'state',                                    # STATUS
                    # None,                                       # USER_EDIDATENVERKEHR
                ]
            },
        ]

    @api.model
    def axx_fields_export_trigger(self):
        return [
            "state",
        ]

    @api.model
    def axx_fields_export_trigger_domain(self):
        return [('state', 'in', ['purchase'])]

    @api.model
    def axx_required_fields_for_export(self):
        return [
            "partner_id.axx_gln",                               # ILNLIEFERANT
            "company_id.partner_id.axx_gln",                    # ILNKAEUFER
            "picking_type_id.warehouse_id.partner_id.axx_gln",  # ILNLIEFERANSCHRIFT
            # None,                                               # ILNRECHNUNGSEMPFAENGER  # TODO TDB
            # None,                                               # KENNZEICHENWAEHRUNG
            "name",                                             # KUNDENAUFTRAGSNUMMER
            "date_planned",                                     # LIEFERDATUM
            # "date_approve",                                     # DATUMKUNDENAUFTRAG
            # None,                                               # VALUTADATUM
            "picking_type_id.warehouse_id.partner_id.name",     # NAME1LIEFERADRESSE
            # None,                                               # NAME2LIEFERADRESSE
            # None,                                               # NAME3LIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.street",   # STRASSELIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.zip",      # PLZLIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.city",     # ORTLIEFERADRESSE
            "picking_type_id.warehouse_id.partner_id.country_id.code",  # LANDLIEFERADRESSE
            {
                "order_line": [
                    'sequence',                                 # POSITIONSNUMMER
                    'product_qty',                              # BESTELLMENGE
                    'product_id.axx_gtin_vpe',                  # EAN
                    'product_id.axx_supplier_article_number',   # ARTIKELLIEFERANTENNUMMER
                    'product_id.name',                          # ARTIKELBESCHREIBUNG
                    # None,                                     # BESTELLMENGENEINHEIT
                    # None,                                     # NATURALRABATT
                    'state',                                    # STATUS
                    # None,                                     # USER_EDIDATENVERKEHR
                ]
            },
        ]