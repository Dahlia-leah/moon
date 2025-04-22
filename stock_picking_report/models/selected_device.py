from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

class DeviceSelectionWizard(models.TransientModel):
    _name = 'device.selection.wizard'
    _description = 'Wizard to select a device for fetching weight'

    selected_device_id = fields.Many2one(
        'devices.connection',
        string='Select Device',
        domain=[('status', '=', 'valid')],
        required=True,
        ondelete='cascade',
        help="Select the scale device to fetch weight and unit data."
    )

    def action_confirm(self):
        """
        Once the device is selected, fetch the scale data and trigger the report.
        """
        active_id = self._context.get('active_id')
        stock_move = self.env['stock.move'].browse(active_id)
        
        # Set the selected device
        stock_move.selected_device_id = self.selected_device_id

        # Fetch scale data and print the report
        fetch_result = stock_move.fetch_and_update_scale_data()
        if fetch_result:
            return fetch_result
        
        # Proceed with printing the report
        report_action = self.env.ref('stock_picking_report.action_report_stock_picking', raise_if_not_found=False)
        if report_action:
            return report_action.report_action(stock_move)
        else:
            raise UserError(_("Report action not found."))
