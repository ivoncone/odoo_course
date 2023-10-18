from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

from datetime import timedelta, datetime

class Offer(models.Model):
	_name = 'property.offer'
	_description = 'registro de ofertas a propiedades'
	_order = 'price desc'

	price = fields.Float()
	state = fields.Selection([('A', 'Accepted'), ('R', 'Refused')])
	is_accepted = fields.Boolean()
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

	# Invisible accept and refused buttons 
	@api.onchange('is_accepted', 'state')
	def _set_is_accepted(self):
		for record in self:
			if record.state == 'Accepted' or 'A':
				self.write({
					'is_accepted': True
					})

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
		self.write({'state': 'A',
					'partner_id': self.partner_id,
					'property_id': self.property_id,
					'price': price})

	def refuse(self):
		self.write({'state': 'R'})

	
	@api.constrains('price', 'property_id')
	def _create_offer(self):
		for record in self:
			if record.price < min(self.search([('id', '!=', record.property_id)]).mapped('price')):
				raise ValidationError("Oferta no puede ser agregada.")
	
		

	