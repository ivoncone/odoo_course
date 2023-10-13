from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime

class Offer(models.Model):
	_name = 'property.offer'
	_description = 'registro de ofertas a propiedades'
	_order = 'price desc'

	price = fields.Float()
	state = fields.Selection([('A', 'Accepted'), ('R', 'Refused')])
	partner_id = fields.Many2one('res.partner', string='Partner')
	validity = fields.Integer(default=7)
	date_deadline = fields.Date(string='Vencimiento de oferta', 
		compute='_get_deadline', inverse='_inverse_date_deadline')
	property_id = fields.Many2one('property.realstate', 
		string='id de propiedad')
	property_type_id = fields.Many2one('property.type',
		related='property_id.property_type_id', 
		string='tipo de propiedad', 
		store=True)

	# define date deadline expiration
	def _get_deadline(self):
		for record in self:
			if record.create_date and record.validity:
				record.date_deadline = record.create_date + timedelta(days=record.validity)
			else:
				record.date_deadline = False 

	def _inverse_date_deadline(self):
		for record in self:
			if record.date_deadline and record.create_date:
				delta = record.date_deadline - record.create_date
				record.validity = delta.days

	# define refuse and accept actions
	def accept_offer(self):
		selling_price = property_id.selling_price
		self.write({'state': 'A',
					'partner_id': 'partner_id',
					'property_id': 'property_id',
					'selling_price': 'price'})

	def refuse(self):
		self.write({'state': 'R'})

	# define create offer with condition price not lower than minimun offer in data
	@api.model
	def create(self, vals):
		price = vals.get('price')
		min_price = self.env['property.offer'].search([]).mapped('price')
		if min_price:
			min_amount = min(min_price)
			if price < min_amount:
				raise ValidationError("N puedes crear una oferta menor a una ya ofertada.")
			return super(Offer, self).create(vals)

	