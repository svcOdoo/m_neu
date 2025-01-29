{
    'name': 'Axx Split List View Records',
    'summary': 'Axx Split List View Records',
    'description': """
            This app include the feature to split the list view records.
        """,
    'category': 'custom',
    'version': '16.0.1.0.3',
    'author': 'axxelia GmbH',
    'website': 'http://www.axxelia.com',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'web',
        'stock'
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
        'security/ir.model.access.csv',
        # Wizards
        'wizards/axx_split_record.xml',
        # Data
        'data/axx_split_limit_data.xml',
        # views
        'views/stock_picking_views.xml',
        # Menus
        # Reports
        # Templates
    ],
    'assets': {
        'web.assets_backend': [
            'axx_split_list_records/static/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
