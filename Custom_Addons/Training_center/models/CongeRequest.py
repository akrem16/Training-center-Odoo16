from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class CongeRequest(models.Model):
    _name = 'hr.leave.request'
    _description = 'Demande de Congé'

    enseignant_id = fields.Many2one('hr.enseignant', string='Enseignant', required=True)
    type_demande = fields.Selection([
        ('conge_annuel', 'Congé Annuel'),
        ('conge_maladie', 'Congé Maladie'),
        ('conge_exceptionnel', 'Congé Exceptionnel'),
        ('conge_maternite', 'Congé Maternité'),
        ('autre', 'Autre'),
    ], string='Type de Demande', required=True)
    date_from = fields.Date(string='Début', required=True)
    date_to = fields.Date(string='Fin', required=True)
    motif = fields.Text(string='Motif')
    etat_demande = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirm', 'Confirmé'),
        ('validate', 'Approuvé'),
        ('refuse', 'Refusé'),
        ('cancel', 'Annulé')
    ], string='État de la Demande', default='draft', readonly=True)

    @api.model
    def create(self, vals):
        # Récupérer l'enseignant connecté basé sur l'utilisateur Odoo actuel
        enseignant = self.env['hr.enseignant'].search([('user_id', '=', self.env.user.id)], limit=1)
        if enseignant:
            vals['enseignant_id'] = enseignant.id
            vals['etat_demande'] = 'confirm'
        else:
            _logger.info(
                "Aucun enseignant trouvé pour l'utilisateur actuel. Vérifiez la configuration des utilisateurs et enseignants.")
        return super(CongeRequest, self).create(vals)

    def action_approve(self):
        self.write({'etat_demande': 'validate'})

    def action_refuse(self):
        self.write({'etat_demande': 'refuse'})
