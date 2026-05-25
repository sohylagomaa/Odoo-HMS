from odoo import models, fields

class HmsLog(models.Model):
    _name = 'hms.log'
    _description = 'Patient Log History'

    patient_id  = fields.Many2one('hms.patient', string='Patient')
    created_by  = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text(string='Description')