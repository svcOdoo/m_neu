from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

import os
import base64
import json
import csv

import fsspec


def find_available_filename(directory, base_filename):
    """Finds the next available filename by appending a version number."""
    version = 1
    filename = base_filename
    file_path = os.path.join(directory, filename)

    while os.path.exists(file_path):
        version += 1
        filename = f"{base_filename[:-4]}_v{version}.csv"  # Assuming base_filename ends with ".csv"
        file_path = os.path.join(directory, filename)

    return file_path


def convert_date_format(date_str):
    # Angenommen, date_str ist im Format YYYY-MM-DD
    parts = date_str.split('-')
    return parts[2] + parts[1] + parts[0]


class AxxDataExport(models.Model):
    _inherit = 'axx.data.export'

    axx_result = fields.Char(string='Result', readonly=True)
    axx_attachment_id = fields.Many2one('ir.attachment', string="Attachment", readonly=True)

    def axx_do_export(self):
        self.ensure_one()

        data_dict = json.loads(self.axx_data)
        if self.axx_model == 'purchase.order':
            res = self._axx_create_edi_csv_order(data_dict)
        else:
            raise ValidationError(_("Unexpected Model, please contact your Administrator!"))

        self.write({
            'state': 'sent',
            'axx_result': res or ''
        })
        return res

    @api.model
    def _axx_check_path(self, path):
        """Check access and create directories if they do not exist"""
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except PermissionError:
                error_message = f'No permission to access or create directory: {path}'
                raise ValidationError(error_message)
            except Exception as e:
                error_message = f'Failed to create directory: {path}. Error: {str(e)}'
                raise ValidationError(error_message)
        elif not os.path.isdir(path):
            error_message = f'The provided path is a file, not a directory: {path}'
            raise ValidationError(error_message)
        # Check for write permission
        if not os.access(path, os.W_OK):
            error_message = f'No write permission for directory: {path}'
            raise ValidationError(error_message)

    def _axx_create_edi_csv_order(self, data):
        headers = [
            "ILNLIEFERANT",             # Vendor ILN (International Location Number)
            "ILNKAEUFER",               # Buyer ILN
            "ILNLIEFERANSCHRIFT",       # Vendor delivery address ILN
            "ILNRECHNUNGSEMPFAENGER",   # ILN Invoice recipient
            "KENNZEICHENWAEHRUNG",      # Currency identifier
            "KUNDENAUFTRAGSNUMMER",     # Customer order number
            "DATUMKUNDENAUFTRAG",       # Date of customer order
            "LIEFERDATUM",              # Delivery date
            "VALUTADATUM",              # Valuta date (often the value date or payment due date)
            "NAME1LIEFERADRESSE",       # First line of delivery address (e.g., company name)
            "NAME2LIEFERADRESSE",       # Second line of delivery address (e.g., department)
            "NAME3LIEFERADRESSE",       # Third line of delivery address (e.g., additional info)
            "STRASSELIEFERADRESSE",     # Street for delivery address
            "PLZLIEFERADRESSE",         # Postal code for delivery address
            "ORTLIEFERADRESSE",         # City for delivery address
            "LANDLIEFERADRESSE",        # Country for delivery address
            "POSITIONSNUMMER",          # Position number (e.g., line item number in order)
            "BESTELLMENGE",             # Ordered quantity
            "EAN",                      # European Article Number (now known as International Article Number)
            "ARTIKELLIEFERANTENNUMMER", # Supplier's item number
            "ARTIKELBESCHREIBUNG",      # product description
            "BESTELLMENGENEINHEIT",     # Unit of ordered quantity (e.g., piece, box, etc.)
            "NATURALRABATT",            # Natural discount (if any)
            "STATUS",                   # Status of the order
            "USER_EDIDATENVERKEHR"      # User data for EDI (Electronic Data Interchange) traffic
        ]

        main_directory = self.env['ir.config_parameter'].sudo().get_param('axxelia.export.directory.main')
        self._axx_check_path(main_directory)
        filename = data.get('name') + '.csv'
        file_path = find_available_filename(main_directory, filename)

        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(headers)

            for idx, item in enumerate(data["order_line"], 1):
                date_approve = data["date_approve"]
                product_qty = item["product_qty"]
                packaging_qty = item.get("product_packaging_qty", 0)
                row = [
                    data["partner_id.axx_gln"],
                    data["company_id.partner_id.axx_gln"],
                    data["picking_type_id.warehouse_id.partner_id.axx_gln"],
                    "",
                    "EUR",
                    data["name"],
                    convert_date_format(data["date_planned"].split('T')[0]),
                    convert_date_format(date_approve.split('T')[0]) if date_approve else "",
                    "",
                    data["picking_type_id.warehouse_id.partner_id.name"],
                    "",
                    "",
                    data["picking_type_id.warehouse_id.partner_id.street"],
                    data["picking_type_id.warehouse_id.partner_id.zip"],
                    data["picking_type_id.warehouse_id.partner_id.city"],
                    data["picking_type_id.warehouse_id.partner_id.country_id.code"],
                    f"{idx:04}",  # item["sequence"], sequence field is default 10, use index instead.
                    product_qty if not packaging_qty else packaging_qty,
                    item["product_id.axx_gtin_vpe"],
                    item["product_id.axx_supplier_article_number"],
                    item["product_id.name"],
                    "Stk",
                    "",
                    "",
                    ""
                ]
                writer.writerow(row)

        with open(file_path, 'rb') as file:
            file_content = file.read()
            attachment = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(file_content),
                'res_model': self._name,
                'res_id': self.id,
            })
            self.axx_attachment_id = attachment.id
        self.axx_transfer_to_sftp(file_path, filename)

        return file_path

    def axx_transfer_to_sftp(self, file_path, filename):
        if not self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.enabled', False):
            return False
        try:
            sftp_host = self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.hostname')
            sftp_port = int(self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.port', 22))
            sftp_user = self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.username')
            sftp_password = self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.password')  # Alternatively, use a private key
            remote_directory = self.env['ir.config_parameter'].sudo().get_param('axxelia.sftp.server.remote_directory')

            if not all([sftp_host, sftp_port, sftp_user, sftp_password, remote_directory]):
                raise ValidationError(_("One or more SFTP configuration parameters are missing!"))

            # Create an SFTP filesystem instance
            fs = fsspec.filesystem('sftp', host=sftp_host, port=sftp_port, username=sftp_user, password=sftp_password)

            # Transfer the file
            with fs.open(f"{remote_directory}/{filename}", 'wb') as remote_file:
                with open(file_path, 'rb') as local_file:
                    remote_file.write(local_file.read())

        except Exception as e:
            raise ValidationError(f"Error while transferring file to SFTP: {str(e)}")
