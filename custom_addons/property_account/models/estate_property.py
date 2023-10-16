from odoo import models, fields, api, Command

class PropertyBalance(models.Model):

	_inherit = 'property.realstate'

	partner_id = fields.Many2one('res.partner', string='Partner id')
	account_id = fields.Many2one('account.account', string='Account')
	
	def action_sold(self):
		# call the super method to inherit the action sold
		sold = super(PropertyBalance, self).action_sold()
		# get partner id from property balance
		partner_id = self.partner_id
		account_id = self.account_id.id
		print('hello ivonne this is your account id '+str(account_id))
		#create account move
		move_type = 'out_invoice'
		#get selling price
		selling_price = self.best_price 
		percentage = 0.06 #6%
		administrative_fee = 100.00

		#calculate the amount for each variable
		price = selling_price * percentage
		fee = administrative_fee

		#define new lines for invoice
		line1 = {
			'name': 'Property Price (6%)',
						'quantity': 1,
						'price_unit': price

		}
		line2 = {
			'name': 'Administrative Fees',
						'quantity': 1,
						'price_unit': fee
		}
		# create custom invoice lines
		self.env['account.move'].create(
			{
				'move_type': move_type,
				'partner_id': partner_id,
				'journal_id': 1,
				'line_ids': [
					Command.create({
						'name': 'Administrative Fees',
						'quantity': 1,
						'price_unit': price,
						})
				]
			},
		)
		self.env
		print('creando factura....')
		return sold




		