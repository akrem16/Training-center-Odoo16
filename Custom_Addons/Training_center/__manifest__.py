# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Training_center',
    'version': '1.1',
    'author': 'Maamri Akram , Laroussi Med Aziz',
    'category': 'Human Resources/Training_center',
    'sequence': -101,
    'summary': 'Centralize training center information',
    'website': '',
    'depends': ['base', 'hr', 'hr_holidays', 'mail','portal','board'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_attendance_security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/enseignant_process.xml',
        'views/etudiant_views.xml',
        'views/cours_views.xml',
        'views/Cours_session.xml',
        'views/training_center_view.xml',
        'reports/report.xml',
        'reports/student_registration.xml',
        'views/view_course_category.xml',
        'views/profile_enseiganat.xml',
        'views/dashboard.xml',
        'views/time_off_inhe_views.xml',
    ],
'qweb': [
        'reports/report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'Training_center/static/src/enseignant.css'
        ]
    },

}
