# -*- coding: utf-8 -*-

{
    'name': "Axxelia Picking commission workflow Module",
    'description': """
    The aim of this module is improve the user experience using the barcode app in the mobile.
    The user will select the picking and then the system is asking for package barcode and its type.
    """,
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.2.0.4',
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
        'axx_stock_product_location',
    ],
    'data': [
        # data

        # security
        'security/ir.model.access.csv',

        # wizards
        'wizards/axx_put_down_wizard_views.xml',
        

        # views
        'views/stock_picking_view.xml',

        # reports

        # Menus

        # data
    ],
    'assets': {
        'web.assets_backend': [
            'axx_picking_commission_workflow/static/**/*',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': True,
}
