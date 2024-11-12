# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result["search_params"]["fields"].extend([
        "x_studio_customer",
        "x_studio_unique_id",
        "x_studio_shipping_method_1"
    ])
        return result