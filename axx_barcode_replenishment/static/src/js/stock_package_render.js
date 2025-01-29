/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { useBus, useService } from "@web/core/utils/hooks";
import { bus } from 'web.core';
import { View } from "@web/views/view";

const { Component, useState, onWillStart, onWillUnmount, onMounted, onWillDestroy } = owl;
export class PackageSelectorDialog extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.dialogService = useService("dialog");
        this.notification = useService("notification");
        this.viewService = useService("view");
        this.packages = false;
        this.packageRef = false;
        this.packageState = useState({
            productInfo: false,
            packageInfo: false,
        });
        onWillStart(async () => {
        this.viewProps = {
            type: "form",
            context: this.props.context || {},
            resModel: "axx.standard.location.select.wizard",
            viewId: this.packageState.packageInfo = [].viewId || false,
            setParent: this,
            preventCreate: false,
            mode: "edit",
            preventEdit: false,

        };

        });
        onMounted(() => {
            this.props.BarcodeScan(this);

        });
        onWillDestroy(() => {
            bus.off('barcode_scanned', this, this.loadPackage);
            bus.off('barcode_scanned', this, this.createTransfer);
        });

        onWillUnmount(() => {
            bus.off('barcode_scanned', this, this.loadPackage);
            bus.off('barcode_scanned', this, this.createTransfer);

        });
    }

    async loadFormPackages(){
        await this.packageRef.model.root.save();
        const record = await this.packageRef.model.root.data;
        const packageInfo = await this.orm.call(
            "stock.quant.package", 'axx_get_package_info_form',
            [record.axx_product_id[0], record.axx_standard_location_id[0]],
        );
        const productInfo =  {
                    'product_id': record.axx_product_id[0],
                    'location_id': record.axx_standard_location_id[0],
                    'name': record.axx_product_id[1],
                    'location_name': record.axx_standard_location_id[1],
                    'fromVireRef': true,
                }
                this.packageState.productInfo = productInfo;
        if (packageInfo.length > 0){
            this.packageState.packageInfo = packageInfo;
        }
    }

    setPackageRef(child){
     this.packageRef = child;
    }

    reloadView(){
     this.packageState.packageInfo = false;
     this.packageState.productInfo = false;
    }

    range(start, end, step = 1) {
        if (end <= start && step > 0) {
            return [];
        }
        if (step === 0) {
            throw new Error("range() step must not be zero");
        }
        const length = Math.ceil(Math.abs((end - start) / step));
        const array = Array(length);
        for (let i = 0; i < length; i++) {
            array[i] = start + i * step;
        }
        return array;
    }

    async loadPackage (barcode){
        const productInfo = await this.orm.call(
            "stock.quant.package", 'axx_get_product_info',
            [barcode],
        );
        if (!productInfo.product_id){
            return this.notification.add(this.env._t("Scan a Product / Location"), {
                type: "danger",
                sticky: false,
            });
        }
        this.packageState.productInfo = productInfo;
        const packageInfo = await this.orm.call(
            "stock.quant.package", 'axx_get_package_info',
            [productInfo.product_id],
        );
        if (packageInfo.length > 0){
            this.packageState.packageInfo = packageInfo;
        }
    }

    selectPackage (ev) {
        $(ev.target).closest('td').toggleClass('package_active');
    }

    async createTransfer(ev, resID = false) {
        let selected_packages;
        if (!resID) {
            selected_packages = await $('input.package_grid_selected:checked').map(function () {
                return parseInt($(this).attr('id'));
            }).get();
        } else {
            selected_packages = [parseInt(resID)];
        }

        let location_dest_id = await $('input.location_dest_id:checked').map(function () {
            return parseInt($(this).attr('id'));
        }).get();

        if (!location_dest_id) {
            location_dest_id = false;
        }

        const picking = await this.orm.call(
            "stock.quant.package",
            'action_move_unpack',
            [selected_packages, location_dest_id]
        );

        if (!picking) {
            return this.notification.add(this.env._t("Transfer Failed"), {
                type: "danger",
                sticky: false,
            });
        } else if (this.props.OnSave) {
            await this.props.OnSave();
        }

        if (!resID && picking) {
            this.notification.add(this.env._t("Transfer Validated"), {
                type: "success",
                sticky: false,
            });
            return this.props.close();
        }

        return picking;
    }

    async clickOpenBarcode(ev){
        var checkbox = await $(ev.target).closest("td").find(".package_grid_selected");
        var checkboxId = checkbox.attr("id");
        const picking = await this.createTransfer(this, checkboxId);
        if (picking == true){
               this.notification.add(this.env._t("Transfer Validated"), {
                    type: "success",
                    sticky: false,
                });
                $(ev.target).closest('td').removeClass('package_active');
                $(ev.target).closest('td').addClass('package_done');
                checkbox.prop("checked", true);
        }
    }

}
PackageSelectorDialog.template = "axx_barcode_replenishment.PackageSelector";
PackageSelectorDialog.components = {Dialog, View};
