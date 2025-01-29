/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';

patch(BarcodePickingModel.prototype, 'markant_module', {

    async updateLine(line, args) {
        this._super(...arguments);
        if (args.expiration_date) {
            line.axx_reference = args.axx_reference;
        }
        if (args.axx_standard_location_name) {
            line.axx_standard_location_name = args.axx_standard_location_name;
        }
    },

    _convertDataToFieldsParams(args) {
        const params = this._super(...arguments);
        if (args.axx_reference) {
            params.axx_reference = args.axx_reference;
        }
        if (args.axx_standard_location_name) {
            params.axx_standard_location_name = args.axx_standard_location_name;
        }
        return params;
    },

    _getFieldToWrite() {
        const fields = this._super(...arguments);
        fields.push('axx_reference');
        fields.push('axx_standard_location_name');
        return fields;
    },

    _createCommandVals(line) {
        const values = this._super(...arguments);
        values.axx_reference = line.axx_reference;
        values.axx_standard_location_name = line.axx_standard_location_name;
        return values;
    },
});
