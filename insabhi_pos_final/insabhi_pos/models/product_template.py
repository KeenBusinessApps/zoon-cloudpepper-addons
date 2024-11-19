from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_total_shipping_cost = fields.Float(string='Total Shipping Cost', readonly=True)
    list_price = fields.Float(compute='_compute_list_price', store=True)

    @api.depends('x_studio_total_shipping_cost')
    def _compute_list_price(self):
        for record in self:
            record.list_price = record.x_studio_total_shipping_cost
