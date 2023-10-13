from odoo import models, fields

class PropertyBalance(models.Model):
	_name = 'property.balance'
	_description = 'Realstate Balance Account'
	


	amount = fields.Float()