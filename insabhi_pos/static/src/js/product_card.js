/** @odoo-module */

import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import { props } from "@odoo/owl";

patch(ProductCard, {
    props: {
        class: { type: String, optional: true },
        name: { type: String, required: true },
        productId: { type: Number, required: true },
        price: { type: String, required: true },
        imageUrl: { type: [String, Boolean], optional: true },
        productInfo: { type: Boolean, optional: true },
        onClick: { type: Function, optional: true },
        onProductInfoClick: { type: Function, optional: true },
        uniqueID: { type: [String, Boolean], optional: true },
        shippingMethod: { type: [String, Boolean], optional: true },
    },

    setup() {
        super.setup();
    },
});
