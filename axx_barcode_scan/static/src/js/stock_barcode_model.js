/** @odoo-module **/

import BarcodeModel from '@stock_barcode/models/barcode_model';

import { patch } from 'web.utils';

patch(BarcodeModel.prototype, '@axx_barcode_scan/js/stock_barcode_model', {

     async _parseBarcode(barcode, filters) {
        const sup = this._super;
        const nomenclature = await this.orm.call("stock.picking", "get_barcode_nomenclature", [[this.record.id]], {});
        if (nomenclature.length){
             this.parser.nomenclature_id = nomenclature;
             await this.parser.load();
        }
        const barcodeData = await sup(...arguments);
        return barcodeData;

    },
});