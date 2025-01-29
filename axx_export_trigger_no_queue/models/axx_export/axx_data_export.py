from odoo import api, fields, models, _


class AxxDataExport(models.Model):
    _name = 'axx.data.export'
    _description = 'Axx Data Export'
    _order = 'id desc'

    def axx_do_export(self):
        """
        TO OVERRIDE,
        Export Logic Here, e.g. REST API Calls
        """
        return True

    name = fields.Char(string='Name', readonly=True, required=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        readonly=True
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', _('New')),
            ('processing', _('To Send')),
            ('sent', _('Sent')),
            ('failed', _('Failed'))
        ],
        required=True,
        copy=False,
        default='new',
        readonly=True
    )
    axx_record_id = fields.Integer(string='Record ID', readonly=True, help='Record ID where the data is coming from.')
    axx_model = fields.Char(string='Model Name', readonly=True, index=True, help='Model where the data is coming from.')
    axx_data = fields.Text(string='Data', readonly=True, help='JSON data for the content to be sent.')

    axx_user_id = fields.Many2one(
        string='Triggered by User',
        comodel_name='res.users',
        readonly=True,
        help='The user who made the change in the record which triggered the generation of the export.'
    )
    axx_changed_fields = fields.Text(
        string='Changed Fields',
        readonly=True,
        groups='base.group_erp_manager',
        help='The fields which were changed that lead to the export trigger. '
             'Only Admins have access to this field, to prevent user rights violations.'
    )

    def axx_write_value_to_linked_record_field(self, field, value):
        self.env[self.axx_model].browse(self.axx_record_id).write({field: value})

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AxxDataExport, self).create(vals_list)
        for record in res:
            record.axx_export()
        return res

    def axx_export(self):
        self.ensure_one()
        company = self.company_id
        if company:
            export_recordset = self.with_company(company).with_context(company_id=company.id)
        else:
            export_recordset = self
        self.write({'state': 'processing'})
        export_recordset.axx_do_export()
        return True

    def action_axx_open_related_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self.axx_model,
            'res_id': self.axx_record_id,
            'view_mode': 'form',
            'target': 'current',
        }
