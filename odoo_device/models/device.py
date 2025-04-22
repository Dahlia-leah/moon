from odoo import models, fields, api, exceptions

class Device(models.Model):
    _name = 'devices.device'
    _description = 'Device'

    name = fields.Char(string='Device Name', required=True, default='Scale')
    device_id = fields.Char(string='Device ID', required=True, default='1', unique=True)

    @api.model
    def create(self, vals):
        # Restrict creation to ensure only one record exists
        if self.env['devices.device'].search_count([]) > 0:
            raise exceptions.UserError("You cannot create new Device records.")
        return super(Device, self).create(vals)

    def unlink(self):
        raise exceptions.UserError("You cannot delete Device records.")