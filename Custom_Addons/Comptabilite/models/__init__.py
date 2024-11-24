from . import CompteComptable
from odoo import models, fields, api

class CompteComptable(models.Model):
    _name = 'compte.comptable'
    _description = 'Compte Comptable'

    name = fields.Char(string='Nom', required=True)
    code = fields.Char(string='Code', required=True)
    # Autres champs nécessaires

class JournalComptable(models.Model):
    _name = 'journal.comptable'
    _description = 'Journal Comptable'

    name = fields.Char(string='Nom', required=True)
    type = fields.Selection([('sale', 'Vente'), ('purchase', 'Achat'), ('general', 'Général')], string='Type', required=True)
    # Autres champs nécessaires

# Définir les autres modèles (EntréeComptable, LigneEcritureComptable, PériodeComptable, etc.)


