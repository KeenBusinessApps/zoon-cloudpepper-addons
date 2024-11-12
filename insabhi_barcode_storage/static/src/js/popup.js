odoo.define('insabhi_barcode_storage.redirect', function (require) {
    "use strict";

    const core = require('web.core');
    const Menu = require('web.Menu');

    Menu.include({
        _onMenuItemClick: function (ev) {
            const $menuItem = $(ev.currentTarget);
            const url = $menuItem.data('url');
            if (url) {
                window.location.href = url;
                ev.preventDefault();  // Prevent the default action
            } else {
                this._super(ev);
            }
        },
    });
});
