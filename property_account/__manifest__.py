# -*- coding: utf-8 -*-
{
    'name': "property_account",
    'description': """
        account for property owners
    """,
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base_setup','property'
    ],

    # always loaded
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
