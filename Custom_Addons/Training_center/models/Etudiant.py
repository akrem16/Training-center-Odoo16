from odoo import models, fields , api


class Etudiant(models.Model):
    _name = 'hr.etudiant'

    # Champs spécifiques à l'étudiant
    name = fields.Char(string="Nom Etudiant", required=True)
    matricule = fields.Char(string='Matricule', required=True)
    date_inscription = fields.Date(string="Date d'inscription")
    # promotion_id = fields.Many2one('hr.promotion', string="Promotion")
    resultat_examen = fields.Float(string="Résultat de l'examen")
    adresse = fields.Text(string="Adresse")

    # Informations personnelles
    prenom_etudiant = fields.Char(string="Prénom", store=True)
    date_naissance = fields.Date(string="Date de naissance",store=True)
    genre = fields.Selection([('male', 'Masculin'), ('female', 'Féminin')], string="Genre",
                             store=True)
    email = fields.Char(string="Email", store=True)
    telephone = fields.Char(string="Téléphone", store=True)
    image = fields.Image()

