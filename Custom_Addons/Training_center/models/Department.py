from odoo import models, fields, api
from odoo.addons.hr.models.hr_department import Department

class Conge(models.Model):
    _inherit = ['hr.department','mail.thread']
    _description = "Department"

    enseignant_ids = fields.One2many(
        'hr.enseignant',
        'department_id',
        string='Enseignants'
    )

    formateur_ids = fields.One2many(
        'hr.enseignant',
        'department_id',
        string='Enseignants'
    )


    total_employee = fields.Integer(compute='_compute_total_employee', string='Total Employee', store=True,)
