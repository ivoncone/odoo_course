# -*- coding: utf-8 -*-
{
    'name': "excursion",
    'version': '1.0',
    'depends': ['base_setup'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}