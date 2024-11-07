from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    lot_stock_warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse'
    )


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    lot_stock_ids = fields.One2many(
        'stock.location', 'lot_stock_warehouse_id',
        string='Stock Locations',
        domain = "[('usage', '=', 'internal'), ('company_id', '=', company_id)]",
    )

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if self.picking_type_id.code == 'internal':
            error_message = ""
            for line in self.move_line_ids:
                quantity_available = line.location_id.quant_ids.filtered(
                    lambda q: q.product_id == line.product_id).quantity

                if quantity_available < line.qty_done:
                    error_message += f"""The product '{line.product_id.display_name}' is not available in sufficient quantity at '{line.location_id.display_name}'.\n"""
                    error_message += f"Available quantity: {quantity_available}, required quantity: {line.qty_done}.\n\n"

            if error_message:
                raise ValidationError(error_message)

        return super(StockPicking, self).button_validate()