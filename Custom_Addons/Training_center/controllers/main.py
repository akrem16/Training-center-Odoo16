# from odoo import http
# from odoo.http import request
#
# class EnseignantCongeController(http.Controller):
#     @http.route('/enseignant/conge', auth='user', type='json', methods=['POST'])
#     def create_conge_for_enseignant(self, enseignant_id, status_conge_id, date_from, date_to, **kwargs):
#         # Assurez-vous que l'utilisateur a les droits nécessaires pour créer une demande de congé
#         Enseignant = request.env['hr.enseignant'].sudo()
#         Leave = request.env['hr.leave'].sudo()
#
#         enseignant = Enseignant.browse(enseignant_id)
#         if not enseignant.exists():
#             return {'error': 'Enseignant non trouvé'}
#
#         # Assurez-vous que l'ID de l'enseignant est correctement mappé à un employé
#         if not enseignant.employee_id:
#             return {'error': 'Aucun employé associé à cet enseignant'}
#
#         demande_conge = Leave.create({
#             'name': 'Congé Personnel',
#             'employee_id': enseignant.employee_id.id,  # Utilisez employee_id de l'enseignant
#             'enseignant_id': enseignant.id,
#             'holiday_status_id': status_conge_id,
#             'date_from': date_from,
#             'date_to': date_to,
#         })
#
#         return {'success': 'Demande de congé créée avec succès', 'demande_conge_id': demande_conge.id}
