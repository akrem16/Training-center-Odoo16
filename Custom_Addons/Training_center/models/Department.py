from odoo import models, fields, api

class Conge(models.Model):
    _inherit = ['hr.department','mail.thread']
    _description = "Department"

    enseignant_ids = fields.One2many(
        'hr.enseignant',
        'department_id',
        string='Enseignants'
    )

