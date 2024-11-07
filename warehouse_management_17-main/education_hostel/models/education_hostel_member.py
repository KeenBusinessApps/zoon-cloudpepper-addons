# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Jumana Haseen (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationHostelMember(models.Model):
    """Created model 'education.hostel.member'"""
    _name = 'education.hostel.member'
    _rec_name = 'hostel_admission_no'
    _description = "Hostel Member"

    name = fields.Char(string="Name", help='Name of hostel member')
    member_type = fields.Selection(string='Member Type',
                                   selection=[('is_faculty', 'Faculty'),
                                              ('is_student', 'Student')],
                                   default='is_student', help="Select faculty"
                                                              "or student.", )
    student_id = fields.Many2one('education.student',
                                 string="Admission No",
                                 domain=[('need_hostel', '=', True),
                                         ('hostel_id', '=', False)],
                                 help="Student admission number.")
    faculty_id = fields.Many2one('education.faculty',
                                 string="Name", help="Faculty name.")
    email = fields.Char(string="Email", help="Email of hostel member")
    hostel_admission_no = fields.Char(string="Hostel Admission No",
                                      required=True, copy=False, readonly=True,
                                      index=True, default=lambda self: _('New'),
                                      help='Sequence of admission number.')
    phone = fields.Char(string="Phone", help='Phone of hostel member')
    mobile = fields.Char(string="Mobile", help='Mobile of hostel member')
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar"
                               " for this contact, limited to 1024x1024px")
    date_of_birth = fields.Date(string="Date Of birth",
                                help='DOM of hostel member')
    guardian_name = fields.Char(string="Guardian",
                                help='Guardian of hostel member')
    father_name = fields.Char(string="Father", help='Father of hostel member')
    mother_name = fields.Char(string="Mother", help='Mother of hostel member')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender', required=True, default='male',
        help='Gender of hostel member')
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'),
         ('ab-', 'AB-'), ('ab+', 'AB+')],
        string='Blood Group', required=True,
        default='a+', help='Blood group of hostel member')
    street = fields.Char(string='Street', help='Street of hostel member')
    street2 = fields.Char(string='Street2', help='Street2 of hostel member')
    zip = fields.Char(string='Zip', change_default=True,
                      help='Zip of hostel member')
    city = fields.Char(string='City', help='City of hostel member')
    state_id = fields.Many2one("res.country.state",
                               string='State', help='State of hostel member')
    country_id = fields.Many2one('res.country', string='Country',
                                 help='Country of hostel member'
                                 )
    allocation_detail_ids = fields.One2many('education.room_member',
                                            'room_member_id',
                                            string="Allocation Details",
                                            help='Members allocated to the '
                                                 'hostel')
    hostel_id = fields.Many2one('education.hostel', string="Hostel",
                                help='Hostel of hostel member')
    room_id = fields.Many2one('education.room', string="Room",
                              help='Room of hostel member')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env[
                                     'res.company']._company_default_get(),
                                 help='Company of hostel member')
    state = fields.Selection([('draft', 'Draft'), ('allocated', 'Allocated'),
                              ('vacated', 'Vacated')],
                             string='Status', default='draft',
                             help='State of hostel member')
    vacated_date = fields.Date(string="Vacated Date",
                               help='Date of vacating hostel')

    @api.onchange('student_id')
    def _onchange_student_id(self):
        """Onchange student information"""
        for student in self.student_id:
            self.email = student.email
            self.phone = student.phone
            self.mobile = student.mobile
            self.date_of_birth = student.date_of_birth
            self.guardian_name = student.guardian_id.name
            self.father_name = student.father_name
            self.mother_name = student.mother_name
            self.street = student.per_street
            self.zip = student.per_zip
            self.street2 = student.per_street2
            self.city = student.per_city
            self.state_id = student.per_state_id
            self.country_id = student.per_country_id
            self.gender = student.gender

    @api.onchange('faculty_id')
    def _onchange_faculty_id(self):
        """Onchange faculty name that updated the faculty details"""
        for student in self.faculty_id:
            self.email = student.email
            self.phone = student.phone
            self.mobile = student.mobile
            self.date_of_birth = student.date_of_birth
            self.guardian_name = student.guardian_name
            self.father_name = student.father_name
            self.mother_name = student.mother_name
            self.gender = student.gender

    @api.model
    def create(self, vals):
        """Computing the name of the member"""
        if vals.get('hostel_admission_no', _('New')) == _('New'):
            vals['hostel_admission_no'] = self.env['ir.sequence'].next_by_code(
                'education.hostel.member') or _('New')
        if vals.get('student_id'):
            obj = self.env['education.student'].search(
                [('id', '=', vals.get('student_id'))])
        elif vals.get('faculty_id'):
            obj = self.env['education.faculty'].search(
                [('id', '=', vals.get('faculty_id'))])
        else:
            obj = False
        if obj:
            if obj._name == 'education.student':
                if obj.middle_name:
                    vals[
                        'name'] = obj.name + '  ' + obj.middle_name + '  ' + obj.last_name
                else:
                    vals['name'] = obj.name + '  ' + obj.last_name
            elif obj._name == 'education.faculty':
                vals[
                    'name'] = obj.name + ' ' + obj.last_name if obj.last_name \
                    else obj.last_name
        res = super(EducationHostelMember, self).create(vals)
        return res

    @api.onchange('student_id', 'faculty_id')
    def _onchange_student_id(self):
        """Computing the name of the member"""
        for name in self:
            if name.student_id:
                name.image = name.student_id.image_1920
                name.name = str(str(name.student_id.name) + ' ' + str(
                    name.student_id.last_name)) if (
                    name.student_id.last_name) else str(
                    name.student_id.name)
            if name.faculty_id:
                name.name = str(
                    name.faculty_id.name + ' ' +
                    name.faculty_id.last_name) if (
                    name.faculty_id.last_name) else str(
                    name.faculty_id.name)

    @api.constrains('allocation_detail_ids')
    def _check_capacity(self):
        """Getting the current room and Hostel"""
        if len(self.allocation_detail_ids) != 0:
            self.hostel_id = self.allocation_detail_ids[
                len(self.allocation_detail_ids) - 1].hostel_room_rel.id
            self.room_id = self.allocation_detail_ids[
                len(self.allocation_detail_ids) - 1].room_id.id
            self.vacated_date = self.allocation_detail_ids[
                len(self.allocation_detail_ids) - 1].vacated_date
            self.student_id.hostel_member = self.id
            self.student_id.hostel_id = self.hostel_id.id
            self.student_id.room_id = self.room_id.id
            self.student_id.hostel_fee = self.hostel_id.total

    def action_allocate_member(self):
        """Function to allocate member"""
        self.ensure_one()
        if self.allocation_detail_ids:
            length = len(self.allocation_detail_ids)
            if not self.allocation_detail_ids[length - 1].allocated_date:
                raise ValidationError(_('Enter the Allocated Date'))
        else:
            raise ValidationError("Please add the Allocation Details")
        return self.write({'state': 'allocated'})

    def action_vacate_member(self):
        """Function to vacate from hostel"""
        self.ensure_one()
        if self.allocation_detail_ids:
            length = len(self.allocation_detail_ids)
            if not self.allocation_detail_ids[length - 1].vacated_date:
                raise ValidationError(_('Enter the Vacated Date'))
        self.student_id.hostel_id = False
        return self.write({'state': 'vacated'})

    def action_reallocate(self):
        """Function to reallocate the hostel room"""
        self.student_id.write({
            'hostel_id': self.hostel_id.id
        })
        return self.write({
            'state': 'draft',
            'vacated_date': False
        })
