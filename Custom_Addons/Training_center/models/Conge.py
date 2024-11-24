from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Conge(models.Model):
    _inherit = 'hr.leave'
    _description = "Congé"
    _order = 'name'

    enseignant_id = fields.Many2one('hr.enseignant', string="Enseignant Associé")

    @api.model
    def create(self, vals):
        if 'date_from' in vals:
            start_date_str = vals['date_from']
            start_date = fields.Date.from_string(start_date_str)
            if start_date < fields.Date.today():
                raise UserError("La date de début ne peut pas être antérieure à la date actuelle.")
        return super(Conge, self).create(vals)

    def write(self, vals):
        if 'date_from' in vals:
            start_date_str = vals['date_from']
            start_date = fields.Date.from_string(start_date_str)
            if start_date < fields.Date.today():
                raise UserError("La date de début ne peut pas être antérieure à la date actuelle.")
        return super(Conge, self).write(vals)
