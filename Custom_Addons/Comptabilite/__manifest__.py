# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Comptabilite',
    'version': '1.1',
    'author': 'Maamri Akram , Laroussi Med Aziz',
    'category': 'Gestion comptable',
    'sequence': -101,
    'summary': '',
    'website': '',
    'depends': ['base', 'Training_center'],
    'data': [
        'security/ir.model.access.csv',
        'views/compte_comptable_views.xml',
    ],
    'qweb': [
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},

}
