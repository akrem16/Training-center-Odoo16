from odoo import api, fields, models, _

class Personnel(models.Model):
    _name = "hr.personnel"
    _inherit = ['hr.employee', 'mail.thread']

    category_ids = fields.Many2many(
        'hr.employee.category',
        relation='personnel_category_rel',
        column1='personnel_id',
        column2='category_id',
        string='Categories'
    )
    progressive_page_number = fields.Char("Personal Mobile")
    num_tel = fields.Char("Telephone Number")  # New field added here

