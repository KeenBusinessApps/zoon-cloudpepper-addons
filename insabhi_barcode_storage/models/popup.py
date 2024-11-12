from odoo import models, fields

class CustomBarcodeScan(models.Model):
    _name = 'custom.barcode.scan'
    _description = 'Custom Barcode Scan'

    def action_open_scanner(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Scanner Opened',
                'message': 'You can now scan a barcode.',
                'sticky': False,
            },
        }
