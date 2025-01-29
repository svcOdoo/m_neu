{
    'name': 'OFR Picking Workflow',
    'summary': 'OFR Picking Workflow',
    'description': """
            This app include the feature related to special picking workflows.
        """,
    'category': 'custom',
    'version': '16.0.0.2',
    'author': 'openfellas GmbH',
    'website': 'http://www.openfellas.com',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale_stock',
        'stock_barcode',
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # EE
        # ---------------------
        # ---------------------
        # Thirdparty
        # ---------------------
        # ---------------------
        # Axxelia
        # ---------------------
        # ---------------------
        # PROJECT
        # ---------------------
        'axx_picking_commission_workflow'

    ],
    'data': [
        # Security
        # Wizards
        # Data
        'data/picking_type_data.xml',
        # views
        'views/stock/stock_picking_type_views.xml',
        'views/sale/sale_order_views.xml',
        'views/stock/stock_route_views.xml',
        'views/stock/stock_picking_views.xml',

        # Menus
        # Reports
        # Templates
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
