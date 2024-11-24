from odoo import models, fields, api, _

import logging

from odoo.addons.google_recaptcha.models.ir_http import logger
from odoo.odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CoursSession(models.Model):
    _name = 'academy.course.session'
    _inherit = 'mail.thread'
    _description = 'Session de Cours'

    name = fields.Char(string="Titre de la Session", required=True)
    start_date = fields.Date(string="Date de Début", default=fields.Date.today)
    end_date = fields.Date(string="Date de Fin")
    enseignant_id = fields.Many2one('hr.enseignant', string='Enseignant', required=True, tracking=True)
    seats = fields.Integer(string="Nombre de Places")
    taken_seats = fields.Float(string="Places Occupées", compute='_compute_taken_seats')
    course_id = fields.Many2one('academy.course', string="Cours Associé", required=True)
    attendee_ids = fields.One2many('hr.etudiant', 'session_id', string="Participants")
    active = fields.Boolean(string='Active', default=True, tracking=True)

    state = fields.Selection(
        [('draft', 'Brouillon'), ('full', 'Places Complètes'), ('in_progress', 'En cours'), ('completed', 'Terminé'),
         ('cancel', 'Annulé')
         ], string='Status', readonly=False, tracking=True, default='draft', copy=False)

    session_count = fields.Integer(string='Nombre de Sessions', compute='_compute_session_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
                if r.taken_seats >= 100:
                    r.state = 'full'
                elif r.state == 'full' and r.taken_seats < 100:
                    r.state = 'draft'
    def action_set_in_progress(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'full'

    @api.onchange("start_date", "end_date", "seats", "attendee_ids")
    def _onchange_verify_valid_seats(self):
        self._compute_taken_seats()
        if self.seats < 0:
            return {
                "warning": {
                    "title": "Valeur incorrecte de 'seats'",
                    "message": "Le nombre de places disponibles ne peut pas être négatif"
                }
            }
        if self.start_date and fields.Date.from_string(self.start_date) < fields.Date.today():
            return {
                "warning": {
                    "title": "Date de début invalide",
                    "message": "La date de début ne peut pas être inférieure à la date actuelle."
                }
            }
        if self.start_date and self.end_date and fields.Date.from_string(self.end_date) < fields.Date.from_string(
                self.start_date):
            return {
                "warning": {
                    "title": "Date de fin invalide",
                    "message": "La date de fin ne peut pas être inférieure à la date de début."
                }
            }

    def action_cancel(self):
        for record in self:
            logger.error(f"CoursSession {record.name} state moved to Cancelled by {self.env.user.name}")
            record.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        if 'start_date' in vals:
            start_date_str = vals['start_date']
            try:
                start_date = fields.Date.from_string(start_date_str)
            except ValueError:
                raise UserError(_("Le format de la date de début n'est pas valide."))

            if start_date == fields.Date.today():
                vals['state'] = 'in_progress'

        if 'end_date' in vals:
            end_date_str = vals['end_date']
            try:
                end_date = fields.Date.from_string(end_date_str)
            except ValueError:
                raise UserError(_("Le format de la date de fin n'est pas valide."))

            if end_date == fields.Date.today():
                vals['state'] = 'completed'

        session = super(CoursSession, self).create(vals)
        return session

    def write(self, vals):
        res = super(CoursSession, self).write(vals)
        if 'start_date' in vals and vals['start_date'] == fields.Date.today():
            self.filtered(lambda r: r.state != 'completed').write({'state': 'in_progress'})
        if 'end_date' in vals and vals['end_date'] == fields.Date.today():
            self.filtered(lambda r: r.state not in ['completed', 'cancel']).write({'state': 'completed'})
        return

    @api.model
    def get_sessions_by_course(self):
        query = """
                SELECT course_id, COUNT(id) as session_count
                FROM academy_course_session
                GROUP BY course_id
            """
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        return result


    def unlink(self):
        for record in self:
            if record.state == 'full':
                record.state = 'draft'  # Réinitialiser le statut si des places sont libérées
        return super(CoursSession, self).unlink()












