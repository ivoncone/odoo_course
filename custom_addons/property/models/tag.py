from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class PropertyTag(models.Model):
	_name = 'property.tag'
	_description = 'tag de propiedad'
	_order = 'name'

	_sql_constraints = [
		('unique_tag_name', 'UNIQUE (name)', 'Tag must be unique'),
	]

	name = fields.Char(required=True)
	color_id = fields.Integer(string="Colors")