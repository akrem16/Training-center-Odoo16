from odoo import models, fields, api


class Classroom(models.Model):
    _name = 'academy.classroom'
    _description = 'Classroom'

    name = fields.Char(string="Classe")
    capacity = fields.Integer(string="Capacity", default=15)
    equipment_ids = fields.Many2many('academy.equipment', string="Equipment")
    booking_datetime = fields.Datetime(string="Date et heure de réservation")
    enseignant_id = fields.Many2one('hr.enseignant', string="Foramteur")
    course_id = fields.Many2one('academy.course', string="Cours")

    duration = fields.Float(string="Durée (heures)")
    classroom_name_id = fields.Many2one('academy.classroom.name', string="Classroom Name")

    teacher_availability_ids = fields.One2many(
        'academy.teacher.availability', 'classroom_id', string="Teacher Availabilities")

    # Champ calculé pour la coloration
    booking_status = fields.Selection(
        selection=[('past', 'Past'), ('future', 'Future')],
        compute='_compute_booking_status',
        store=True
    )

    @api.onchange('classroom_name_id')
    def _onchange_class_id(self):
        if self.classroom_name_id:
            # Mettre à jour le champ name avec le nom de l'enseignant sélectionné
            self.name = self.classroom_name_id.name
        else:
            # Réinitialiser le champ name si aucun enseignant n'est sélectionné
            self.name = ''

    @api.depends('booking_datetime')
    def _compute_booking_status(self):
        for record in self:
            if record.booking_datetime:
                record.booking_status = 'past' if record.booking_datetime < fields.Datetime.now() else 'future'
            else:
                record.booking_status = 'future'  # ou 'past', selon ce qui est logique pour votre application

class Classname(models.Model):
    _name = 'academy.classroom.name'
    _description = 'Classroom'

    name = fields.Char(string="Name")



