from odoo import models, fields, api

class DesechosUnitPrice(models.Model):

	_inherit = 'stock.scrap'

	costo = fields.Float(string='Costo', compute='_get_unit_cost')

	def _get_unit_cost(self):
		for record in self:
			product_info = self.product_id.id
			producto = self.env['product.product'].search([('id','=',product_info)])
			record.costo = producto.standard_price


