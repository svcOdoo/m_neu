/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from 'web.utils';
import { useService } from "@web/core/utils/hooks";
import { onRendered, onMounted, onWillStart, useEffect } from "@odoo/owl";

patch(FormController.prototype, '@axx_barcode_replenishment/js/form_controller', {

setup() {
        this._super(...arguments);
        onWillStart(() => {
                if(this.props.setParent){
                 this.props.setParent.setPackageRef(this);
                }

        });
        },

});

FormController.props = {
...FormController.props,
setParent: {type: Object, optional: true}
}
