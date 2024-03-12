from odoo import api, fields, models, _


class Enseignant(models.Model):
    _name = "hr.enseignant"
    _inherit = ['hr.employee', 'mail.thread']
    _description = "Enseignant"
    _order = 'name'

    # Inherited fields like 'address', 'name', etc., from 'hr.employee' do not need redeclaration
    mobile_pro = fields.Char(string="Téléphone portable professionnel", digits=(8, 0))
    email_pro = fields.Char(string="Adresse email professionnelle", tracking=True)
    email_pers = fields.Char("Personal Email", tracking=True)
    mobile_pers = fields.Char("Personal Mobile", tracking=True)
    date_naiss = fields.Date(string="Date de Naissance", tracking=True)
    # Additional custom fields specific to Enseignant
    genre = fields.Selection([('male', 'Masculin'), ('female', 'Féminin')], string="Genre", tracking=True)
    matrimonial = fields.Selection([
        ('single', 'Célibataire'),
        ('married', 'Marié(e)'),
        ('cohabitant', 'Cohabitant(e) légal(e)'),
        ('widower', 'Veuf/Veuve'),
        ('divorced', 'Divorcé(e)')
    ], string="État matrimonial", tracking=True)
    children = fields.Integer(string="Nombre d'Enfants", tracking=True)
    lang = fields.Selection([
        ('arabic', 'Arabic'),
        ('english', 'English'),
        ('french', 'French/Français'),
    ], string="Langue", tracking=True)
    certificat = fields.Selection([
        ('graduate', 'Gradué'),
        ('bachelor', 'Licence'),
        ('master', 'Master'),
        ('doctor', 'Doctorat'),
        ('other', 'Autre'),
    ], string='Niveau de Certificat', default='doctor', tracking=True)

    study_field = fields.Char(string="Domaine d'Étude", tracking=True)
    study_school = fields.Char(string="École", tracking=True)
    emergency_contact = fields.Char(string="Nom du Contact en Cas d'Urgence", tracking=True)
    emergency_phone = fields.Char(string="Téléphone du Contact en Cas d'Urgence", tracking=True)
    km_home_work = fields.Integer(string="Distance Domicile-Travail", tracking=True)
    # time_off_ids = fields.One2many('hr.leave', 'enseignant_id', string='Demandes de Congé')
    user_id = fields.Many2one('res.users', string="Utilisateur", help="L'utilisateur Odoo lié à cet enseignant.", tracking=True)
    category_ids = fields.Many2many(
        'hr.employee.category',
        relation='hr_enseignant_category_rel',
        column1='enseignant_id',
        column2='category_id',
        string='Categories'
    )
    course_ids = fields.One2many('academy.course', 'enseignant_id', string="Cours", tracking=True)
    job_id = fields.Many2one('hr.job', string="Titre de poste", compute='_compute_job_id', store=True, readonly=True, tracking=True)

    resource_calendar_id = fields.Many2one(string="Horaire")
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade', index=True, auto_join=True, tracking=True)

    department_id = fields.Many2one('hr.department', 'Department', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=True)
    def action_open_time_off(self):
        action = self.env.ref('hr_holidays.hr_leave_action_new_request').read()[0]
        action['domain'] = [('enseignant_id', '=', self.id)]
        return action

    @api.depends('name')
    def _compute_job_id(self):
        enseignant_job_name = _('Enseignant')  # Utilisation de la fonction de traduction
        enseignant_job = self.env['hr.job'].search([('name', '=', enseignant_job_name)], )
        if not enseignant_job:
            # Création du poste 'Enseignant' s'il n'existe pas - considérez les permissions
            enseignant_job = self.env['hr.job'].create({'name': enseignant_job_name})
        for record in self:
            record.job_id = enseignant_job.id

    @api.model
    def create(self, vals):
        # Préparation des valeurs pour créer un nouvel employé
        employee_vals = {
            'name': vals.get('name'),
            'work_email': vals.get('email_pro'),
            'mobile_phone': vals.get('mobile_pro'),
            'department_id': vals.get('department_id'),
        }

        # Créez d'abord l'employé
        employee = self.env['hr.employee'].create(employee_vals)
        # Assurez-vous que `employee_id` est correctement défini pour le nouvel enseignant
        vals['employee_id'] = employee.id
        # Puis, créez l'enseignant avec le lien vers l'employé
        enseignant_record = super(Enseignant, self).create(vals)
        # Si nécessaire, liez maintenant l'enseignant à l'employé (si vous avez ajouté un champ dans hr.employee)
        employee.enseignant_id = enseignant_record.id

        return enseignant_record

    def write(self, vals):
        result = super(Enseignant, self).write(vals)
        return result




