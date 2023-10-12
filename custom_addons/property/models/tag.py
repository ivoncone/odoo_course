from odoo import fields, models, api
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class PropertyTag(models.Model):
	_name = 'property.tag'
	_description = 'tag de propiedad'
	_order = 'name'

	name = fields.Char(required=True)
	color_id = fields.Integer(string="Colors")