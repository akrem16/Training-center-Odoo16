/** @odoo-module **/

import BoardView from 'board.BoardView';
import core from 'web.core';
import dataManager from 'web.data_manager';

const QWeb = core.qweb;

BoardView.prototype.config.Controller.include({
    custom_events: _.extend({}, BoardView.prototype.config.Controller.prototype.custom_events, {
        save_dashboard: '_saveDashboard',
    }),

    /**
     * Actually save a dashboard
     * @override
     * @returns {Promise}
     */
    _saveDashboard: function () {
        var board = this.renderer.getBoard();
        var arch = QWeb.render('Dashboard.xml', _.extend({}, board));
        return this._rpc({
            route: '/web/view/edit_custom',
            params: {
                custom_id: this.customViewID != null? this.customViewID : "",
                arch: arch,
            },
        }).then(dataManager.invalidate.bind(dataManager));
    },
});
