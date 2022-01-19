# -*- coding: utf-8 -*-
# from odoo import http


# class TravelUmroh(http.Controller):
#     @http.route('/travel__umroh/travel__umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel__umroh/travel__umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel__umroh.listing', {
#             'root': '/travel__umroh/travel__umroh',
#             'objects': http.request.env['travel__umroh.travel__umroh'].search([]),
#         })

#     @http.route('/travel__umroh/travel__umroh/objects/<model("travel__umroh.travel__umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel__umroh.object', {
#             'object': obj
#         })
