from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http, _

class WeblearnsTeacherPortal(CustomerPortal):

    @http.route(["/new/teacher"], type="http", methods=["POST", "GET"], auth="user", website=True)
    def registerTeacherProfile(self, **kw):
        subject_list = request.env['academy.subject'].search([])
        vals = {'subjects': subject_list, 'page_name': "register_teacher"}
        if request.httprequest.method == "POST":
            print(kw)
            error_list = []
            if not kw.get("name"):
                error_list.append(_("Name field is mandatory."))
            if not kw.get("subject"):
                error_list.append(_("Subject field is mandatory."))
            if not kw.get("subject").isdigit():
                error_list.append(_("Invalid subject field."))
            elif not request.env['academy.subject'].search([('id', '=', int(kw.get("subject")))]):
                error_list.append(_("Invalid subject field selected value."))
            elif not error_list:
                request.env['hr.enseignant'].create({
                    "name": kw.get("name"),
                    "subject_ids": [(6, 0, [int(kw.get("subject"))])]
                })
                success = _("Successfully registered teacher!")
                vals['success_msg'] = success
            else:
                vals['error_list'] = error_list
        else:
            print("GET Method..........")

        return request.render("your_module.new_teacher_form_view_portal", vals)

    def _prepare_home_portal_values(self, counters):
        rtn = super(WeblearnsTeacherPortal, self)._prepare_home_portal_values(counters)
        rtn['teacher_counts'] = request.env['hr.enseignant'].search_count([])
        return rtn

    @http.route(['/my/teachers', '/my/teachers/page/<int:page>'], type='http', auth="user", website=True)
    def weblearnsTeacherListView(self, page=1, sortby='name', search="", search_in="All", groupby="none", **kw):
        # Implement similar logic for sorting, grouping, and filtering teachers
        vals = {
            # Populate 'teachers_group_list' with grouped and sorted teacher data
            'group_teachers': [],  # This needs to be implemented
            'page_name': 'teachers_list_view',
            # Include additional necessary values like 'pager', 'sortby', etc.
        }

        return request.render("your_module.weblearns_teachers_list_view_portal", vals)

    @http.route(['/my/teacher/<model("hr.enseignant"):teacher_id>'], auth="user", type='http', website=True)
    def weblearnsTeacherFormView(self, teacher_id, **kw):
        # Implementation for a detailed teacher view
        vals = {
            "teacher": teacher_id,
            'page_name': 'teacher_form_view'
        }

        return request.render("your_module.weblearns_teacher_form_view_portal", vals)

    # Implement any additional routes/methods as needed for your application
