# -*- coding: utf-8 -*-

{
    'name': "Axxelia Markant Delivery Module",
    'description': """
When the sale order is confirmed, we need to create 3 pickings:
From WH/Stock (the default location for deliveries, take it from the default calculations) to WA-Bahn 
(Warehouse-out-location) the WA-Bahn needs to be taken from the delivery address of the sale order, 
field axx_outgoing_location_id. If the field axx_outgoing_location_id in the partner is not set when confirming the SO,
raise an error message
 
From WA-Bahn to pack location.

From the pack location to the customer location.
""",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'OPL-1',
    'version': '16.0.1.7',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale',
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
        'axx_partner_outgoing_location',
    ],
    'data': [
        # data
        # Security
        # wizards
        # views
        # reports
        # Menus
        # data
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'post_init_hook': '_update_warehouse_delivery_step'
}
