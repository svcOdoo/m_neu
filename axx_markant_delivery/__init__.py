from . import models

from odoo.api import Environment, SUPERUSER_ID


def _update_warehouse_delivery_step(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    warehouse_ids = env['stock.warehouse'].search([])
    warehouse_ids and warehouse_ids.write({'delivery_steps': 'pick_pack_ship'})
