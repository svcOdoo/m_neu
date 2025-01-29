/** @odoo-module **/

import MainComponent from '@stock_barcode/components/main';
import { PackageSelectorDialog } from '@axx_barcode_replenishment/js/stock_package_render'
import { useService } from "@web/core/utils/hooks";
import { bus } from 'web.core';

import { patch } from 'web.utils';

patch(MainComponent.prototype, 'axx_barcode_replenishment/barcode_main', {

setup() {
        this._super(...arguments);
        this.dialogService = useService("dialog");

    },

clickReplenish (){
    this.dialogService.add(PackageSelectorDialog, {
            mainView: true,
            context: this.props.context,
            BarcodeScan: (PackageSelector) => {
                bus.off('barcode_scanned', this, this._onBarcodeScanned);
                bus.on('barcode_scanned', PackageSelector, PackageSelector.loadPackage);
                },
            OnSave: async () => {
                await this.env.model.assignPicking();
                await this.env.model.trigger('refresh');
                                 }
        },{
        onClose: () => {
            bus.on('barcode_scanned', this, this._onBarcodeScanned)
            }
            })
},


});