# -*- coding: utf-8 -*-
{
    'name': "Markant EDI Export",
    'summary': """
    Markant EDI Export
    """,
    'description': """
    Create EDI CSV Files when a purchase order is confirmed
    
""",

    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Tools',
    'version': '16.0.2.0.1',
    'license': 'OPL-1',

    'depends': [
        # odoo
        'base',
        'purchase',
        # project
        'axx_export_trigger_no_queue'
    ],
    "external_dependencies": {"python": ["fsspec"]},

    'data': [
        # data
        'data/ir_config_parameter_data.xml',
        # 'data/groups.xml',
        # Security
        # Report
        # views
        'views/axx_export/axx_data_export_views.xml',
        'views/purchase/purchase_order_views.xml',
        # wizards
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
