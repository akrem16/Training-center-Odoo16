from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'
    enseignant_id = fields.Many2one('hr.enseignant', string="Enseignant associé", help="L'enseignant associé à cet utilisateur.")
