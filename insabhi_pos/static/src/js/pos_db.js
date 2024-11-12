
/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosDB } from "@point_of_sale/app/store/db";

patch(PosDB.prototype, {
    add_products(products) {
        super.add_products(products);
        this.product_by_customer = {};
        for (var i = 0, len = products.length; i < len; i++) {
            var product = products[i];
            if(this.product_by_customer && this.product_by_customer[product.x_studio_customer[0]]){
                this.product_by_customer[product.x_studio_customer[0]].push(product);
            }else{
                this.product_by_customer[product.x_studio_customer[0]] = [product];
            }
        }
    },
    get_product_by_customer(customer_id){
        if(this.product_by_customer[customer_id]){
            return this.product_by_customer[customer_id];
        }else{
            return [];
        }
    }
});