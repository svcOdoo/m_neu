# -*- coding: utf-8 -*-

{
    'name': "Axxelia Stock Load Module",
    'description': """
    In order to track the package and loading equipment charges in sale order
    Configuration:
    1. Loading aid product checkbox should be enabled in product record
    2. While adding the loading aid product in delivery order line, the same loading aid product will be added to 
    the corresponding sale order
    """,
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.3',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale',
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
        # 'views/product/product_template_views.xml',

        # reports

        # Menus

        # data
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
