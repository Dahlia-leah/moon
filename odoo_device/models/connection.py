from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class Connection(models.Model):
    _name = 'devices.connection'
    _description = 'Device Connection'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Connection Name', required=True, index=True, tracking=True)
    device_id = fields.Many2one('devices.device', string='Device', required=True, ondelete='cascade', tracking=True)
    json_data = fields.Text(string='JSON Data', readonly=True)
    status = fields.Selection(
        [('valid', 'Valid'), ('invalid', 'Invalid')],
        string='Status',
        readonly=True,
        default='invalid',
        tracking=True
    )
    active = fields.Boolean(default=True, string="Active", tracking=True)
    last_checked = fields.Datetime(string="Last Checked", readonly=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, required=True, tracking=True)


    def delete_connection(self):
        self.ensure_one()
        if self.env['stock.move'].search_count([('selected_device_id', '=', self.id)]) > 0:
            raise ValidationError(_("Cannot delete this connection because it is being used in stock moves. Please archive it instead."))
        _logger.info(f"Deleting connection: {self.name}")
        return self.unlink()

    def archive_connection(self):
        self.ensure_one()
        self.active = False
        _logger.info(f"Archived connection: {self.name}")
        return True

    @api.model
    def create(self, vals):
        record = super(Connection, self).create(vals)
        return record

    def write(self, vals):
        result = super(Connection, self).write(vals)
        # No need to re-check anything since URL is gone
        return result

    def name_get(self):
        return [(record.id, f"{record.name} ({record.device_id.name})") for record in self]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('device_id.name', operator, name)]
        domain += [('user_id', '=', self.env.user.id)]
        return super(Connection, self)._search(domain + args, limit=limit, access_rights_uid=name_get_uid, **kwargs)

    def read(self, fields=None, load='_classic_read'):
        user = self.env.user
        for record in self:
            if record.user_id != user:
                raise UserError(_("You do not have access to this connection. Please enter a new scale to proceed."))
        return super(Connection, self).read(fields, load)

    @api.model
    def _search(self, domain, limit=None, access_rights_uid=None, **kwargs):
        domain += [('user_id', '=', self.env.user.id)]
        return super(Connection, self)._search(domain, limit=limit, access_rights_uid=access_rights_uid, **kwargs)


    @api.model
    def _cron_check_connections(self):
        connections = self.search([('active', '=', True)])
