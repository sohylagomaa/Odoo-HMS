from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient'
    )

@api.constrains('email', 'related_patient_id')
def _check_patient_email(self):
    for rec in self:
        if rec.email:
            patient = self.env['hms.patient'].search([
                ('email', '=', rec.email)
            ])
            if patient and rec.related_patient_id.id != patient.id:
                raise ValidationError(
                    f'A patient with email {rec.email} already exists! '
                    f'You cannot link this customer.'
                )
            

def unlink(self):
    for rec in self:
        if rec.related_patient_id:
            raise ValidationError(
                'You cannot delete a customer linked to a patient!'
            )
    return super().unlink()