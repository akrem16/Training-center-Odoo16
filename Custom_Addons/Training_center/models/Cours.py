from odoo import models, fields, api, _
from odoo.addons.google_recaptcha.models.ir_http import logger


class Cours(models.Model):
    _name = 'academy.course'
    _inherit = 'mail.thread'
    _description = 'Cours'

    name = fields.Char(string="Titre", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    category_id = fields.Many2one('academy.course.category', string="Catégorie", required=True, tracking=True)
    learning_objectives = fields.Text(string="Objectifs d'apprentissage", tracking=True)
    course_format = fields.Selection([
        ('online', 'En ligne'),
        ('in_person', 'Présentielle'),
    ], string="Format du cours", default='online', tracking=True)
    duration = fields.Float(string="Durée (heures)", tracking=True)
    materials_resources = fields.Html(string="Matériaux et ressources", tracking=True)
    fee = fields.Float(string="Frais", required=True)

    lang = fields.Selection([
        ('english', 'Anglais'),
        ('french', 'Français'),
        ('spanish', 'Espagnol'),
    ], string="Langue", default='french', tracking=True)

    enseignant_id = fields.Many2one('hr.enseignant', string='Enseignant', tracking=True)

    student_ids = fields.Many2many(
        'hr.etudiant',
        'course_student_rel',
        'course_id',
        'student_id',
        string='Étudiants'
    )
    total_etudiant = fields.Integer(
        string='Total Étudiants',
        compute='_compute_total_etudiant',
        store=True,
    )
    session_ids = fields.One2many('academy.course.session', 'course_id', string="Séances")

    state = fields.Selection([('draft', 'Brouillon'), ('in_progress', 'En cours'), ('completed', 'Terminé'), ('cancel', 'Annuler')
                              ], string='Status', readonly=False, tracking=True, default='draft', copy=False)
    active = fields.Boolean(string='Active', default=True, tracking=True)



    @api.depends('student_ids')
    def _compute_total_etudiant(self):
        for course in self:
            course.total_etudiant = len(course.student_ids)

    _sql_constraints = [
        ('name_description_check',
         'check (name != description)',
         'Le nom et la description du cours ne peuvent pas être identiques.'),

        ('course_name_unique',
         'unique(name)',
         'Le nom du cours doit être unique'),
    ]


