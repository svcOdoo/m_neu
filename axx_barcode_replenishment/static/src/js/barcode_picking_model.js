/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';

patch(BarcodePickingModel.prototype, '@axx_barcode_replenishment/js/barcode_picking_model', {

     async assignPicking() {
        const action = await this.orm.call(
            'stock.picking',
            'action_assign',
            [this.record.id],

        );
    }
});