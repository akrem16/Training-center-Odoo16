from odoo import models, fields, api
from datetime import datetime, time

class Conge(models.Model):
    _inherit = 'hr.leave'
    enseignant_id = fields.Many2one('hr.enseignant', string='Enseignant', required=True)

