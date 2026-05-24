from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history    = fields.Html(string='History')
    cr_ratio   = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ], string='Blood Type')
    pcr        = fields.Boolean(string='PCR')
    image      = fields.Image(string='Image')
    address    = fields.Text(string='Address')
    email      = fields.Char(string='Email')
    age = fields.Integer(
    string='Age',
    compute='_compute_age',
    store=True
)

    # relations
    department_id = fields.Many2one(
        'hms.department',
        string='Department',
        domain="[('is_opened', '=', True)]"
    )

    capacity = fields.Integer(
        related='department_id.capacity',
        string='Department Capacity',
        readonly=True
    )

    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')
    log_ids = fields.One2many('hms.log', 'patient_id', string='Log History')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Auto-Checked',
                    'message': 'PCR has been automatically checked because age is below 30.'
                }
            }
        
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError('CR Ratio is mandatory when PCR is checked!')
    
    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                # Check valid email format
                import re
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', rec.email):
                    raise ValidationError('Please enter a valid email address!')
                # Check uniqueness
                duplicate = self.search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.id)
                ])
                if duplicate:
                    raise ValidationError('Email already exists in another patient!')
                
        
    def write(self, vals):
        if 'state' in vals:
            state_label = dict(self._fields['state'].selection).get(vals['state'])
            self.env['hms.log'].create({
                'patient_id': self.id,
                'description': f'State changed to {state_label}',
            })
        return super().write(vals)
    
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                from datetime import date
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
