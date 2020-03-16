# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from odoo import models, fields, api
from datetime import date


class HelpdeskTicket(models.Model):
	_inherit = 'helpdesk.ticket'

    # ---------------------
    # DEFINICION DE CAMPOS
    # ---------------------
	
	x_datetime_en_proceso = fields.datetime(
		string='Fecha de inicio En Proceso',
		store=True,
	)
	x_datetime_por_confirmar = fields.datetime(
		string='Fecha de inicio Por Confirmar',
		store=True,
	)
	x_datetime_resuelto = fields.datetime(
		string='Fecha de inicio Resuelto',
		store=True,
	)
	
	x_sla_failed_notify = fields.boolean(
		string='Notificado por SLA fallado',
		store=True,
	)
	x_sla_over_failed_notify = fields.boolean(
		string='Notificado por SLA sobre fallado',
		store=True,
	)
	x_sla_to_fail_notify = fields.boolean(
		string='Notificado por SLA por fallar',
		store=True,
	)

    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.onchange('partner_id', 'ticket_type_id')
	def _nombre_ticket(self):
	
		self.name = str('' if not self.partner_id.name else self.partner_id.name) + ' | ' + str('' if not self.ticket_type_id.name else self.ticket_type_id.name)
								
		





class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # ---------------------
    # DEFINICION DE CAMPOS
    # ---------------------
	
	
    partner_ref_new = fields.many2one(
        'helpdesk.ticket',
        string='Ticket',
        help='Ticket de servicio creado en Helpdesk',
        store=True,
    )

    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    @api.onchange('partner_ref_new')
    def _vendor_ref(self):

        self.partner_ref = str(self.partner_ref_new.name) + ' (#' + str(self.partner_ref_new.id) + ')'
		
		


class StockPicking(models.Model):
	_inherit = "stock.picking"
	
	# ---------------------
    # DEFINICION DE CAMPOS
    # ---------------------
	x_studio_cliente_final = fields.many2one(
		'res.parter',
		string='Cliente Final',
		help='Contacto de cliente al cual realizar entrega.',
		store=True,
	)

    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––