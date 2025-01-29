# -*- coding: utf-8 -*-

{
    'name': "Axxelia Stock Commission Routes",
    'description': """
    The order of operations in picking must follow the locations along the aisles in the warehouse, and must be manually adjustable.
    The goal is to not have to run "back and forth" during picking.

    Note:
        - Standard Location and Reserve Location are in the same place, so there is no need to distinguish between goods receipt and warehouse out.
        - The sequence of the operations in the picking follows the sequence of the Standard Location of the products. It is grouped according to the parent location.
          Example: Aisle A and Aisle B each have 100 locations with sequence 1-100. In Picking, all locations from Aisle A come first, then Aisle B.
    """,
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.4',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
        'axx_stock_product_location',
    ],
    'data': [
        # data

        # Security

        # wizards

        # views
        'views/stock/stock_location_views.xml',
        'views/stock/stock_move_line_views.xml',
        'views/stock/stock_picking_views.xml',

        # reports

        # Menus

        # data
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
