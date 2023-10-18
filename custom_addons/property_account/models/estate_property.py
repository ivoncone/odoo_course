from odoo import models, fields, api, Command

class PropertyBalance(models.Model):

	_inherit = 'property.realstate'

	
	def action_sold(self):
		# call the super method to inherit the action sold
		sold = super(PropertyBalance, self).action_sold()
		# get partner id from property balance
		property_id = self.env['property.realstate'].browse(self.id)
		offer = property_id.offers
		partner_id = offer.partner_id
		socio = partner_id.id
		move_type = 'out_invoice'
		#get selling price
		selling_price = self.best_price 
		percentage = 0.06 #6%
		administrative_fee = 100.00
		#calculate the amount for each variable
		price = selling_price * percentage
		fee = administrative_fee
		#invoice lines 
		lines = [ 
					{
						'name': "Property Sale 6% of selling price",
						'quantity': 1,
						'price_unit': price,					
						'account_id': 1
					},
					{
						'name': "administrative Free",
						'quantity': 1,
						'price_unit': fee,
						'account_id': 1
					}
				]
		# create move
		move = self.env['account.move'].write({
				'move_type': move_type,
				'partner_id': socio,
				'journal_id': 1,
				'invoice_line_ids': [(0, 0, line) for line in lines]
			})

		print('Creando factura....')
		return sold




		