from odoo import models, fields, api


class Training(models.Model):
    _name = 'training.center'
    _inherit = ['mail.thread']
    _description = 'Training Center'

    name = fields.Char()

    description = fields.Text()
