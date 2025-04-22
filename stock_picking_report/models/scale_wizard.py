from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)  

class ScaleConnectionWizard(models.TransientModel):
    _name = 'scale.connection.wizard'
    _description = 'Scale Connection Error Wizard'

    message = fields.Text(string="Message", readonly=True, default="The scale is not connected.")
    stock_move_id = fields.Many2one('stock.move', string="Stock Move", readonly=True)

    def action_print_empty(self):
        """
        Proceed with printing empty data.
        """
        self.ensure_one()
        _logger.info("action_print_empty called for wizard ID: %s", self.id)

        # Ensure stock_move_id exists
        if not self.stock_move_id:
            _logger.error("No stock_move_id set for wizard ID: %s", self.id)
            raise UserError(_("No stock move record is associated with this wizard."))

        # Check if the method exists on stock.move and call it
        if hasattr(self.stock_move_id, 'action_force_empty_print'):
            return self.stock_move_id.action_force_empty_print()
        else:
            _logger.error("The method 'action_force_empty_print' does not exist on stock.move.")
            raise UserError(_("The 'action_force_empty_print' method is not defined on the stock.move model."))

    def action_cancel(self):
        """
        Cancel the operation and close the wizard.
        """
        _logger.info("action_cancel called for wizard ID: %s", self.id)
        return {'type': 'ir.actions.act_window_close'}
