from odoo import models, fields
class AcademyCourseSchedule(models.Model):
    _name = 'academy.course.schedule'
    _description = 'Course Schedule'

    course_id = fields.Many2one('academy.course', string="Course", required=True)
    start_time = fields.Datetime(string="Start Time", required=True)
    end_time = fields.Datetime(string="End Time", required=True)
    repeat = fields.Selection([
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='none', string="Repeat")
