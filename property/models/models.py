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
	def _compute_offer_count(self):
		for property_type in self:
			property_type.offer_count = len(property_type.offer_ids)

#def action to display count
	def offer_count(self):
		for record in self:
			return record.offer_count
			

class PropertyTag(models.Model):
	_name = 'property.tag'
	_description = 'tag de propiedad'
	_order = 'name'

	name = fields.Char(required=True)
	color_id = fields.Integer(string="Colors")


class RealState(models.Model):
	_name = 'property.realstate'
	_description = 'registro de propiedades'
	_order = 'id desc'
	
	name = fields.Char(required=True, default="Unknown")
	user_id = fields.Many2one('res.users', 
		index=True, tracking=True, default=lambda self: self.env.user)
	last_seen = fields.Datetime('Last Seen', 
		default=lambda self: fields.Datetime.now())
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date(string='availability date',
		default=lambda self: self._get_avaible_date(),
		)
	expected_price = fields.Float(required=True)
	selling_price = fields.Float()
	bedrooms = fields.Integer(default=2)
	tag_ids = fields.Many2many('property.tag', 'id', string='tags')
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer(string='Area de jardin', attrs={'invisible': [('garden', '=', False)]})
	garden_orientation = fields.Selection([
		('N', 'North'), 
		('E', 'East'), 
		('W', 'West'), 
		('S', 'South')], string='Garden orientation', attrs={'invisible': [('garden', '=', False)]})
	property_type_id = fields.Many2one('property.type', string='tipo')
	total_area = fields.Integer(string='Total area', compute='_get_total_area')
	best_price = fields.Float(string='Mejor oferta', 
			compute='_get_best_offer')
	offers = fields.One2many('property.offer', 'id',
			string='nuevas ofertas')
	state = fields.Selection([
		('cancel', 'Cancelled'),
		('sold', 'Sold'),
		('new', 'New'),
		('received', 'Received'),
		('available', 'Available')
		], default='available')
	active = fields.Boolean(default=True)

	_sql_constraints = [
		('unique_property_type', 'UNIQUE (property_type_id)', 'Property type must be unique'),
		('unique_tag_name', 'UNIQUE (tag_ids)', 'Tag must be unique'),
	]

	
	# on change apply to garden and orientation
	@api.onchange('garden', 'garden_area', 'garden_orientation')
	def _onchange_garden(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = 'N'
			print(garden_area)
		else:
			self.garden_area = 0
			self.garden_orientation = False


	# define available date from today to 3 month ahead
	def _get_avaible_date(self):
		today = datetime.today().date()
		three_months = today + timedelta(days=90)
		return three_months

	# compute total area
	def _get_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area

	# compute best price offer
	@api.depends("offers.price")
	def _get_best_offer(self):
		for record in self:
			if record.offers:
				record.best_price = max(record.offers.mapped('price'))
			else:
				record.best_price = 0.0

	#define action for sold and cancel
	def action_cancel_property(self):
		self.write({'state': 'cancel'})

	def action_sold(self):
		self.write({'state': 'sold'})

	
	# define constraitns
	@api.constrains('expected_price')
	def _check_expected_price_positive(self):
		for record in self:
			if record.expected_price <= 0:
				raise ValidationError("Expected price must be extricted positive and none 0.")
	
	@api.constrains('selling_price')
	def _check_selling_price_positive(self):
		for record in self:
			if record.selling_price < 0:
				raise ValidationError("Selling price must be extricted positive")
				
	@api.constrains('offers')
	def _check_offer_positive(self):
		for record in self:
			for offer in record.offers:
				if offer.price < 0:
					raise ValidationError("offer must be positive.")

	@api.constrains('property_type_id')
	def _check_unique_property_type_id(self):
		for record in self:
			tipos = self.search([(
				'property_type_id', '=', record.property_type_id.id
				)])
			if len(tipos) > 1:
				raise ValidationError("This type of property already exists.")

	@api.constrains('tag_ids')
	def _check_unique_tag_ids(self):
		for record in self:
			tag_ids = record.tag_ids.ids
			if len(tag_ids) != len(set(tag_ids)):
				raise ValidationError("You can repeat tags already existing.")

	#define prevent from delete
	@api.ondelete(at_uninstall=False)
	def _ondelete_prevent_delete(self):
		for record in self:
			if record.state not in ('new', 'cancelled'):
				raise ValidationError("You cannot delete a property that is new or has been cancelled.")


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
		self.write({'state': 'A'})
		self.partner_id = self.partner_id
		realstate = self.realstate.id
		realstate.selling_price = self.price

	def refuse(self):
		self.write({'state': 'R'})

	#define offer creation
	@api.model
	def create(self, vals):
		min_price = self.env['property.offer'].search([], order='price_unit', limit=1)
		if min_price and self.price < min_price.price_unit:
			raise ValidationError("La oferta no puede ser menor a alguna que ya existe.")
		propiedad = self.env['property.realstate'].browse(vals['id'])
		propiedad['state'] = 'received'
		return super(Offer, self).create(vals)