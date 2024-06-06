from odoo import models, fields
import os
import logging
_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def auto_delete_attachment_file(self, before_datetime_now=None, limit_record=None):
        before_date_time = fields.Datetime.subtract(fields.Datetime.now(), days=before_datetime_now)
        attachment = self.env['ir.attachment'].search([('write_date', '<', before_date_time), ('type', '=', 'binary')],
                                                      limit=limit_record)

        if attachment:
            file_path = 'data/filestore/kittipatkimmy01-kim-demo-module-main-13562532/%s' % attachment.store_fname

            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    _logger.info(f"File {file_path} has been deleted successfully.")
                except Exception as e:
                    _logger.error(f"Error deleting file {file_path}: {e}")
            else:
                _logger.warning(f"File {file_path} does not exist.")

            attachment.unlink()
