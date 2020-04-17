# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from odoo import models, fields, api
from datetime import date


class HelpdeskTicket(models.Model):
	_inherit = 'helpdesk.ticket'

	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	
	x_datetime_en_proceso = fields.Datetime(
		string='Fecha de inicio En Proceso',
		store=True,
	)
	x_datetime_por_confirmar = fields.Datetime(
		string='Fecha de inicio Por Confirmar',
		store=True,
	)
	x_datetime_resuelto = fields.Datetime(
		string='Fecha de inicio Resuelto',
		store=True,
	)
	
	x_sla_failed_notify = fields.Boolean(
		string='Notificado por SLA fallado',
		store=True,
	)
	x_sla_over_failed_notify = fields.Boolean(
		string='Notificado por SLA sobre fallado',
		store=True,
	)
	x_sla_to_fail_notify = fields.Boolean(
		string='Notificado por SLA por fallar',
		store=True,
	)
	x_rating_notify = fields.Boolean(
		string='Notificado por SLA por fallar',
		store=True,
	)

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.onchange('partner_id', 'ticket_type_id')
	def _nombre_ticket(self):
	
		self.name = str('' if not self.partner_id.name else self.partner_id.name) + ' | ' + str('' if not self.ticket_type_id.name else self.ticket_type_id.name)
								
		



class StockPicking(models.Model):
	_inherit = "stock.picking"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	cliente_final = fields.Many2one(
		'res.partner',
		string='Cliente Final',
		help='Contacto de cliente al cual realizar entrega.',
		store=True,
	)
	
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket',
		help='Ticket de servicio creado en Helpdesk',
		store=True,
	)

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	
	
	
class ProductTemplate(models.Model):
	_inherit = "product.template"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	owner_id = fields.Many2one(
		'res.partner',
		string='Cliente Empresa',
		help='Contacto de cliente al cual le pertenece el manejo de este producto.',
		store=True,
		required=True
	)
	
	x_pvp = fields.Monetary(
		string='PVP',
		store=True,
	)
	
	x_unidad_principal = fields.Selection(
		[
		('TAM', 'Tambor'),
		('CAN', 'Caneca'),
		('CAJ', 'Caja'),
		('FCO', 'Frasco'),
		('FUN', 'Funda'),
		('SAC', 'Saco'),
		('GAL', 'Galón'),
		('IBC', 'IBC'),
		('CUÑ', 'Cuñete')],
		string='Unidad Principal (Presentación)',
		store=True,
		required=True
	)
	
	x_unidad_secundaria = fields.Selection(
		[
		('Kg', 'Kilogramos'),
		('Lt', 'Litros'),
		('g', 'gramos'),
		('Gl', 'Galón')],
		string='Unidad Secundaria',
		store=True,
		required=True
	)
	
	x_familia = fields.Selection(
		[
		('INSECTICIDA', 'Insecticida'),
		('FUNGICIDA', 'Fungicida'),
		('HERBICIDA', 'Herbicida'),
		('ALCALICIDA', 'Alcalicida'),
		('PINTURA', 'Pintura'),
		('OTRO', 'Otro')],
		string='Familia',
		store=True,
		required=True
	)
	
	x_coeficiente = fields.Float(
		string='Coeficiente',
		store=True,
		required=True
	)
	
	x_unidades_por_empaque = fields.Float(
		string= 'Unidades por Empaque',
		store=True,
		required=True
	)
	
	x_empaques_por_pallet = fields.Integer(
		string= 'Empaques por Pallet',
		store=True,
		required=True
	)
	
	x_registro_nacional = fields.Char(
		string= 'No. Registro Nacional',
		store=True,
	)
	
	x_peso_empaque = fields.Float(
		string= 'Peso por Empaque (Kg)',
		store=True,
		required=True
	)
	
	x_volumen_empaque = fields.Float(
		string= 'Volumen por Empaque (m3)',
		store=True,
		required=True
	)
	
	

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	
	
class MRP(models.Model):
	_inherit = "mrp.production"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket',
		help='Ticket de servicio creado en Helpdesk',
		store=True,
		required=True
	)
	
	
	
