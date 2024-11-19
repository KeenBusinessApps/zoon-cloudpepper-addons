/* @odoo-module */
import { patch } from "@web/core/utils/patch";
import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { _t } from "@web/core/l10n/translation";

patch(ProductsWidget.prototype, {

    // Method to add a product to the current order
    addProductToCurrentOrder(product) {
        console.log('Adding product to order:', product);
        this.pos.addProductToCurrentOrder(product);
    },

    // Method to handle product info click
    onProductInfoClick(product) {
        console.log('Showing product info:', product);
        this.showProductInfoModal(product);
    },

    // Corrected getter for productsToDisplay
    get productsToDisplay() {
        let originalList = super.productsToDisplay;
        const { db } = this.pos;
        const customer_id = this.pos.get_order().partner ? this.pos.get_order().partner.id : null;
        let list = [];

        // Search products based on the search term
        if (this.searchWord !== "") {
            list = db.search_product_in_category(this.selectedCategoryId, this.searchWord);
        } else {
            list = db.get_product_by_category(this.selectedCategoryId);
        }

        // Filter by customer-specific products if a customer is selected
        if (customer_id) {
            const customer_products = db.get_product_by_customer(customer_id);
            list = customer_products;
        }

        // Remove products that shouldn't be displayed
        list = list.filter((product) => !this.getProductListToNotDisplay().includes(product.id));

        // Debugging log to check product details
        list.forEach(product => {
            console.log("Product ID: ", product.id);
            console.log("Unique ID: ", product.x_studio_unique_id);
            console.log("Shipping Method: ", product.x_studio_shipping_method_1);
        });

        // Return sorted list by product display name
        return list.sort((a, b) => a.display_name.localeCompare(b.display_name));
    }
});
