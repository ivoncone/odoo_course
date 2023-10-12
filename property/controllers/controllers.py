# -*- coding: utf-8 -*-
# from odoo import http


# class Property(http.Controller):
#     @http.route('/property/property', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property/property/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('property.listing', {
#             'root': '/property/property',
#             'objects': http.request.env['property.property'].search([]),
#         })

#     @http.route('/property/property/objects/<model("property.property"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property.object', {
#             'object': obj
#         })
