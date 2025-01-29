/** @odoo-module **/

import MainComponent from '@stock_barcode/components/main';
import { patch } from 'web.utils';
import { useService } from "@web/core/utils/hooks";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";


patch(MainComponent.prototype, '@axx_picking_commission_workflow/js/main', {
    setup() {
        this._super(...arguments);
        this.action = useService('action');
        this.dialogService = useService("dialog");
    },

    async loadNextAction() {
        const action = await this.orm.call(
            'stock.picking',
            'action_confirm_packaging',
            [this.props.id],
            { context: { open_record: false } }
        );
        return action;
    },

    loadPicking(picking_id) {
        // action = backorder_id.with_context(save_and_close=True).action_open_picking_client_action()
        const picking_action = {
            'res_id': picking_id,
            'name': 'Barcode Picking Client Action',
            'type': 'ir.actions.client',
            'xml_id': 'stock_barcode.stock_barcode_picking_client_action',
            'help': false,
            'binding_model_id': false,
            'binding_type': 'action',
            'binding_view_types': 'list,form',
            'display_name': 'Barcode Picking Client Action',
            'tag': 'stock_barcode_client_action',
            'target': 'fullscreen',
            'res_model': 'stock.picking',
            'context': {'precision': 2, 'active_id': picking_id},
            'params': false
        };
        return picking_action;
      },

    async _onDoAction(ev) {
        if (ev.type === "ir.actions.act_window" && ev.xml_id === "axx_picking_commission_workflow.action_add_pack_pid_wizard"){
            let picking_id = ev.context.picking_id;
            if (!picking_id) {
                picking_id = this.props.id;
            }
            this.scrollToTop = true;
            this.dialogService.add(FormViewDialog, {
                title: this.env._t('New PID'),
                resModel: 'stock.picking',
                resId: picking_id,
                context: {
                    form_view_ref: 'axx_picking_commission_workflow.view_axx_pid_stock_picking_form',
                },
                onRecordSaved: async () => {
                    await this.env.model.trigger('refresh');
                },
                onRecordDiscarded: async () => {
                    await this.env.model.trigger('refresh');
                },
            }, { onClose: async () => { await this.env.model.trigger('refresh'); }});
        }
        else {
            return await this._super(...arguments);
        }
    },

    /**
     * @private
     * @param {MouseEvent} event
     */
    async _onClickSetPackPid() {
        this.dialogService.add(FormViewDialog, {
            title: this.env._t('New PID'),
            resModel: 'stock.picking',
            resId: this.props.id,
            context: {
                form_view_ref: 'axx_picking_commission_workflow.view_axx_pid_stock_picking_form',
            },
            onRecordSaved: async () => {
                await this.env.model.trigger('refresh');
            },
        });
    },

    async putDown(ev) {
        if (!this.env.model.axxQtyEntered) {
            return false;
        }
        const axxRequiresPackaging = this.env.model.axxRequiresPackaging;

        if (axxRequiresPackaging) {
            await this.env.model._axxPutInPack({ save_and_close: true });
        } else {
            // First Wizard: 'Drive to WA-Bahn'
            this.dialogService.add(FormViewDialog, {
                title: this.env._t('Drive to WA-Bahn'),
                resModel: 'axx.put.down.wizard',
                context: {
                    form_view_ref: 'axx_picking_commission_workflow.view_axx_put_down_wizard_form',
                    active_id: this.props.id,
                },
                onRecordSaved: async () => {
                    await this.env.model.validate();
                    const backorder_id = await this.env.model.axxBackorderId();
                    // After confirming the 'Drive to WA-Bahn' wizard, show the next PID wizard
                    const self = this;
                    if (backorder_id && typeof backorder_id === 'object' && backorder_id.skip_pid) {
                            if (backorder_id.open_backorder){
                            const backorderAction = self.loadPicking(backorder_id.backorder_id);
                            self.action.doAction(backorderAction);
                            }
                            else{
                                await this.env.model.trigger('refresh');
                            }

                        }
                    else if (backorder_id !== 0) {
                        self.dialogService.add(FormViewDialog, {
                            title: self.env._t('New PID'),
                            resModel: 'stock.picking',
                            resId: backorder_id,
                            context: {
                                form_view_ref: 'axx_picking_commission_workflow.view_axx_pid_stock_picking_form',
                                coming_from_putDown: true,
                                picking_id: backorder_id
                            },
                            onRecordSaved: async () => {
                                try {
                                    const backorderAction = self.loadPicking(backorder_id);
                                    self.action.doAction(backorderAction);
                                } catch (error) {
                                    console.error("Failed to load next picking:", error);
                                }
                            },
                        });
                    } else {
                        await this.env.model.trigger('refresh');
                    }
                },
            });
        }
    },

    /**
     * Overriding this fuction to remove the auto scroll
     */
      _scrollToSelectedLine() {
        const selectedLine = this.env.model.selectedLine;
        const isaxxCommissionWorkflow = this.env.model.axxCommissionWorkflow
        if (isaxxCommissionWorkflow && selectedLine && selectedLine.result_package_id && selectedLine.qty_done == selectedLine.reserved_uom_qty) {
            if (this.scrollToTop) {
                this.scrollToTop = false;
                const page = document.querySelector('.o_barcode_lines');
                page.scroll({ left: 0, top: 0, behavior: this._scrollBehavior });
            }
            return;
        } else {
            this._super();
        }
    },
});
