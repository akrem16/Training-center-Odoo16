# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Enseignant(models.Model):
    _name = "hr.enseignant"
    _description = "training center"
    _order = 'name'

    name = fields.Char(string="Nom enseignant", required=True)

    mobile_pro = fields.Char(string="Téléphone portable professionnel", required=True, digits=(8, 0))
    mobile_pers = fields.Char(string="Téléphone portable", required=True, digits=(8, 0))
    email_pro = fields.Char(string="Adresse email professionnelle", required=True)
    email_pers = fields.Char(string="Adresse email", required=True)

    genre = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    matrimonial = fields.Selection([
        ('single', 'Célibataire'),
        ('married', 'Marié(e)'),
        ('cohabitant', 'Cohabitant(e) légal(e)'),
        ('widower', 'Veuf/Veuve'),
        ('divorced', 'Divorcé(e)')
    ], string="matrimonial(e)")
    children = fields.Integer(string="Nombre d'Enfants")
    lang = fields.Selection([
        ('arabic', 'arabic'),
        ('english', 'English'),
        ('french', 'French/Français'),
    ])
    certificat = fields.Selection([
        ('graduate', 'Gradué'),
        ('bachelor', 'Licence'),
        ('master', 'Master'),
        ('doctor', 'Doctorat'),
        ('other', 'Autre'),
    ], 'Niveau de Certificat', default='other')

    date_naiss = fields.Date(string="Date de naissance")
    address = fields.Char(string="Adresse")
    experience = fields.Integer(string="Expérience (en années)")
    contract_start_date = fields.Date(string="Date de début du contrat")
    contract_end_date = fields.Date(string="Date de fin du contrat")
    contract_type = fields.Selection([
        ('full_time', 'Temps plein'),
        ('part_time', 'Temps partiel'),
    ], string="Type de Contrat")
    bank_account = fields.Char(string="Numéro de compte bancaire")
    image = fields.Image()
    # Champ Many2one pour lier à l'employé
    employee_id = fields.Many2one('hr.employee', string='Enseignant')

    study_field = fields.Char(string="Domaine d'Étude")
    study_school = fields.Char(string="École")
    emergency_contact = fields.Char(string="Nom du Contact en Cas d'Urgence")
    emergency_phone = fields.Char(string="Téléphone du Contact en Cas d'Urgence")
    km_home_work = fields.Integer(string="Distance Domicile-Travail")

    country_id = fields.Many2one('res.country', string='Pays')
    identification_id = fields.Char("Identifiant")
    passport_id = fields.Char("Numéro de Passeport")
    place_of_birth = fields.Char("Lieu de Naissance")
    country_of_birth = fields.Many2one('res.country', string='Pays de Naissance')
    time_off_ids = fields.One2many('hr.leave', 'enseignant_id', string='Demandes de Congé')
    user_id = fields.Many2one('res.users', string="Utilisateur", help="L'utilisateur Odoo lié à cet enseignant.")

    # Action pour ouvrir les demandes de congé
    def action_open_time_off(self):
        action = self.env.ref('hr_holidays.hr_leave_action_new_request').read()[0]
        action['domain'] = [('employee_id', '=', self.employee_id.id)]
        return action

