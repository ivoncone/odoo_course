from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime

class PropertyType(models.Model):
	_name = 'property.type'
	_description = 'tipo de propiedad'
	_order = 'name'

	name = fields.Char(required=True)
	sequence = fields.Integer('Sequence', default=1)
	property_id = fields.One2many('property.realstate', 'property_type_id', string='propiedades')
	offer_ids = fields.One2many('property.offer', 'property_type_id', string='Ofertas')
	offer_count = fields.Integer(string='Numero de ofertas', compute='_compute_offer_count', store=True)

# compute offers count
	@api.depends('offer_ids')
	def offer_count(self):
		for record in self:
			record.offer_count = len(record.offer_ids)
			self.write({'offer_count': record.offer_count})

	print(offer_count)

	def action_show_offers(self):
		action = {
			'name': 'View Offer',
			'type': 'ir.actions.act_window',
			'res_model': 'property.property_type_id',
			'view_mode': 'tree',
			'view_id': self.env.ref('property.offer_view').id,
			'res_id': self.id,
		}

		return action


			
