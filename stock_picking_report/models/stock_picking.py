from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    external_weight = fields.Char(string='External Weight', readonly=True)
    external_unit = fields.Char(string='External Unit', readonly=True)
    time_printing = fields.Datetime(string="Time Printing", default=fields.Datetime.now)

    selected_device_id = fields.Many2one(
        'devices.connection',
        string='Select Device',
        domain=[('status', '=', 'valid')],
        required=True,
        help="Select the scale device to fetch weight and unit data."
    )

    def fetch_and_update_scale_data(self):
        """
        Fetches scale data from the selected device's JSON_DATA field.
        Updates stock move with weight and unit.
        """
        self.ensure_one()
        self.write({'external_weight': '', 'external_unit': ''})  # Reset fields

        if not self.selected_device_id:
            return self._open_scale_error_wizard(_("No device selected. Please select a scale device before printing."))

        connection = self.selected_device_id
        json_str = connection.json_data  # Get JSON data from the field

        if not json_str:
            return self._open_scale_error_wizard(_("No JSON data found in the selected device."))

        try:
            # Parse JSON data
            data = json.loads(json_str)
            weight = data.get("weight", "")
            unit = data.get("unit", "")

            if not weight or not unit:
                return self._open_scale_error_wizard(_("Invalid JSON format. Missing weight or unit."))

            # Update stock move
            self.write({'external_weight': str(weight), 'external_unit': unit})
            _logger.info(f"Updated stock move: {weight} {unit}")

        except json.JSONDecodeError:
            return self._open_scale_error_wizard(_("Invalid JSON data in the selected device."))

    def _open_scale_error_wizard(self, message):
      """
      Opens the wizard for handling scale connection errors.
      Clears the current selected device to prompt the user to reselect.
      """
      self.write({'selected_device_id': False})  # Clear the current device selection
      return {
          'type': 'ir.actions.act_window',
          'res_model': 'scale.connection.wizard',
          'view_mode': 'form',
          'target': 'new',
          'context': {
              'default_message': message,
              'default_stock_move_id': self.id,
          },
      }


    def action_print_report(self):
        """
        Trigger the printing of the report.
        Fetch and update scale data before printing, but always proceed with printing.
        """
        if not self.selected_device_id:
            # If no device is selected, open the wizard to select a device
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'device.selection.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_selected_device_id': self.selected_device_id.id if self.selected_device_id else False,
                    'active_id': self.id,  # Pass the current stock move ID to the wizard
                }
            }

        # If a device is already selected, fetch data and print
        fetch_result = self.fetch_and_update_scale_data()
        if fetch_result:
            return fetch_result

        # Proceed with printing the report
        report_action = self.env.ref('stock_picking_report.action_report_stock_picking', raise_if_not_found=False)
        if report_action:
            return report_action.report_action(self)
        else:
            raise UserError(_("Report action not found."))
        
    def action_force_empty_print(self):
        """
        Force printing with empty data.
        """
        self.write({'external_weight': '', 'external_unit': ''})
        # Trigger the report printing with empty data
        report_action = self.env.ref('stock_picking_report.action_report_stock_picking', raise_if_not_found=False)
        if report_action:
            return report_action.report_action(self)
        else:
            raise UserError(_("Report action not found."))

