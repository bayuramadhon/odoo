from odoo import _, api, fields, models

class Respartner(models.Model):
    _inherit = 'res.partner'
    _description = 'res partner'
    
    
class PaketProduk(models.Model):
    _inherit = 'mrp.bom'
    _description = 'paket Produk'

class Produk(models.Model):
    _inherit = 'Produk.template'
    _description = 'Produk'
    