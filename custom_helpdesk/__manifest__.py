{
    'name': 'Custom Helpdesk Team Members',
    'version': '1.0',
    'category': 'Helpdesk',
    'summary': 'Replace helpdesk team members with employees instead of users',
    'depends': ['helpdesk', 'hr'],
    'data': [
        'views/helpdesk_team_views.xml',
    ],
    'installable': True,
    'application': False,
}
