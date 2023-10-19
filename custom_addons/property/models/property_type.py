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
	offer_count = fields.Integer(string='  Total de ofertas', compute='_get_best_offer', store=True)

	
	# compute offers count
	def _get_offer_count(self):
		tipo = self.name
		offers_with_same_type = self.env['property.offer'].search([('property_type_id', '=', tipo)])
		count = len(offers_with_same_type)
		self.write({'offer_count': count})

	def show_offers(self):
		self._get_offer_count()
		tipo = self.name
		domain = [('property_type_id', '=', tipo)]
		return {
			'type': 'ir.actions.act_window',
			'name': 'Offer Count',
			'res_model': 'property.offer',
			'view_mode': 'tree',
			'domain': domain
		}



			
