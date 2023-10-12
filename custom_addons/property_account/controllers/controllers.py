# -*- coding: utf-8 -*-
# from odoo import http


# class PropertyAccount(http.Controller):
#     @http.route('/property_account/property_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/property_account/property_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('property_account.listing', {
#             'root': '/property_account/property_account',
#             'objects': http.request.env['property_account.property_account'].search([]),
#         })

#     @http.route('/property_account/property_account/objects/<model("property_account.property_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('property_account.object', {
#             'object': obj
#         })
