# from odoo import http
# from odoo.http import request
#
# class CongeController(http.Controller):
#
#     @http.route('/submit_leave_request', type='http', auth="user", website=True)
#     def submit_leave_request(self, **post):
#         enseignant_id = int(post.get('enseignant_id'))
#         date_from = post.get('date_from')
#         date_to = post.get('date_to')
#         # Autres champs de la demande de congé
#
#         hr_leave = request.env['hr.leave'].create({
#             'enseignant_id': enseignant_id,
#             'date_from': date_from,
#             'date_to': date_to,
#             # Autres champs de la demande de congé
#         })
#
#         return request.render('votre_module.confirmation_template', {
#             'hr_leave': hr_leave,
#         })
