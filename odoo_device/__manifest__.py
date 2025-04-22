{
    'name': 'Odoo Device',
    'version': '1.0',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'summary': 'Manage Devices in the System',
    'description': """
        This module helps you manage devices and their connections.
    """,
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/connection_views.xml',
        'security/connection_security.xml',
        'views/device_views.xml',
        'data/device_data.xml',
        'data/ir_cron_data.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}