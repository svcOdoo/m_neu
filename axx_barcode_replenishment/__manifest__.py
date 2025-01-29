# -*- coding: utf-8 -*-
{
    'name': 'Barcode for Replenishment',
    'summary': "Add replenishment into the barcode view",
    'description': "",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.4',
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
        'markant_module',
        'stock_barcode',
        'axx_stock_product_location',
    ],
    'data': [
        # data

        # security
        'security/ir.model.access.csv',

        # wizards
        'wizards/axx_standard_location_select_wizard.xml',
        

        # views
        'views/stock_barcode_picking.xml',


        # reports

        # Menus

        # data
    ],
    'assets': {
        'web.assets_backend': [
            'axx_barcode_replenishment/static/src/**/*',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': True,

}
