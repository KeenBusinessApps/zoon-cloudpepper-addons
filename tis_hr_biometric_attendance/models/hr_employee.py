# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import fields, models


class HrEmployee(models.Model):
    """Inherits HrEmployee model to include a relationship with biometric devices"""
    _inherit = 'hr.employee'

    biometric_device_ids = fields.One2many('biometric.attendance.devices', 'employee_id', string='Biometric Devices')
    card_number = fields.Char(string="Card Number", groups="hr.group_hr_user", copy=False,
                              help="This card number is used for authentication purposes and will be passed to the biometric device")


class BiometricAttendanceDevices(models.Model):
    """Model biometric attendance devices and their association with employees."""
    _name = 'biometric.attendance.devices'
    _description = 'biometric attendance devices'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    biometric_attendance_id = fields.Char(string='Biometric User ID', required=True)
    device_id = fields.Many2one('biometric.config', string='Biometric Attendance Device', required=True)
