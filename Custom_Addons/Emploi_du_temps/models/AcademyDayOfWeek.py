from odoo import models, fields

class DayAvailability(models.Model):
    _name = 'academy.day.of.week'
    _description = 'Day of Week Availability'

    teacher_availability_id = fields.Many2one(
        'academy.teacher.availability',
        string="Teacher Availability",
        ondelete="cascade",
        help="Link to the teacher's overall availability."
    )
    day_of_week_id = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string="Day of the Week", required=True)
    start_time = fields.Float(string="Start Time", required=True, help="Start time in hours.")
    end_time = fields.Float(string="End Time", required=True, help="End time in hours.")
