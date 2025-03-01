from odoo import models, fields

class Equipment(models.Model):
    _name = 'academy.equipment'
    _description = 'Equipment'

    name = fields.Char(required=True)
    quantity = fields.Integer(required=True)
    description = fields.Text(string="Description")
