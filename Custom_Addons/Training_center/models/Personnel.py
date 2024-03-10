from odoo import api, fields, models, _

class Personnel(models.Model):
    _inherit = ['hr.employee','mail.thread']
    _order = 'name'

