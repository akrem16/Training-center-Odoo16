from odoo import models, fields, api

class Training(models.Model):
    _name = 'training.center'
    _inherit = ['mail.thread']
    _description = 'Training Center'

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    address = fields.Char(string="Address", required=True, tracking=True)
    phone = fields.Char(string="Phone", required=True, tracking=True)
    mobile = fields.Char(string="Mobile", required=True, tracking=True)
    email = fields.Char("Email", tracking=True)
    site = fields.Char("Site Web", tracking=True)


