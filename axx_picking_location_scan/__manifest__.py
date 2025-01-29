# -*- coding: utf-8 -*-

{
    'name': "Axxelia Picking Location Scan Module",
    'description': """
    Each storage location has a barcode or check digit. When picking, the barcode or check digit of the location should be scanned to ensure that the correct product is picked
    """,
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.2',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
        'axx_partner_outgoing_location',
        'axx_stock_product_location',
    ],
    'data': [
        # data

        # Security

        # wizards

        # views
        'views/stock/stock_location_views.xml',
        'views/stock/stock_move_line_views.xml',
        'views/stock/stock_picking_views.xml',

        # reports

        # Menus

        # data
    ],
    'assets': {
        'web.assets_backend': [
            'axx_picking_location_scan/static/**/*',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
}
