from odoo import models, fields

class Course(models.Model):
    _name = 'academy.course'
    _description = 'Academy Course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    category = fields.Selection([
        ('computer_science', 'Computer Science'),
        ('mathematics', 'Mathematics'),
        ('history', 'History'),
        # Ajoutez autant de catégories que nécessaire
    ], string="Category", required=True)
    learning_objectives = fields.Text(string="Learning Objectives")
    course_format = fields.Selection([
        ('online', 'Online'),
        ('onsite', 'Onsite'),
        ('hybrid', 'Hybrid'),
    ], string="Course Format", default='online')
    duration = fields.Float(string="Duration (hours)")
    materials_resources = fields.Html(string="Materials and Resources")
    language = fields.Selection([
        ('english', 'English'),
        ('french', 'French'),
        ('spanish', 'Spanish'),
        # Ajoutez d'autres langues si nécessaire
    ], string="Language", default='english')
