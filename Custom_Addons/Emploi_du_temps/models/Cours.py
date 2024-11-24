from datetime import timedelta
from odoo import models, fields, api
import logging


class Cours(models.Model):
    _inherit = 'academy.course'

    classroom_id = fields.Many2one('academy.classroom', string="Classroom")
    schedule_ids = fields.One2many('academy.course.schedule', 'course_id', string="Schedule")

@api.model
def generate_timetable(self):
    courses_to_schedule = self.env['academy.course'].search([('schedule_ids', '=', False)])
    for course in courses_to_schedule:
        # Simplification : trouver le premier enseignant disponible
        available_teacher = self.env['academy.teacher.availability'].search([], limit=1)
        if available_teacher:
            # Simplification : trouver la première salle de classe disponible
            available_classroom = self.env['academy.classroom'].search([], limit=1)
            if available_classroom:
                # Simplification : fixer l'heure de début et de fin du cours
                start_datetime = fields.Datetime.now()
                end_datetime = start_datetime + timedelta(hours=2)  # Par exemple, chaque cours dure 2 heures

                # Création du schedule pour le cours
                self.env['academy.course.schedule'].create({
                    'course_id': course.id,
                    'start_time': start_datetime,
                    'end_time': end_datetime,
                    # 'repeat': 'none', ou selon les besoins
                })
                # Assumer que le cours est attribué à l'enseignant et à la salle de classe
                course.write({
                    'teacher_id': available_teacher.enseignant_id.id,
                    'classroom_id': available_classroom.id,
                })
