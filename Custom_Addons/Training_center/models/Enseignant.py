import re
from random import choice
from string import digits

from odoo import api, fields, models, _
from odoo.odoo.exceptions import ValidationError, UserError



class Enseignant(models.Model):
    _name = "hr.enseignant"
    _inherit = ['hr.employee', 'mail.thread']
    _description = "Enseignant"
    _order = 'name'
    reference = fields.Char(string='Reference', required=True, tracking=True, copy=False, readonly=True,
                            default=lambda self: ('New'))
    matricule = fields.Char(string='CIN', tracking=True, required=True)
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
    time_off_ids = fields.One2many('hr.leave', 'enseignant_id', string='Demandes de Congé')
    user_id = fields.Many2one('res.users', string="Utilisateur", help="L'utilisateur Odoo lié à cet enseignant.",
                              tracking=True)
    category_ids = fields.Many2many(
        'hr.employee.category',
        relation='hr_enseignant_category_rel',
        column1='enseignant_id',
        column2='category_id',
        string='Categories'
    )
    course_ids = fields.One2many('academy.course', 'enseignant_id', string="Cours", tracking=True)
    job_id = fields.Many2one('hr.job', string="Titre de poste", compute='_compute_job_id', store=True, readonly=True,
                             tracking=True)

    resource_calendar_id = fields.Many2one(string="Horaire")
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade', index=True,
                                  auto_join=True, tracking=True)
    # image_1920 = fields.Image("Image de Profil")
    department_id = fields.Many2one('hr.department', 'Department',
                                    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                    tracking=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('barcode_uniq', 'unique (barcode)',
         "The Badge ID must be unique, this one is already assigned to another employee."),
        ('user_uniq', 'unique (user_id, company_id)',
         "A user cannot be linked to multiple employees in the same company.")
    ]

    def action_open_time_off(self):
        # action = self.env.ref('hr_holidays.hr_leave_action_new_request').read()[0]
        # action['domain'] = [('employee_id', '=', self.id)]
        # return action
        return {
            'name': _('Time Off Dashboard'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'views': [[self.env.ref('hr_holidays.hr_leave_employee_view_dashboard').id, 'calendar']],
            'domain': [('employee_id', 'in', self.ids)],
            'context': {
                'employee_id': self.ids,
            },
        }

    @api.depends('name')
    def _compute_job_id(self):
        # Utilisez des noms fixes pour le débogage, sans traduction
        enseignant_job_name = 'Enseignant'
        enseignant_job = self.env['hr.job'].search([('name', '=', enseignant_job_name)], limit=1)
        if not enseignant_job:
            enseignant_job = self.env['hr.job'].create(
                {'name': enseignant_job_name, 'enseignant_job': enseignant_job.id})

        for record in self:
            record.job_id = enseignant_job.id

    @api.model
    def create(self, vals):

        # Validation du matricule
        if 'matricule' in vals:
            matricule = vals['matricule']
            if not matricule.isdigit() or len(matricule) != 8:
                raise ValidationError(_("Le matricule doit contenir exactement 8 chiffres."))

        # Génération d'une nouvelle référence si nécessaire
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hr.enseignant') or _('New')

        # Préparer les valeurs pour créer un nouvel hr.employee lié
        employee_vals = {
            'name': vals.get('name'),
            'job_id': vals.get('job_id'),
            'work_email': vals.get('work_email'),
            'mobile_phone': vals.get('mobile_phone'),
            'department_id': vals.get('department_id'),
            'job_title': vals.get('job_title'),
            'image_1920': vals.get('image_1920'),
            # Assurez-vous que cette valeur est correctement formatée si elle est utilisée
        }

        # Créer l'enregistrement hr.employee
        employee = self.env['hr.employee'].create(employee_vals)

        # S'assurer que employee_id est correctement défini pour le nouvel enseignant
        vals['employee_id'] = employee.id

        # Créer l'enregistrement enseignant lié à l'employé
        enseignant_record = super(Enseignant, self).create(vals)

        # Lier l'employé à l'enseignant créé
        employee.enseignant_id = enseignant_record.id  # Ligne ajoutée pour résoudre le problème

        return enseignant_record

    def write(self, vals):

        if 'matricule' in vals and (not vals['matricule'].isdigit() or len(vals['matricule']) != 8):
            raise ValidationError(_("Le matricule doit contenir exactement 8 chiffres."))

        result = super(Enseignant, self).write(vals)

        if 'name' in vals:
            self.employee_id.name = vals['name']
        if 'job_id' in vals:
            self.employee_id.name = vals['job_id']
        if 'work_email' in vals:
            self.employee_id.work_email = vals['work_email']
        if 'mobile_phone' in vals:
            self.employee_id.mobile_phone = vals['mobile_phone']
        if 'department_id' in vals:
            self.employee_id.department_id = vals['department_id']
        if 'job_title' in vals:
            self.employee_id.image_1920 = vals['job_title']
        if 'image_1920' in vals:
            self.employee_id.image_1920 = vals['image_1920']
        return result

    def unlink(self):
        # Collecte tous les IDs d'employés associés aux enseignants à supprimer
        employee_ids = self.mapped('employee_id')

        # Pour chaque employé, trouve et supprime les lignes de CV correspondantes
        # for employee in employee_ids:
        #     resume_lines = self.env['hr.resume.line'].search([('employee_id', '=', employee.id)])
        #     resume_lines.unlink()

        # Suppression des enseignants
        res = super(Enseignant, self).unlink()

        # Ensuite, supprime les employés correspondants
        employee_ids.unlink()
        return res

    def generate_random_barcode(self):
        for enseignant in self:
            enseignant.barcode = '058' + "".join(choice(digits) for i in range(9))

    _sql_constraints = [
        ('CIN_name_unique',
         'unique(matricule)',
         'CIN doit être unique')
    ]

    def toggle_active(self):
        for record in self:
            record.active = not record.active
            if record.employee_id:
                record.employee_id.sudo().write({'active': record.active})

    @api.constrains('mobile_phone')
    def _check_mobile_phone(self):
        for enseignant in self:
            if enseignant.mobile_phone and (
                    not re.match("^[0-9]*$", enseignant.mobile_phone) or len(enseignant.mobile_phone) != 8):
                raise ValidationError(_("Le numéro de téléphone mobile doit contenir exactement 8 chiffres."))



