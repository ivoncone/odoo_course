from odoo import models, fields, api, Command

class PropertyBalance(models.Model):

	_inherit = 'property.realstate'

	
	def action_sold(self):
		# call the super method to inherit the action sold
		sold = super(PropertyBalance, self).action_sold()
		# get partner id from property balance
		for record in self:
			partner_id = record.buyer_id
			move_type = 'out_invoice'
			#get selling price
			selling_price = self.selling_price
			percentage = 0.06 #6%
			fee = 100.00
			#calculate the amount for each variable
			price = selling_price * percentage
		
			# create move
			move = self.env['account.move'].create({
					'move_type': move_type,
					'partner_id': partner_id,
					'journal_id': 1,
					'invoice_line_ids': [ 
						(0, 0, {
							'name': 'property sellling price',
							'quantity': 1,
							'price_unit': price
						}),
						(0, 0, {
							'name': "administrative Free",
							'quantity': 1,
							'price_unit': fee
							})
					]

				})
		return sold




		