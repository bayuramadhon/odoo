from odoo import _, api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string='Instruktur')
    session_line = fields.One2many('training.session', 'partner_id', string='Daftar Mengajar Sesi', readonly=True)
    