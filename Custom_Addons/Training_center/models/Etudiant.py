from odoo import models, fields , api


class Etudiant(models.Model):
    _name = 'hr.etudiant'
    _inherit = ['hr.employee', 'mail.thread']
    _description = "Etudiant"


    # Champs spécifiques à l'étudiant
    matricule = fields.Char(string='Matricule', required=True, tracking=True)
    date_inscription = fields.Date(string="Date d'inscription", tracking=True)
    # promotion_id = fields.Many2one('hr.promotion', string="Promotion")
    resultat_examen = fields.Float(string="Moyenne", tracking=True)
    adresse = fields.Text(string="Adresse", tracking=True)

    # Informations personnelles
    prenom_etudiant = fields.Char(string="Prénom", store=True, tracking=True)
    date_naissance = fields.Date(string="Date de naissance",store=True, tracking=True)
    genre = fields.Selection([('male', 'Masculin'), ('female', 'Féminin')], string="Genre",
                             store=True, tracking=True)
    email = fields.Char(string="Email", store=True, tracking=True)
    telephone = fields.Char(string="Téléphone", store=True, tracking=True)
    image = fields.Image()
    # course_id = fields.Many2one('academy.course', string='Course')
    course_ids = fields.Many2many(
        'academy.course',
        'course_student_rel',
        'student_id',
        'course_id',
        string='Courses'
    )

    category_ids = fields.Many2many(
        'hr.employee.category',
        relation='hr_etudiant_category_rel',
        column1='etudiant_id',
        column2='category_id',
        string='Categories'
    )

    @api.model
    def creat(self, vals):
        # if not vals.get('resultat_examen'):
        #     vals['resultat_examen'] = 'New etudiant'
        return super(Etudiant, self).creat(vals)


    def write(self, vals):
        return super(Etudiant, self).write(vals)
