{
    'name': 'Axx Basic Styles',
    'summary': 'Axx Basic Styles',
    'description': """
            This app include the custom styles over the base odoo.
        """,
    'category': 'custom',
    'version': '16.0.1.0.4',
    'author': 'axxelia GmbH',
    'website': 'http://www.axxelia.com',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'web',
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
        # Menus
        # Reports
        # Templates
    ],
    'assets': {
        'web.assets_backend': [
            'axx_basic_styles/static/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
