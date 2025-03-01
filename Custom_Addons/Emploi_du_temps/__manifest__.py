# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Emploi du temps',
    'version': '1.1',
    'author': 'Maamri Akram , Laroussi Med Aziz',
    'category': 'Feuilles de temps',
    'sequence': -101,
    'summary': '',
    'website': '',
    'depends': ['base', 'Training_center'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_attendance_security.xml',
        'views/ClassRoom.xml',
        'views/Equipment.xml',
        'views/TeacherAvailability.xml',
        'views/menu.xml',
        'views/Emploi_du_temps.xml',
        'views/dashboard.xml'

    ],
    'qweb': [
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'Emploi_du_temps/static/src/js/dashboard.js',
        ],
    },

}
