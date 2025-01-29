# -*- coding: utf-8 -*-

{
    'name': "Axxelia Partner Outgoing Location",
    'description': "Axxelia Partner Outgoing Location",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.2',
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
        'views/base/res_partner_views.xml',

        'views/stock/stock_location_views.xml',

        # reports

        # Menus
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
