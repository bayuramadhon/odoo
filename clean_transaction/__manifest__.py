{
    'name': 'Clean Transaction',
    'version': '1',
    'author': 'Sunpop.cn',
    'category': 'Productivity',
    'website': 'https://www.sunpop.cn',
    'license': 'LGPL-3',
    'sequence': 2,
    'summary': """ Reset Data """,
    'description': """
        App Customize Odoo :
        ====================
        1. Quick delete test data in Apps: Sales/POS/Purchase/MRP/Inventory/Accounting/Project/Message/Workflow etc.
        2. One Click to clear all data (Sometime pls click twice)
        3. Can clear and reset account chart. Be cautious
    """,
    'images': [],
    'depends': [],
    'data': [
        'views/app_theme_config_settings_views.xml',
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
