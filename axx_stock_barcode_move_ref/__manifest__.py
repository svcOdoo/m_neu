# -*- coding: utf-8 -*-

{
    'name': "Markant PID Wareneingang",
    'description': "Markant PID Wareneingang",
    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.2',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'stock_barcode',
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
        'views/stock/stock_move_line_views.xml',

        # reports

        # Menus
    ],
    'demo': [],
    'assets': {

    },
    'installable': True,
    'application': False,
}
