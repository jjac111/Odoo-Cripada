# -*- coding: utf-8 -*-
{
    'name': "Personalizaciones Cripada",

    'summary': """
        Módulo de personalizaciones de Helpdesk, Purchase, Sale, MRP, y Stock para Cripada S.A.""",

    'description': """
        Este módulo incopora las personalizaciones requeridas por Cripada para el funcionamiento de Odoo.
    """,

    'author': "Juan Javier Arosemena",
    'website': "http://www.jarosemena.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
		'mrp',
		'hr'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/all_views.xml',
    ],
}