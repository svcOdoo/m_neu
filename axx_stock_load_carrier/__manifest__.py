# -*- coding: utf-8 -*-

{
    'name': "Axxelia Stock Load Module",
    'description': """
    In order to track the package and loading equipment charges in sale order
    Configuration:
    1. Loading aid product checkbox should be enabled in product record
    2. This loading aid product should be configured in package types
    3. When assigning the package type to a package, the loading aid product will be added to the corresponding sale order
    """,
    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.2',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale',
        'stock',
        'delivery',
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
        'views/stock/stock_package_type_views.xml',
        # reports
        # Menus
        # data
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
