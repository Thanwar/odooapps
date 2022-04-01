from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    # class properties
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _order = "name desc"

    # Class fields
    name = fields.Char(string='Order Reference', required=True, copy=False,
                       readonly=True, default=lambda self: _('New'))
    patient_ID = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_ID = fields.Many2one('hospital.doctor', string='Doctor')
    age = fields.Integer(string='Age', related='patient_ID.age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    note = fields.Text(string='Description')
    prescription = fields.Text(string='Prescription')
    other_info = fields.Text(string='other_info')
    # date field
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Date Checkup Time")
    # state for status-bar and header
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)

    # One2Many field
    prescription_lines_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                             string='Prescription Lines')

    # BTN functions

    # Action_confirm_BTN function
    def action_confirm(self):
        self.state = 'confirm'

    # Action_done_BTN function
    def action_done(self):
        self.state = 'done'

    # Action_draft_BTN function
    def action_draft(self):
        self.state = 'draft'

    # Action_cancel_BTN function
    def action_cancel(self):
        self.state = 'cancel'

    # Override Create Method

    @api.model
    def create(self, vals):
        print("Create overrided")
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    @api.onchange('patient_ID')
    def onchange_patient_ID(self):
        if self.patient_ID:
            if self.patient_ID.gender:
                self.gender = self.patient_ID.gender
            if self.patient_ID.note:
                self.note = self.patient_ID.note
        else:
            self.gender = ''
            self.note = ''


# Another Model for One2Many field

class AppointmentPrescriptionLines(models.Model):
    # class properties
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription ines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
