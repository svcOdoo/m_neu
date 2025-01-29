/** @odoo-module **/

import LazyBarcodeCache from '@stock_barcode/lazy_barcode_cache';

import { patch } from 'web.utils';

patch(LazyBarcodeCache.prototype, '@axx_picking_location_scan/js/lazy_barcode_cache', {

    setCache(cacheData) {
        for (const model in cacheData) {
            const records = cacheData[model];
            // Adds the model's key in the cache's DB.
            if (!this.dbIdCache.hasOwnProperty(model)) {
                this.dbIdCache[model] = {};
            }
            if (!this.dbBarcodeCache.hasOwnProperty(model)) {
                this.dbBarcodeCache[model] = {};
            }
            // Adds the record in the cache.
            const barcodeField = this._getBarcodeField(model);
            for (const record of records) {
                this.dbIdCache[model][record.id] = record;
                // Start Axxelia Adjustment
                let axxIsPicking;
                if (this.dbBarcodeCache["stock.picking"]) {
                    axxIsPicking = this.dbBarcodeCache["stock.picking"];
                }
                if (model === 'stock.location' && record.axx_picking_location_scan === 'check_digit' && axxIsPicking) {
                    var locationbarcodeField = 'axx_check_digit';
                    if (locationbarcodeField) {
                        const barcode = record[locationbarcodeField];
                        if (!this.dbBarcodeCache[model][barcode]) {
                            this.dbBarcodeCache[model][barcode] = [];
                        }
                        if (!this.dbBarcodeCache[model][barcode].includes(record.id)) {
                            this.dbBarcodeCache[model][barcode].push(record.id);
                            if (this.nomenclature && this.nomenclature.is_gs1_nomenclature && this.gs1LengthsByModel[model]) {
                                this._setBarcodeInCacheForGS1(barcode, model, record);
                            }
                        }else{
                            let move_lines = cacheData['stock.move.line']
                            if (move_lines && move_lines.length){
                                const hasMatchingElement = move_lines.some(item =>
                                  item.result_package_id && item.location_id === record.id
                                );
                                if(hasMatchingElement){
                                    const barcodeCache = this.dbBarcodeCache[model][barcode];
                                    const indexToRemove = barcodeCache.indexOf(record.id);
                                    if (indexToRemove !== -1) {
                                      barcodeCache.splice(indexToRemove, 1);
                                      }
                                }

                            }
                        }
                    }
                }
                // End Axxelia Adjustment
                else {
                    if (barcodeField) {
                        const barcode = record[barcodeField];
                        if (!this.dbBarcodeCache[model][barcode]) {
                            this.dbBarcodeCache[model][barcode] = [];
                        }
                        if (!this.dbBarcodeCache[model][barcode].includes(record.id)) {
                            this.dbBarcodeCache[model][barcode].push(record.id);
                            if (this.nomenclature && this.nomenclature.is_gs1_nomenclature && this.gs1LengthsByModel[model]) {
                                this._setBarcodeInCacheForGS1(barcode, model, record);
                            }
                        }
                    }
                }
            }
        }
    }
});