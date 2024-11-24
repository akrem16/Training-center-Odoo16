from random import choice
from string import digits

from odoo import models, fields, api, _
from datetime import datetime

from odoo.odoo.exceptions import ValidationError, UserError


class Etudiant(models.Model):
    _name = 'hr.etudiant'
    _inherit = ['mail.thread']
    _description = "Etudiant"

    matricule = fields.Char(string='CIN', tracking=True, required=True)
    reference = fields.Char(string='Reference', required=True, tracking=True, copy=False, readonly=True,
                            default=lambda self: self.env['ir.sequence'].next_by_code('hr.etudiant'))
    date_inscription = fields.Date(string="Date d'inscription", tracking=True, required=True)
    resultat_examen = fields.Float(string="Moyenne", tracking=True, required=True)
    adresse = fields.Text(string="Adresse", tracking=True, required=True)

    # Informations personnelles
    prenom_etudiant = fields.Char(string="Prénom", store=True, tracking=True, required=True)
    name = fields.Char(string="Nom", store=True, tracking=True, required=True)

    date_naissance = fields.Date(string="Date de naissance", store=True, tracking=True, required=True)
    genre = fields.Selection([('male', 'Masculin'), ('female', 'Féminin')], string="Genre",
                             store=True, tracking=True, required=True)
    email = fields.Char(string="Email", store=True, tracking=True, required=True)
    telephone = fields.Char(string="Téléphone", store=True, tracking=True, required=True)
    image = fields.Image(tracking=True)

    course_id = fields.Many2one('academy.course', string='Formation', tracking=True, required=True)
    course_ids = fields.Many2many(
        'academy.course',
        'course_student_rel',
        'student_id',
        'course_id',
        string='Courses'
    )

    session_ids = fields.Many2many(
        'academy.course.session',
        'etudiant_session_rel',
        'etudiant_id',
        'session_id',
        string='Sessions Inscriptions',
        help="Les sessions auxquelles l'étudiant est inscrit.",
        tracking=True,
        required=True
    )



    category_ids = fields.Many2many(
        'hr.employee.category',
        relation='hr_etudiant_category_rel',
        column1='etudiant_id',
        column2='category_id',
        string='Categories'
    )
    active = fields.Boolean(string='Active', default=True, tracking=True)
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user",
                          copy=False)

    session_id = fields.Many2one('academy.course.session', string="Session Associée")

    _sql_constraints = [
        ('barcode_uniq', 'unique (barcode)',
         "The Badge ID must be unique, this one is already assigned to another employee."),
        ('user_uniq', 'unique (user_id, company_id)',
         "A user cannot be linked to multiple employees in the same company."),

        ('CIN_name_unique',
         'unique(matricule)',
         'CIN doit être unique'),
    ]



    @api.model
    def create(self, vals):
        if vals.get('reference', '') == '':  # Check for empty string
            vals['reference'] = self.env['ir.sequence'].next_by_code('hr.etudiant')
        return super(Etudiant, self).create(vals)

    def write(self, vals):
        return super(Etudiant, self).write(vals)

    @api.depends('course_id')
    def _compute_available_sessions(self):
        for etudiant in self:
            if etudiant.course_id:
                etudiant.available_session_ids = self.env['academy.course.session'].search([
                    ('course_id', '=', etudiant.course_id.id),
                    ('state', '=', 'draft')  # Vous pouvez filtrer les sessions par tout autre critère nécessaire
                ])
            else:
                etudiant.available_session_ids = False

    @api.onchange('course_id')
    def _onchange_course_id(self):
        if self.course_id:
            self.course_ids = [(6, 0, [self.course_id.id])]
        else:
            self.course_ids = False

    available_session_ids = fields.Many2many(
        'academy.course.session',
        compute='_compute_available_sessions',
        string='Sessions disponibles'
    )

    session_id = fields.Many2one(
        'academy.course.session',
        string="Session Choisi",
        domain="[('course_id', '=', course_id), ('state', '=', 'draft')]",
        # Assure que seulement les sessions du cours sélectionné sont affichées.
        help="Choisissez une session pour l'inscription."
    )

    def generate_random_barcode(self):
        for etudiant in self:
            etudiant.barcode = '058' + "".join(choice(digits) for i in range(9))

    numero_de_facture = fields.Char(string='Numéro de facture', compute='_compute_numero_facture', store=True)

    @api.depends('date_inscription', 'matricule')
    def _compute_numero_facture(self):
        for etudiant in self:
            if etudiant.date_inscription and etudiant.reference:
                # Logique pour générer le numéro de facture
                numero_de_facture = f"{etudiant.date_inscription.year}/{etudiant.date_inscription.month:02d}/{etudiant.reference}"
                etudiant.numero_de_facture = numero_de_facture

    @api.model
    def create(self, vals):
        record = super(Etudiant, self).create(vals)
        if record.session_id:
            record.session_id.write({'attendee_ids': [(4, record.id)]})
        return record

    def write(self, vals):
        if 'matricule' in vals:
            matricule_value = vals.get('matricule')
            if matricule_value and not matricule_value.isdigit():
                raise UserError("Le matricule ne doit contenir que des chiffres.")
        return super(Etudiant, self).write(vals)


@api.model
def copy(self, vals):
    raise UserError(_("Copying is not allowed for this model."))
