from odoo import api, fields, models, _


class HospitalPatient(models.Model):
    # class properties
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    # Class fields
    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True,
                            copy=False, readonly=True, default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    # state for status-bar and header
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)
    responsible_ID = fields.Many2one(comodel_name='res.partner', string="Responsible")

    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')

    image = fields.Binary(string="Patient Image")

    appointments_ids = fields.One2many('hospital.appointment','patient_ID', string="Appointments")


    # functions
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_ID','=',rec.id)])
            rec.appointment_count = appointment_count

    # Action_confirm_BTN function
    def action_confirm(self):
        print("Confirm Pressed")
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
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res
