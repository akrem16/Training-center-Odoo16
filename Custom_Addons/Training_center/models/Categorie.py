from odoo import models, fields

class CoursCategorie(models.Model):
    _name = 'academy.course.category'
    _description = 'Cours Categorie'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
