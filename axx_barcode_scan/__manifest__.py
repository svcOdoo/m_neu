{
    'name': 'Axx Barcode Scan',
    'summary': 'Axx Barcode Scan',
    'description': """
            This app include the custom features of Barcode APP
        """,
    'category': 'stock',
    'version': '16.0.1.0.5',
    'author': 'axxelia GmbH',
    'website': 'http://www.axxelia.com',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
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

    ],
    'data': [
        # Security
        # Wizards
        # Data
        # views
        'views/stock_picking_type.xml'
        # Menus
        # Reports
        # Templates
    ],
    'assets': {
        'web.assets_backend': [
            'axx_barcode_scan/static/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
