from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime

class PropertyType(models.Model):
	_name = 'property.type'
	_description = 'tipo de propiedad'
	_order = 'name'

	name = fields.Char()
	sequence = fields.Integer('Sequence', default=1)
	property_id = fields.One2many('property.realstate', 'property_type_id', string='propiedades')
	offer_ids = fields.One2many('property.offer', 'property_type_id', string='Ofertas')
	offer_count = fields.Integer(string='Numero de ofertas')

	
	# compute offers count
	def _get_offer_count(self):
		tipo = self.name
		offers_with_same_type = self.env['property.offer'].search([('property_type_id', '=', tipo)])
		count = len(offers_with_same_type)
		print(f"propertty_type_id {tipo}: {count} items")

	def show_offers_count(self):
		self._get_offer_count()
		count = self.offer_count
		message = f'Las ofertas son: {count}'
		return {
			'type': 'ir.actions.act_window',
			'name': 'Offer Count',
			'res_model': 'property.offer',
			'view_mode': 'tree',
			'res_id': self.id,
			'context': {'default_name': message}
		}



			
