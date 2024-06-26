from odoo import fields, models, _
from odoo.exceptions import UserError

class PdfOrientation(models.TransientModel):
    _name = 'pdforientation'
    _description = "Select the Orientation of the PDF"

    orientation = fields.Selection(string="PDF orientation", selection=[('landscape', _('Landscape')), ('portrait', _('Portrait'))], default='landscape')
    query_name = fields.Text(string="Query")

    def print_pdf(self):
        self = self.sudo()
        try:
            self.env.cr.execute(self.query_name)
        except Exception as e:
            raise UserError(e)

        try:
            if self.env.cr.description:
                headers = [d[0] for d in self.env.cr.description]
                bodies = self.env.cr.fetchall()
        except Exception as e:
            raise UserError(e)

        action_print_pdf = self.env.ref('ctp_query.action_print_pdf')
        if self.orientation == 'landscape':
            action_print_pdf.paperformat_id.orientation = "Landscape"
        elif self.orientation == 'portrait':
            action_print_pdf.paperformat_id.orientation = "Portrait"

        append_data = {
            'query_name': self.query_name,
            'headers': headers,
            'bodies': bodies
        }
        
        return action_print_pdf.report_action(self, data=append_data)
