from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import json
import datetime
import operator


OP_MAPPING = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    'in': lambda a, b: a in b,
}


def axx_filter_by_domain(records, domain):
    filtered_records = records
    for condition in domain:
        field, operation, value = condition
        op_func = OP_MAPPING.get(operation)
        if op_func:
            filtered_records = filtered_records.filtered(lambda r: op_func(getattr(r, field), value))
    return filtered_records


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


class AxxExportDataSource(models.AbstractModel):
    _name = 'axx.export.data.source'
    _description = 'Axx Export Data Source'

    axx_is_export = fields.Boolean(
        string='Is Export?',
        copy=False,
    )
    axx_export_count = fields.Integer(string='Export Count', compute='_compute_axx_export_count')

    @api.model
    def axx_fields_to_export(self):
        """
        OVERRIDE THIS IN INHERITANCE
        list of field names, dict is also allowed for one2many fields. many2one fields can be accessed with ".":
        ["code", "product_id.name", {"bom_line_ids": ["product_id.default_code", "product_qty"]}]
        if the one2many construct is used, you need to add: # noinspection PyTypeChecker
        """
        return []

    @api.model
    def axx_fields_export_trigger(self):
        """
        OVERRIDE THIS IN INHERITANCE
        fields which need to change in order for the export data to be generated.
        """
        return []

    @api.model
    def axx_fields_export_trigger_domain(self):
        """
        OVERRIDE THIS in inheritance
        optional condition which needs to be fulfilled, otherwise the export data will not be generated.
        use odoo domain format
        """
        # e.g.[('state', 'in', ['purchase', 'done', 'cancel'])]
        return []

    @api.model
    def axx_required_fields_for_export(self):
        """
        OVERRIDE THIS IN INHERITANCE
        It returns a list of fields required for export. The list may contain
        field names as strings for simple fields, and dictionaries for one2many fields.
        Each dictionary should map a one2many field name to a list of its subfields that are needed for the export.

        raise an error in @api.onchange of field axx_is_export if a required field is not set.
        raise an error if users try to save the record with missing required data when axx_is_export is true.

        does not catch if the one2many / many2one records are changed.
        """
        return []

    def axx_data_export_name(self):
        # is not @api.model because it might depend on self in inheritance
        """OVERRIDE THIS IN INHERITANCE
        """
        return "Placeholder"

    @api.model
    def axx_split_export_fields(self, field_list):
        """
        This function separates the list of fields returned by get_fields_for_export
        into two lists: one for simple fields (strings) and one for one2many fields (dictionaries).

        :return: two lists:
            1. A list of strings, each being a name of a simple field or many2one.
            2. A list of dictionaries, each mapping a one2many field name to a list of its subfields.
        """
        simple_fields = []
        one2many_fields = []

        for field in field_list:
            if isinstance(field, str):
                simple_fields.append(field)
            elif isinstance(field, dict):
                one2many_fields.append(field)
            else:
                raise ValidationError(_("Unexpected list element, please contact your Administrator"))

        return simple_fields, one2many_fields

    def __axx_required_field_export_validation_message(self, missing_fields):
        missing_fields_str = ', '.join(f'{field_desc} ({field_name})' for field_name, field_desc in missing_fields)
        return missing_fields_str

    @api.onchange('axx_is_export')
    def _axx_check_required_fields_export(self):
        required_fields = self.axx_required_fields_for_export()
        simple_fields, one2many_fields = self.axx_split_export_fields(required_fields)

        if self.axx_is_export:
            # Check simple fields
            missing_fields = [(field_name, self._axx_get_field_string(field_name, self)) for field_name in simple_fields if
                              not self._axx_read_field(self, field_name)]
            if missing_fields:
                missing_fields_str = self.__axx_required_field_export_validation_message(missing_fields)
                raise ValidationError(_("Required field for export is not set: %s!") % missing_fields_str)

            # Check one2many fields
            for one2many_field in one2many_fields:
                field_name = list(one2many_field.keys())[0]
                subfields = one2many_field[field_name]
                if not self[field_name]:
                    field_string = self._axx_get_field_string(field_name, self)
                    raise ValidationError(_("No records found in one2many field: %s (%s)."
                                            " Please add at least one record.") % (field_string, field_name))

                for record in self[field_name]:
                    missing_subfields = [(subfield, self._axx_get_field_string(subfield, record)) for subfield in subfields if
                                         not self._axx_read_field(record, subfield)]
                    if missing_subfields:
                        missing_fields_str = self.__axx_required_field_export_validation_message(missing_subfields)
                        raise ValidationError(_("Required subfield for export is not set in one of the records: "
                                                "'%s'.\n\nMissing field: %s!")
                                              % (record.display_name, missing_fields_str))

    def _get_axx_export_domain(self):
        domain = [('axx_model', '=', self._name), ('axx_record_id', '=', self.id)]
        if self.company_id:
            domain.append(('company_id', '=', self.company_id.id))
        return domain

    def _compute_axx_export_count(self):
        data_export_env = self.env['axx.data.export']
        for record in self:
            record.axx_export_count = data_export_env.search_count(self._get_axx_export_domain())

    @api.model
    def _axx_export_language_code(self):
        ir_config_parameter = self.env['ir.config_parameter']
        language_code = ir_config_parameter.sudo().get_param('axxelia.export.language')
        if not language_code:
            return 'de_DE'
        return language_code

    @api.model
    def _axx_read_field(self, record, field_name, lang='de_DE'):
        axx_fields = field_name.split('.')
        current_record = record.with_context(lang=lang)

        for field in axx_fields:
            current_record = current_record[field]

        return current_record

    @api.model
    def _axx_get_field_string(self, field_name, current_model):
        # Splitting the field by dots for traversal
        axx_fields = field_name.split('.')
        field_strings = []

        for field in axx_fields:
            # Appending the string representation of the field to the list
            field_strings.append(current_model._fields[field].string)

            # If it's not the last field, update the model to its related model
            if field != axx_fields[-1]:
                current_model = self.env[current_model._fields[field].comodel_name]

        # Join the strings with a '#'
        return "#".join(field_strings)

    def _axx_create_data_export_record(self, fields_to_export, lang, changed_fields):
        company_id = False
        if 'company_id' in self._fields:
            company_id = self.company_id.id or False
        export_data = {
            'name': self.axx_data_export_name(),
            'company_id': company_id,
            'axx_record_id': self.id,
            'axx_model': self._name,
            'axx_user_id': self.env.user.id,
            'axx_changed_fields': json.dumps(changed_fields, indent=4, cls=DateTimeEncoder),
        }
        export_data_content = {}
        simple_fields, one2many_fields = self.axx_split_export_fields(fields_to_export)
        for field_name in simple_fields:
            if isinstance(field_name, str):
                export_data_content[field_name] = self._axx_read_field(self, field_name, lang=lang)
        for field_name in one2many_fields:
            dict_name = list(field_name.keys())[0]
            export_data_content[dict_name] = []
            for record in self.with_context(lang=lang)[dict_name]:
                record_dict = {}
                for fn in field_name[dict_name]:
                    record_dict[fn] = self._axx_read_field(record, fn, lang=lang)
                export_data_content[dict_name].append(record_dict)

        export_data['axx_data'] = json.dumps(export_data_content, indent=4, cls=DateTimeEncoder)
        export_record = self.env['axx.data.export'].sudo().create(export_data)
        return export_record

    @api.model_create_multi
    def create(self, vals_list):
        created_records = super(AxxExportDataSource, self).create(vals_list)

        fields_to_export = self.axx_fields_to_export()
        lang = self._axx_export_language_code()
        export_trigger_domain = self.axx_fields_export_trigger_domain()
        if export_trigger_domain:
            filtered_records = axx_filter_by_domain(created_records, export_trigger_domain)
        else:
            filtered_records = created_records
        for record in filtered_records.filtered(lambda x: x.axx_is_export):
            record._axx_check_required_fields_export()
            record._axx_create_data_export_record(fields_to_export, lang, vals_list)

        return created_records

    def write(self, values):
        do_export = False
        fields_export_trigger = self.axx_fields_export_trigger()
        if ('axx_is_export' in values and values['axx_is_export']) \
                or any(field in fields_export_trigger for field in values):
            do_export = True

        res = super(AxxExportDataSource, self).write(values)

        if do_export and self.axx_is_export:
            export_trigger_domain = self.axx_fields_export_trigger_domain()
            if not export_trigger_domain or axx_filter_by_domain(self, export_trigger_domain):
                self._axx_check_required_fields_export()
                self._axx_create_data_export_record(
                    self.axx_fields_to_export(), self._axx_export_language_code(), values)
        return res

    def action_view_axx_exports(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Axx Exports',
            'res_model': 'axx.data.export',
            'view_mode': 'tree,form',
            'domain': self._get_axx_export_domain()
        }
