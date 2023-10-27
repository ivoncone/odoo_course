# -*- coding: utf-8 -*-
# from odoo import http


# class Desechos(http.Controller):
#     @http.route('/desechos/desechos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/desechos/desechos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('desechos.listing', {
#             'root': '/desechos/desechos',
#             'objects': http.request.env['desechos.desechos'].search([]),
#         })

#     @http.route('/desechos/desechos/objects/<model("desechos.desechos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('desechos.object', {
#             'object': obj
#         })
