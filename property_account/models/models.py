from odoo import models, fields

class PropertyAccount(models.Model):
	_name = 'property.accout'
	_description = 'Realstate accout'

	property_id = fields.Many2one('property.realstate', string='Propiedad')
	partner_id = fields.Many2one('res.partner', string='Cuenta')