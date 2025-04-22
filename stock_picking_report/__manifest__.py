{
    'name': 'Stock Picking Report',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'summary': 'Add a button to fetch weight from IoT device and print stock picking reports.',
    'depends': ['stock', 'odoo_device'],
    'data': [
        'views/stock_picking_views.xml',
        'views/wizard_form.xml',
        'views/selected_device.xml',
        'reports/stock_picking_report_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
