from odoo import models, fields, api

class Cours(models.Model):
    _name = 'academy.course'
    _inherit = 'mail.thread'
    _description = 'Cours'

    name = fields.Char(string="Title", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    category = fields.Selection([
        ('computer_science', 'Computer Science'),
        ('Multimédia', 'multimedia'),
    ], string="Category", required=True, tracking=True)
    learning_objectives = fields.Text(string="Learning Objectives", tracking=True)
    course_format = fields.Selection([
        ('online', 'En ligne'),
        ('onsite', 'Sur site'),
        ('hybrid', 'Hybride'),
    ], string="Format du cours" , default='online', tracking=True)
    duration = fields.Float(string="Duration (hours)", tracking=True)
    materials_resources = fields.Html(string="Materials and Resources", tracking=True)

    lang= fields.Selection([
        ('english', 'Anglais'),
        ('french', 'Français'),
        ('spanish', 'Espagnol'),
    ], string="Language", default='french',tracking=True)

    enseignant_id = fields.Many2one('hr.enseignant', string='Enseignant', required=True, tracking=True)

    student_ids = fields.Many2many(
        'hr.etudiant',
        'course_student_rel',
        'course_id',
        'student_id',
        string='Students'
    )

    total_etudiant = fields.Integer(
        string='Total Students',
        compute='_compute_total_etudiant',
    )
    @api.depends('student_ids')
    def _compute_total_etudiant(self):
        for course in self:
            course.total_etudiant = len(course.student_ids)
