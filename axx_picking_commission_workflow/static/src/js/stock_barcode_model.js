/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';

const originalValidate = BarcodePickingModel.prototype.validate;

patch(BarcodePickingModel.prototype, '@axx_picking_commission_workflow/js/barcode_picking_model', {
    get axxCommissionWorkflow() {
        return this.record.picking_type_code && this.record.picking_type_code === 'internal';
    },
    get displayNeueTeButton() {
        return this.axxCommissionWorkflow;
    },
    get displayAbstellenButton() {
        return this.axxCommissionWorkflow;
    },
    get displayValidateButton() {
        // overwrite
        return !this.axxCommissionWorkflow;
    },

    get axxQtyEntered() {
        for (const line of this.pageLines) {
            if (line.qty_done > 0) {
                return true;
            }
        }
        return false;
    },

    get axxRequiresPackaging() {
        if (this.axxCommissionWorkflow) {
            for (const line of this.pageLines) {
                if (line.qty_done > 0 && !line.result_package_id) {
                    return true;
                }
            }
        }
        return false;
    },

    async _axxPutInPack(additionalContext = {}) {
        // todo we could probably use the base function
        const context = Object.assign({ barcode_view: true }, additionalContext);
        if (!this.groups.group_tracking_lot) {
            return this.notification.add(
                _t("To use packages, enable 'Packages' in the settings"),
                { type: 'danger'}
            );
        }
        await this.save();
        const result = await this.orm.call(
            this.params.model,
            'action_put_in_pack',
            [[this.params.id]],
            { context }
        );
        if (typeof result === 'object') {
            this.trigger('process-action', result);
        } else {
            this.trigger('refresh');
        }
    },

    async axxBackorderId(additionalContext = {}) {
        const context = Object.assign({ barcode_view: true }, additionalContext);
        const result = await this.orm.call(
            this.params.model,
            'axx_find_open_backorder',
            [[this.params.id]],
            { context }
        );
        return result;
    },

});
