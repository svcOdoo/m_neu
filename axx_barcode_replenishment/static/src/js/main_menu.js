/** @odoo-module **/

import  { MainMenu } from '@stock_barcode/main_menu';
import { useService } from "@web/core/utils/hooks";
import { PackageSelectorDialog } from '@axx_barcode_replenishment/js/stock_package_render'
import { patch } from 'web.utils';
import { bus } from 'web.core';

patch(MainMenu.prototype, '@axx_barcode_replenishment/main_menu', {

setup() {
        this._super(...arguments);
        this.dialogService = useService("dialog");
        this.actionService = useService("action");
        this.orm = useService("orm");

    },

onclickReplenishment() {
this.dialogService.add(PackageSelectorDialog, {
            mainView: true,
            context: this.props.context,
            BarcodeScan: (PackageSelector) => {
                bus.off('barcode_scanned', this, this._onBarcodeScanned);
                bus.on('barcode_scanned', PackageSelector, PackageSelector.loadPackage);
                },
        },{
        onClose: () => {
            bus.on('barcode_scanned', this, this._onBarcodeScanned)
            }
            })
        },

async onclickEinlagern() {
    const action = await this.orm.call(
                'stock.picking.type',
                'action_open_einlagern'
            );

    this.actionService.doAction(action);

        },

});