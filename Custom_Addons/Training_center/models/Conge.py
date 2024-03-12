from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Conge(models.Model):
    _name = "hr.conge"
    _inherit = 'hr.leave'
    _description = "Congé"
    _order = 'name'

    enseignant_id = fields.Many2one('hr.enseignant', string="Enseignant Associé")

    @api.model
    def create(self, vals):
        # Get the connected teacher based on the current Odoo user
        enseignant = self.env['hr.enseignant'].search([('user_id', '=', self.env.user.id)], limit=1)
        if enseignant:
            vals['employee_id'] = enseignant.employee_id.id
        else:
            _logger.info("No Enseignant found for the current user. Check the user and Enseignant configurations.")
        return super(Conge, self).create(vals)
