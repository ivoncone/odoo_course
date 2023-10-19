from odoo import models, fields, api, Command

class Excursion(models.Model):

	_inherit = 'property.realstate'

	transporte = fields.Char(string="empresa de transporte")