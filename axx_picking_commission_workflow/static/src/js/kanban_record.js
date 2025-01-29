/** @odoo-module **/

import { KanbanRecord } from "@web/views/kanban/kanban_record";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";

patch(KanbanRecord.prototype, '@axx_picking_commission_workflow/js/kanban_record', {
    setup() {
        this._super(...arguments);
        this.dialogService = useService("dialog");
        this.orm = useService('orm');
    },

    async loadNextAction() {
        const action = await this.orm.call(
            'stock.picking',
            'action_confirm_packaging',
            [this.props.record.resId],
            { context: { open_record: true } }
        );
        return action;
    },

    onGlobalClick(ev) {
        const sup = this._super;
        const { archInfo, forceGlobalClick, openRecord, record } = this.props;
        (async () => {
            if(this.props.record.resModel !== 'stock.picking'){
                return sup(...arguments);
            }
            const need_action = await this.orm.call(
                'stock.picking',
                'get_need_pack_action_ignore_pid',
                [this.props.record.resId]
            );
            if (need_action === false) {
                return sup(...arguments);
            }
            this.dialogService.add(FormViewDialog, {
                title: this.env._t('Add PACK PID'),
                resModel: 'stock.picking',
                resId: record.resId,
                context: {
                    form_view_ref: 'axx_picking_commission_workflow.view_axx_pid_stock_picking_form',
                },
                onRecordSaved: async () => {
                    const action = await this.loadNextAction();
                    if (action) {
                        this.action.doAction(action);
                    }
                },
                onRecordDiscarded: async () => {
                        // do nothing
                },
            });
        })();
    }
});
