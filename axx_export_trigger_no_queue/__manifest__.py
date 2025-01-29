# -*- coding: utf-8 -*-
{
    'name': "Axxelia Export Trigger",
    'summary': """
    Axxelia Export Trigger
    """,
    'description': """
    Generate data export when defined fields on the tracked models change.
    Allow users to view the data to export and the status of the export: 
    There is a smart button on each tracked model where you can see the json data that will be sent out.
    
    Config Parameter: 'axxelia.export.language'. Is set by default to german, only the german field values will be 
    provided for export.
    
""",

    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Tools',
    'version': '16.0.1.0.3',
    'license': 'OPL-1',

    'depends': [
        # odoo
        'base',
        # oca
    ],
    "external_dependencies": {
    },

    'data': [
        # data
        'data/ir_config_parameter_data.xml',
        # 'data/groups.xml',
        # Security
        'security/ir.model.access.csv',
        # Report
        # views
        'views/axx_export/axx_data_export_views.xml',
        # wizards
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
