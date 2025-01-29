/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { _t, _lt } from "web.core";
import { sprintf } from '@web/core/utils/strings';
import { session } from '@web/session';
import { patch } from 'web.utils';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(BarcodePickingModel.prototype, 'markant_module_picking_model', {
    // OVERWRITE
    constructor(params) {
        this._super(...arguments);
        this.dialogService = useService('dialog');
    },
    // OVERWRITE
    lineCanBeSelected(line) {
        if (this.selectedLine && this.selectedLine.virtual_id === line.virtual_id) {
            return true; // We consider an already selected line can always be re-selected.
        }
        // START CHANGED BY AXXELIA
        // can select line if we need to edit it to access the "zubuchen" button
        let zubuchen_forbidden = false;
        if (line.location_id) {
            zubuchen_forbidden = line.location_id.name === line.axx_standard_location_name;
        }
        // by default, we want to be able to edit lines if the location does not match the standard location,
        // so that we can use the "zubuchen" button. after zubuchen is done, standard logic applies again.
        if (zubuchen_forbidden && this.config.restrict_scan_source_location && !line.qty_done && (!this.lastScanned.sourceLocation || this.lastScanned.sourceLocation.barcode !== line.location_id.barcode)) {
            return false; // Can't select a line if source is mandatory and wasn't scanned yet or if lastScanned sourceLocation does not equal line.location_id.
        }

        // END CHANGED BY AXXELIA
        if (line.isPackageLine) {
            // The next conditions concern product, skips them in case of package line.
            // return super.lineCanBeSelected(...arguments);
            // ADJUSTED BY AXXELIA due to overwrite, package line must always be editable
            return true
        }
        const product = line.product_id;
        if (this.config.restrict_put_in_pack === 'mandatory' && this.selectedLine &&
            this.selectedLine.qty_done && !this.selectedLine.result_package_id &&
            this.selectedLine.product_id.id != product.id) {
            return false; // Can't select another product if a package must be scanned first.
        }
        if (this.config.restrict_scan_product && product.barcode) {
            // If the product scan is mandatory, a line can't be selected if its product isn't
            // scanned first (as we can't keep track of each line's product scanned state, we
            // consider a product was scanned if the line has a qty. greater than zero).
            if (product.tracking === 'none' || !this.config.restrict_scan_tracking_number) {
                return !this.getQtyDemand(line) || this.getQtyDone(line) || (
                    this.lastScanned.product && this.lastScanned.product.id === line.product_id.id
                );
            } else if (product.tracking != 'none') {
                return line.lot_name || (line.lot_id && line.qty_done);
            }
        }
        // START CHANGED BY AXXELIA
        return true;
        // END CHANGED BY AXXELIA
    },
    // OVERWRITE
    _sortingMethod(l1, l2) {
        // AXX: COPIED FROM BarcodePickingModel
        const l1IsCompleted = this._lineIsComplete(l1);
        const l2IsCompleted = this._lineIsComplete(l2);
        // Complete lines always on the bottom.
        if (!l1IsCompleted && l2IsCompleted) {
            return -1;
        } else if (l1IsCompleted && !l2IsCompleted) {
            return 1;
        }
        // AXX: START ADDED BY AXXELIA
        // sort by standard location first
        const sourceLocationSequence1 = l1.product_id.axx_standard_location_full_seq;
        const sourceLocationSequence2 = l2.product_id.axx_standard_location_full_seq;
        if (sourceLocationSequence1 < sourceLocationSequence2) {
            return -1;
        } else if (sourceLocationSequence1 > sourceLocationSequence2) {
            return 1;
        }
        // AXX: END ADDED BY AXXELIA
        // AXX: COPIED FROM BarcodeModel
        // Sort by source location.
        const sourceLocation1 = l1.location_id.display_name;
        const sourceLocation2 = l2.location_id.display_name;
        if (sourceLocation1 < sourceLocation2) {
            return -1;
        } else if (sourceLocation1 > sourceLocation2) {
            return 1;
        }
        // Sort by (source) package.
        const package1 = l1.package_id.name;
        const package2 = l2.package_id.name;
        if (package1 < package2) {
            return -1;
        } else if (package1 > package2) {
            return 1;
        }
        // Sort by destination location.
        if (l1.location_dest_id && l2.location_dest_id) {
            const destinationLocation1 = l1.location_dest_id.display_name;
            const destinationLocation2 = l2.location_dest_id.display_name;
            if (destinationLocation1 < destinationLocation2) {
                return -1;
            } else if (destinationLocation1 > destinationLocation2) {
                return 1;
            }
        }
        // Sort by result package.
        if (l1.result_package_id && l2.result_package_id) {
            const resultPackage1 = l1.result_package_id.name;
            const resultPackage2 = l2.result_package_id.name;
            if (resultPackage1 < resultPackage2) {
                return 1;
            } else if (resultPackage1 > resultPackage2) {
                return -1;
            }
        }
        // Sort by product's category.
        const categ1 = l1.categ_id;
        const categ2 = l2.categ_id;
        if (categ1 < categ2) {
            return -1;
        } else if (categ1 > categ2) {
            return 1;
        }
        // Sort by product's display name.
        const product1 = l1.product_id.display_name;
        const product2 = l2.product_id.display_name;
        if (product1 < product2) {
            return -1;
        } else if (product1 > product2) {
            return 1;
        }
        return 0;
    },
    // OVERWRITE
    async _putInPack(additionalContext = {}) {
        const context = Object.assign({ barcode_view: true }, additionalContext);
        if (!this.groups.group_tracking_lot) {
            return this.notification.add(
                _t("To use packages, enable 'Packages' in the settings"), { type: 'danger' }
            );
        }
        await this.save();
        // Start Axxelia Adjustment
        const useDummyLot = await this.orm.call(
            this.params.model,
            'check_use_dummy_lot', [
                [this.params.id]
            ], { context }
        );
        if (useDummyLot) {
            const params = {
                title: _t("Use Dummy Lot?"),
                body: _t("You did not assign Lot Numbers to some moves. Would you like to use dummy lot numbers?"),
                confirm: async() => {
                    const result = await this.orm.call(
                        this.params.model,
                        'action_use_dummy_lot', [
                            [this.params.id]
                        ], { context }
                    );
                    if (typeof result === 'object') {
                        this.trigger('process-action', result);
                    } else {
                        this.trigger('refresh');
                    }
                },
                cancel: () => {},
                confirmLabel: _t("Yes"),
                cancelLabel: _t("No"),
            };
            this.dialogService.add(ConfirmationDialog, params);
        } else {
            const result = await this.orm.call(
                this.params.model,
                'action_put_in_pack', [
                    [this.params.id]
                ], { context }
            );
            if (typeof result === 'object') {
                this.trigger('process-action', result);
            } else {
                this.trigger('refresh');
            }
        }
        // End Axxelia Adjustment
    }
});