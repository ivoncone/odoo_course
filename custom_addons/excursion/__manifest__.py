# -*- coding: utf-8 -*-
{
    'name': "excursion",
    'version': '1.0',
    'depends': ['base_setup', 'property'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
