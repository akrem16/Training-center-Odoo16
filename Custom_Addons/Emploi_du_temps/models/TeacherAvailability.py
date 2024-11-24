from odoo import models, fields

class TeacherAvailability(models.Model):
    _name = 'academy.teacher.availability'
    _description = 'Teacher Availability'

    enseignant_id = fields.Many2one(
        'hr.enseignant',
        string="Teacher",
        help="Link to the teacher's record."
    )
    day_availabilities = fields.One2many(
        'academy.day.of.week',
        'teacher_availability_id',
        string="Daily Availabilities",
        help="Teacher's availability throughout the week."
    )
