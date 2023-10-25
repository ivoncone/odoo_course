from odoo import fields, models, api
from odoo.exceptions import ValidationError

from dateutil.relativedelta import relativedelta

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
			if record.state == 'A':
				self.write({
					'is_accepted': True
					})

	# define date deadline expiration
	@api.depends('create_date', 'validity')
	def _get_deadline(self):
		for record in self:
			date = record.create_date.date() if record.create_date else fields.Date.today()
			record.date_deadline = date + relativedelta(days=record.validity)

	def _inverse_date_deadline(self):
		for record in self:
			date = record.create_date.date() if record.create_date else fields.Date.today()
			record.validity = (record.date_deadline - date).days

	# define refuse and accept actions
	def accept_offer(self):
		if 'A' in self.mapped('property_id.offers.state'):
			raise ValidationError('Una oferta ya ha sido aceptada')
		self.write({'state': 'A'})
		return self.mapped('property_id').write(
				{
				'state': 'offer_accepted',
				'selling_price': self.price,
				'buyer_id': self.partner_id.id,
				}
			)

	def refuse(self):
		self.write({'state': 'R'})

	
	@api.constrains('price')
	def _create_offer(self):
		for record in self:
			offers = self.search([('id', '!=', record.id), ('property_id', '=', record.property_id.id)])
			for offer in offers:
				if offer.price > record.price: 
					raise ValidationError("Oferta no puede ser menor a una ya ofertada.")
	
		

	