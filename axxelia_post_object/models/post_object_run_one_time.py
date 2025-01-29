from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class PostObjectRunOneTime(models.Model):
    _name = 'post.object.run.one.time'
    _description = 'Post Object Run One Time'

    @api.model
    def create_ir_config_parameter(self, functions=[]):
        ir_config_parameter_env = self.env['ir.config_parameter']
        ran_functions = ir_config_parameter_env.search([
            ('key', '=', 'functions_run_one_time'),
            ])
        if ran_functions:
            ran_functions_model_data = self.env['ir.model.data'].search([
                ('res_id', '=', ran_functions.id),
                ('model', '=', 'ir.config_parameter'),
            ])
            if ran_functions_model_data:
                ran_functions_model_data.module = 'axxelia_post_object'
                ran_functions_model_data.name = 'functions_run_one_time'
        else:
            ir_config_parameter_env.create({
                'key': 'functions_run_one_time',
                'value': [],
            })
        return True

    @api.model
    def func_run_one_time(self, object_name, functions=[]):
        ir_config_parameter_env = self.env['ir.config_parameter']
        try:
            post_object_env = self.env[object_name]
        except Exception as e:
            _logger.warning("Could not create a env for object %s! Error message: %s" % (object_name, e))
            return False
        ran_functions = ir_config_parameter_env.get_param('functions_run_one_time', '[]')
        ran_functions = safe_eval(ran_functions)
        if not isinstance(ran_functions, list):
            ran_functions = []
        if isinstance(functions, str):  # @UndefinedVariable
            functions = [functions]
        if not functions \
                or not isinstance(functions, list):
            _logger.warning('Invalid value of parameter list_functions.\
                                    Exiting...')
            return False
        for function in functions:
            if (object_name + ':' + function) in ran_functions:
                continue
            getattr(post_object_env, function)()
            ran_functions.append(object_name + ':' + function)
        if ran_functions:
            ir_config_parameter_env.set_param('functions_run_one_time', ran_functions)
        return True
