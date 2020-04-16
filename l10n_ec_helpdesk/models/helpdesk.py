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
	)
	
	

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
class Product(models.Model):
	_inherit = "product.product"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	owner_id = fields.Many2one(
		'res.partner',
		string='Cliente Empresa',
		help='Contacto de cliente al cual le pertenece el manejo de este producto.',
		store=True,
	)
	
	

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––