/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from 'web.utils';
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, '@axx_split_list_records/js/list_controller', {

setup() {
        this._super(...arguments);
        this.orm = useService("orm");
        },

async openRecord(record) {
    const sup = this._super
    // disable below code for now, get_param only works for admins
    if (record.resModel !== 'stock.picking'){
        return sup(...arguments);
    }
    const splitLimit = await this.orm.call("stock.picking", "get_param_split_limit", []);
        const Limit = splitLimit && parseInt(splitLimit) || false;
        if (Limit && Limit !=0){
            var action = await this.orm.call(record.resModel, "get_split_action", [
            record.resId, Limit
            ]);
            if (action){
               this.actionService.doAction({
            name: action.name,
            res_model: action.res_model,
            type: "ir.actions.act_window",
            views: [[false, "form"]],
            view_mode: "form",
            target: 'new',
            context: action.context
        });
            }
            else{
                sup(...arguments);
            }
        }
        else{
            sup(...arguments);
        }

}

});