from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from random import randint
from datetime import timedelta, datetime, date

class Trainingcourse(models.Model):
    _name = 'training.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training.course'

    _sql_constraints = [
        ('nama_kursus_unik', 'UNIQUE(name)', 'Judul kursus harus unik'),
        ('nama_keterangan_cek', 'CHECK(name != description)', 'Judul kursus dan keterangan tidak boleh sama ')
    ]

    def get_default_color(self):
        return randint(1, 11)


    name = fields.Char(string='Judul', required=True, tracking=True)
    description = fields.Text(string='keterangan', tracking=True)
    user_id = fields.Many2one('res.users', string="Penanggung Jawab", tracking=True)
    session_line = fields.One2many('training.session', 'course_id', string='', tracking=True)
    product_ids = fields.Many2many('product.product', 'course_product_rel', 'course_id', 'product_id', string='cendera mata', tracking=True)

    ref = fields.Char(string='Referensi', readonly=True, default='/')
    level = fields.Selection([('basic', 'Dasar'), ('advanced', 'Lanjutan')], string='Tingkatan', default='basic')
    color = fields.Integer('Warna', default=get_default_color)
    email = fields.Char(string="Email", related='user_id.login')


    # contoh nomer dokumen/ref overding

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('training.course')
        return super(Trainingcourse, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=("%s (copy)") % (self.name or ''))
        return super(Trainingcourse, self).copy(default)
    
    def action_print_course(self):
        return self.env.ref('training_odoo.report_training_course_action').report_action(self)  

class TrainingSession(models.Model):
    _name = 'training.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training Sesi'

    def default_partner_id(self):
        instruktur = self.env['res.partner'].search(['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')], limit=1)
        return instruktur


    course_id = fields.Many2one('training.course', string='Judul Kursus', required=True, ondelete='cascade', readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char(string='Nama', required=True, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date(string='Tanggal', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    duration = fields.Float(string='Durasi', help='Jumlah Hari Training', default=3, readonly=True, states={'draft': [('readonly', False)]})
    seats = fields.Integer(string='Kursi', help='Jumlah Kuota Kursi', default=10, readonly=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', string='Instruktur', domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'Pengajar')], default=default_partner_id, readonly=True, states={'draft': [('readonly', False)]})
    attendee_ids = fields.Many2many('training.attendee', 'session_attendee_rel', 'session_id', 'attendee_id', 'Peserta', readonly=True, states={'draft': [('readonly', False)]})
    end_date = fields.Date(string="Tanggal Selesai", compute='get_end_date', inverse='set_end_date', store=True, readonly=True, states={'draft': [('readonly', False)]})


    taken_seats = fields.Float(string="Kursi Terisi", compute='compute_taken_seats')
    attendees_count = fields.Integer(string="Jumlah Peserta", compute='get_attendees_count', store=True)

    color = fields.Integer('Color Index', default=0)
    level = fields.Selection(string='Tingkatan', related='course_id.level')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('done', 'Done')], string='Status', readonly=True, default='draft')


    def action_confirm(self):
        self.state = "open"

    def action_cancel(self):
        self.write({'state': 'draft'})

    def action_close(self):
        self.write({'state': 'done'})


    @api.depends('seats', 'attendee_ids')
    def compute_taken_seats(self):
        for sesi in self:
            sesi.taken_seats = 0
            if sesi.seats and sesi.attendee_ids :
                sesi.taken_seats = 100 * len(sesi.attendee_ids) / sesi.seats

    @api.constrains('seats', 'attendee_ids')
    def check_seats_and_attendees(self):
        for r in self:
            if r.seats < len(r.attendee_ids): 
                raise ValidationError("Jumlah peserta melebihi kuota yang disediakan")

    @api.onchange('duration')
    def verify_valid_duration(self):
            if self.duration <= 0:
                self.duration = 1
                return {'warning': {'title': 'Perhatian', 'message': 'Durasi Hari Training Tidak Boleh 0 atau Negatif'}}

    @api.depends('start_date', 'duration')
    def get_end_date(self):
        for sesi in self:
            if not sesi.start_date: 
                sesi.end_date = sesi.start_date
                continue

            start = fields.Date.from_string(sesi.start_date)
            sesi.end_date = start + timedelta(days=sesi.duration)

    def set_end_date(self):
        for sesi in self:
            if not (sesi.start_date and sesi.end_date):
                continue

            start_date = fields.Datetime.from_string(sesi.start_date)
            end_date = fields.Datetime.from_string(sesi.end_date)
            sesi.duration = (end_date - start_date).days + 1
            end_date = fields.Date(string="Tanggal Selesai", compute='get_end_date', inverse='set_end_date', store=True)
            attendees_count = fields.Integer(string="Jumlah Peserta", compute='get_attendees_count', store=True)
    
    @api.depends('attendee_ids')
    def get_attendees_count(self):
        for sesi in self:
            sesi.attendees_count = len(sesi.attendee_ids)

    def cron_expire_session(self):
        now = fields.Date.today()
        expired_ids = self.search([('end_date', '<', now), ('state', '=', 'open')])
        expired_ids.write({'state': 'done'})

    def action_print_session(self):
        return self.env.ref('training_odoo.report_training_session_action').report_action(self)
    
class TrainingAttendee(models.Model):
    _name = 'training.attendee'
    _description = 'Training Peserta'

    name = fields.Char(string='Nama', required=True)
    sex = fields.Selection([('male', 'Pria'), ('female', 'Wanita')], string='Kelamin', required=True, help='Jenis Kelamin')
    marital = fields.Selection([
        ('single', 'Belum Menikah'), 
        ('married', 'Menikah'), 
        ('divorced', 'Cerai')], 
        string='Pernikahan', help='Status Pernikahan')
    session_ids = fields.Many2many('training.session', 'session_attendee_rel', 'attendee_id', 'session_id', 'Sesi')


# class Trainingcourse(models.Model):
#     _name = 'training.course'
#     _description = 'Training.course'

#     name = fields.Char(string='Judul', required=True)
#     description = fields.Text(string='keterangan')
#     user_id = fields.Many2one('res.users', string='penanggung jawab')


