from . import models
from . import wizards

from odoo.api import Environment, SUPERUSER_ID


def _enable_german(cr):
    env = Environment(cr, SUPERUSER_ID, {})
    env['res.lang']._activate_lang('de_DE')
