/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";

import { _t } from "@web/core/l10n/translation";

patch(ProductsWidget.prototype,{
    get productsToDisplay() {
    debugger
        let originalList = super.productsToDisplay;
        const { db } = this.pos;
        const customer_id = this.pos.get_order().partner ? this.pos.get_order().partner.id : null;
        let list = [];
        if (this.searchWord !== "") {
            list = db.search_product_in_category(this.selectedCategoryId, this.searchWord);
        } else {
            list = db.get_product_by_category(this.selectedCategoryId);
        }

        if (customer_id) {
            const customer_products = db.get_product_by_customer(customer_id);
            list = customer_products;
        }
        list = list.filter((product) => !this.getProductListToNotDisplay().includes(product.id));

        return list.sort((a, b) => a.display_name.localeCompare(b.display_name));
    }
});
