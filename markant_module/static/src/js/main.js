/** @odoo-module **/

import MainComponent from '@stock_barcode/components/main';
import { patch } from 'web.utils';

patch(MainComponent.prototype, 'markant_module_main_component', {

    async saveFormView(lineRecord) {
        const lineId = (lineRecord && lineRecord.data.id) || (this._editedLineParams && this._editedLineParams.currentId);
        const recordId = (lineRecord.resModel === this.props.model) ? lineId : undefined
        await this._onRefreshState({ recordId, lineId });
        await this.env.model.trigger('refresh')
    }
});