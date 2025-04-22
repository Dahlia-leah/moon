from odoo import models, fields, api

class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    member_ids = fields.Many2many(
        'hr.employee',  # Link to employees instead of users
        'helpdesk_team_employee_rel',  # Relation table
        'team_id',  # Column for helpdesk team
        'employee_id',  # Column for employees
        string="Team Members",
        help="Employees assigned to this helpdesk team.",
    )

    @api.model
    def _default_member_ids(self):
        """Fetch all employees as default members."""
        return self.env['hr.employee'].search([]).ids

    # Add default value to include all employees initially
    member_ids = fields.Many2many(
        'hr.employee',
        'helpdesk_team_employee_rel',
        'team_id',
        'employee_id',
        string="Team Members",
        help="Employees assigned to this helpdesk team.",
        default=_default_member_ids,
    )
