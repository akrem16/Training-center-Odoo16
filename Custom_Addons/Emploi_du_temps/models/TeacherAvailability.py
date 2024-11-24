from odoo import models, fields, api


class TeacherAvailability(models.Model):
    _name = 'academy.teacher.availability'
    _description = 'Teacher Availability'

    name = fields.Char(string="Enseignant")
    enseignant_id = fields.Many2one('hr.enseignant', string="Teacher")
    booking = fields.Datetime(string="Booking Date and Time", help="Date and time of the booking.")
    course_schedule_id = fields.Many2one('academy.course.schedule', string="Course Schedule")
    classroom_id = fields.Many2one('academy.classroom', string="Classroom")  # Link to Classroom
    course_id = fields.Many2one('academy.course', string="Course")  # Assuming a Course model

    @api.onchange('enseignant_id')
    def _onchange_enseignant_id(self):
        if self.enseignant_id:
            # Mettre à jour le champ name avec le nom de l'enseignant sélectionné
            self.name = self.enseignant_id.name
        else:
            # Réinitialiser le champ name si aucun enseignant n'est sélectionné
            self.name = ''


        @api.onchange('booking')
        def _onchange_booking(self):
            if self.booking and self.course_schedule_id:
                self.course_schedule_id.start_time = self.booking
