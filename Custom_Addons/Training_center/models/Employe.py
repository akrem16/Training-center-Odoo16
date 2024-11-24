from odoo import models, fields, _
from odoo.odoo import api
from odoo.odoo.exceptions import ValidationError


class HREmployee(models.Model):
    _inherit = 'hr.employee'


    CIN = fields.Char(string='CIN', tracking=True)
    enseignant_id = fields.Many2one('hr.enseignant', string="Enseignant Associé", auto_join=True)

    # image_1920 = fields.Image("Image de Profil")


#     category_ids = fields.Many2many('category.model',
#                                     relation='custom_category_employee_rel',
#                                     column1='employee_id',
#                                     column2='category_id',
#                                     string='Categories')


total_employee = fields.Integer(string="Total Employees", compute="_compute_total_employee")
CIN = fields.Char(string='CIN', tracking=True)


@api.depends('employee_ids')
def _compute_total_employee(self):
    for department in self:
        department.total_employee = len(department.employee_ids)


_sql_constraints = [
    ('CIN_name_unique',
     'unique(CIN)',
     'CIN doit être unique')
]


def create(self, vals):
    # Validation du matricule
    if 'matricule' in vals:
        matricule = vals['matricule']
        if not matricule.isdigit() or len(matricule) != 8:
            raise ValidationError(_("Le matricule doit contenir exactement 8 chiffres."))

    # Continuer avec la création si la validation est réussie
    return super(HREmployee, self).create(vals)
