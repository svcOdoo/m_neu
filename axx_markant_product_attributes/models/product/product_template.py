# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    axx_abc_classification_article = fields.Char(string="ABC Classification Article")               # ABC Klassifizierung Artikel
    axx_hull_range_classification = fields.Char(string="Hull Range Classification")                 # Klassifizierung Rumpfsortiment
    axx_supplier_article_number = fields.Char(string="Supplier Article Number")                     # Lieferantenartikelnummer
    axx_trading_partner_supplier_number = fields.Char(string="Trading Partner Supplier No.")        # Lieferanten-Nr. Handelspartner
    axx_trading_partner_article_number = fields.Char(string="Trading Partner Article No.")          # Artikelnummer Handelspartner
    axx_gtin_single_piece = fields.Char(string="GTIN Single Piece")                                 # GTIN Einzelstück
    axx_gtin_vpe = fields.Char(string="GTIN VPE")                                                   # GTIN VPE
    axx_qty_per_vpe = fields.Float(string="Content / Quantity per VPE")                             # Inhalt / Menge pro VPE
    axx_purchase_unit = fields.Char(string="Purchase Unit")                                         # Einkaufseinheit
    axx_sales_unit = fields.Char(string="Sales Unit")                                               # Verkaufseinheit
    axx_layer_factor_vpe = fields.Char(string="Layer Factor in VPE")                                # Lagenfaktor in VPE
    axx_pallet_factor_vpe = fields.Char(string="Pallet Factor in VPE")                              # Palettenfaktor in VPE
    axx_min_purchase_qty_vpe = fields.Char(string="Minimum Purchase Quantity in VPE")               # Mindestabnahmemenge in VPE
    axx_order_quantity = fields.Float(string="Ø Order Quantity")                                    # Ø Bestellmenge
    axx_qty_sold_per_week = fields.Float(string="Quantity Sold per Week")                           # Abverkaufsmenge pro Woche
    axx_delivery_type = fields.Char(string="Delivery Type (Route / ZL)")                            # Lieferart (Strecke / ZL)
    axx_material_group = fields.Char(string="Material Group")                                       # Warenunterfach / Warengruppe
