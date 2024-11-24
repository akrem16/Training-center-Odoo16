from odoo import models, fields

class Classroom(models.Model):
    _name = 'academy.classroom'
    _description = 'Classroom'

    name = fields.Char(required=True, string="Name", help="Name of the classroom.")
    capacity = fields.Integer(string="Capacity", help="Capacity of the classroom.")
    equipment_ids = fields.Many2many('academy.equipment', string="Equipment", help="Equipment available in the classroom.")
