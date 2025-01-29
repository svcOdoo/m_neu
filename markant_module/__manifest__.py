# -*- coding: utf-8 -*-

{
    'name': "Markant Module",
    'description': "Markant Project Module",
    'author': "axxelia GmbH",
    'website': "www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.3.7',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale_management',
        'contacts',
        'stock',
        'purchase',
        'stock_barcode',
        'product_expiry',
        'base_import',
        'delivery',
        'delivery_stock_picking_batch',
        'auth_password_policy',
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
        'axx_markant_delivery',
        'axx_stock_product_location',
        'axx_stock_commission_routes',
        # 'axx_stock_load_aid',
        'axx_stock_load_carrier',
        'axx_picking_location_scan',
        'axx_markant_product_attributes',
        'axx_stock_barcode_move_ref',
        'axx_barcode_scan',
        'axx_basic_styles',
        'markant_edi_export',
        'axx_split_list_records',
        'axxelia_post_object',
    ],
    'data': [
        # data

        # Security
        'security/ir.model.access.csv',

        # wizards
        'wizards/axx_stock_move_line_wizard_views.xml',
        'wizards/axx_stock_move_line_pid_pack_wizard_views.xml',

        # views
        'views/base/res_partner_views.xml',

        'views/stock/stock_move_line_views.xml',
        'views/stock/stock_location_views.xml',
        'views/stock/stock_picking_views.xml',

        'views/purchases/purchase_order_views.xml',

        # reports
        'report/stock_report_deliveryslip.xml',
        'report/purchase_order_templates.xml',

        # Menus
        'views/stock/stock_menus.xml',
        # data
        'data/ir_sequence_data.xml',
        'data/init_call.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'markant_module/static/src/**/*.js',
            'markant_module/static/src/**/*.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'pre_init_hook': '_enable_german'
}
