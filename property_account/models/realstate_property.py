from odoo import api, models 

class RealstateProperty(models.Model):
	_inherit = 'property.realstate'

	def action_sold(self):
		move_obj = self.env['account.move']
		user_id = self.user_id

		values = {
			'user_id': user_id.id;
			'move_type': 'out_invoice',
		}
		new_move = move_obj.create(values)
		selling_price = self.price 
		invoice_line_1 = {
			'name': 'Property Sale (6% of selling price)',
			'quantity': 1,
			'price_unit': selling_price * 0.6,
		}

		invoice_line_2 = {
			'name': 'Administrative fees',
			'quantity': 1,
			'price_unit': 100.00
		}

		new_move.write({
			'invoice_line_ids': [(0,0, invoice_line_1) (0,0, invoice_line_2)]
			})
        return super(RealStateProperty, self).action_sold()