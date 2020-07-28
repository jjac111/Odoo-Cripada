# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from odoo import models, fields, api
from sqlalchemy import create_engine # Permite enviar la información del DF como SQL a una base de datos
import logging
_logger = logging.getLogger(__name__) 


	
class MRP(models.Model):
	_inherit = "mrp.production"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	
	personel = fields.Many2many(
		'hr.employee',
		string='Personal requerido',
		help='Empleados asignados a esta órden de producción',
		store=True,
	)
	
	notes = fields.Char(
		string='Observaciones',
		store=True
	)
	
