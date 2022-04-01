from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    # class properties
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    # Class fields
    date_appointment = fields.Date(string='Date', required=True)
    patient_ID = fields.Many2one('hospital.patient', string='Patient', required=True)

    def action_create_appointment(self):
        vals = {
            'patient_ID': self.patient_ID.id,
            'date_appointment': self.date_appointment
        }
        self.env['hospital.appointment'].create(vals)



