# -*- coding: utf-8 -*-

{
    'name': "Markant Product Attributes",
    'description': "Markant Product Attributes",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.0',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'product',
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

        # reports

        # Menus
    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [
            'axx_markant_product_attributes/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
