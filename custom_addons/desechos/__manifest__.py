# -*- coding: utf-8 -*-
{
    'name': "desechos",

    'description': """
        modulo para agregar el precio de desechos 
    """,

    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base_setup', 'stock_account', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/desechos_stock_views.xml',
        #'views/desechos_valuation_layer.xml'   
        ],
    'application': True,
    'installable': True
}
