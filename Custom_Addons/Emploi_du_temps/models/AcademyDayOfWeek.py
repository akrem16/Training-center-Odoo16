from odoo import models, fields, api

class DayAvailability(models.Model):
    _name = 'academy.day.of.week'
    _description = 'Day of Week Availability'

    teacher_availability_id = fields.Many2one(
        'academy.teacher.availability',
        string="Teacher Availability",
        ondelete="cascade",
        help="Link to the teacher's overall availability."
    )

    enseignant_id = fields.Many2one('hr.enseignant', string="Teacher")

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

    # Ajout des champs start_datetime et end_datetime
    start_datetime = fields.Datetime(string="Start Datetime", compute="_compute_start_datetime")
    end_datetime = fields.Datetime(string="End Datetime", compute="_compute_end_datetime")

    @api.depends('day_of_week_id', 'start_time', 'end_time')
    def _compute_start_datetime(self):
        for record in self:
            if record.day_of_week_id and record.start_time:
                start_datetime = fields.Datetime.now().replace(hour=int(record.start_time), minute=0, second=0, microsecond=0)
                record.start_datetime = start_datetime

    @api.depends('day_of_week_id', 'end_time')
    def _compute_end_datetime(self):
        for record in self:
            if record.day_of_week_id and record.end_time:
                end_datetime = fields.Datetime.now().replace(hour=int(record.end_time), minute=0, second=0, microsecond=0)
                record.end_datetime = end_datetime
