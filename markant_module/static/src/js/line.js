/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';
import { patch } from 'web.utils';

patch(LineComponent.prototype, 'markant_module', {
    get axxReference() {
        if (this.line) {
            return this.line.axx_reference || '';
        }
        return '';
    },
    get axxStandardLocationName() {
        if (this.line) {
            return !this.line.ofr_palette_picking && this.line.axx_standard_location_name || '';
        }
        return '';
    },
});