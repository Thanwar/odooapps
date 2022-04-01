from odoo import api, models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor"
    _rec_name = "doctor_name"

    doctor_name = fields.Char(string="Name", required=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], default='male', string="Gender", required=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string="Doctor Image")
