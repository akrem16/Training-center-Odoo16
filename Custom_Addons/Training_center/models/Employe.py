from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    enseignant_id = fields.Many2one('hr.enseignant', string="Enseignant Associé", auto_join=True)

#     category_ids = fields.Many2many('category.model',
#                                     relation='custom_category_employee_rel',
#                                     column1='employee_id',
#                                     column2='category_id',
#                                     string='Categories')
