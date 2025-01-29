# -*- coding: utf-8 -*-

{
    'name': "Axxelia Stock Product Module",
    'description': """
    Each product is assigned a standard storage location and a reserve storage location. At goods receipt, the product is posted to the reserve storage location.
    At warehouse out - or at picking/comminioning - the products are always taken from the same standard storage location.
    09.02.2023 - Anoop - Change in stock move lines destination location readonly attribute 
    to manually add the loading aid product
    """,
    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.10',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'stock',
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
    ],
    'data': [
        # data

        # Security

        # wizards

        # views
        'views/product/product_template_views.xml',
        'views/product/product_product_views.xml',

        'views/stock/stock_move_line_views.xml',
        'views/stock/stock_picking_views.xml',

        # reports

        # Menus

        # data
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
