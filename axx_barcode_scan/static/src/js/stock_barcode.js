/** @odoo-module **/

import {MainMenu} from '@stock_barcode/main_menu';
import { patch } from 'web.utils';
import MainComponent from '@stock_barcode/components/main';

patch(MainMenu.prototype, '@axx_barcode_scan/js/stock_barcode', {

    async applyBarcode() {
        const barcode = await $('input.manual_text_barcode').val();
        $('input.manual_text_barcode').val('');
        if (barcode){
            this._onBarcodeScanned(barcode);
            if ('vibrate' in window.navigator) {
                window.navigator.vibrate(100);
            }
        }
    },

    onBarcodeKeypress(event) {
        if (event.key !== 'Enter') {
            return;
        }
        this.applyBarcode();
    }
});

patch(MainComponent.prototype, '@axx_barcode_scan/js/stock_barcode', {

    toggleManualBarcode() {
        $('input.manual_text_barcode').toggle();

    },

    async applyBarcode() {
        const barcode = await $('input.manual_text_barcode').val();
        $('input.manual_text_barcode').val('');
        if (barcode){
            this._onBarcodeScanned(barcode);
            if ('vibrate' in window.navigator) {
                window.navigator.vibrate(100);
            }
        }
    },

    onBarcodeKeypress(event) {
        if (event.key !== 'Enter') {
            return;
        }
        this.applyBarcode();
    }
});
