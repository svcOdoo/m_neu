.. code-block:: rst
AxxDataExport and AxxExportDataSource in Odoo

The provided Odoo module is primarily designed for managing data exports.
It is particularly useful when you need to export data from various Odoo models to an external system.
The module defines two classes:

    AxxDataExport
    AxxExportDataSource

AxxDataExport

This class serves as the principal manager of the data export process. Key components include:

    axx_data: This field stores JSON-formatted data that is set to be exported.
    It acts as the central repository for the data extracted from the source model.

    axx_do_export: This method is where the actual export logic is executed.
    It is supposed to be overridden in subclasses or extended module

AxxExportDataSource

This abstract class is intended to be inherited by other Odoo models that necessitate data export.
The class introduces several methods and fields associated with data export. Key components include:

    axx_fields_to_export: This method is designed to be overridden in subclasses and should return a list of fields to be exported.

    axx_data_export_name: Another method planned for overriding, which should return a name for the export operation.

    _axx_create_data_export_record: This method creates an AxxDataExport record,
    which includes data extraction from the current record, formatting it into JSON, and storing it in the axx_data field.

In the create and write methods of the AxxExportDataSource model, the module checks whether the axx_is_export flag is
active or if any of the fields ready for export have been modified. If either condition holds,
the _axx_create_data_export_record method is called to create a new AxxDataExport record,
subsequently triggering the export process.

Purpose

The primary purpose of this module is to provide a generalized framework for exporting data from different Odoo models.
It facilitates export operations and maintains a record of these operations' states.
