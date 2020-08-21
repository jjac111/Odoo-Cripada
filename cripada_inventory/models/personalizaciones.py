# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from odoo import models, fields, api
from datetime import date
import threading
import datetime
import pandas as pd                  # Contiene DataFrames
import numpy as np                   # Matrices
import sqlalchemy
from sqlalchemy import create_engine # Permite enviar la información del DF como SQL a una base de datos
#from sqlalchemy.orm import sessionmaker
import math
import logging
_logger = logging.getLogger(__name__) 




class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'
	
	
	
	guia_remision = fields.Char(
		string="Guía de Remisión",
		store=True,
	)
	

	
class SaleOrder(models.Model):
	_inherit = 'sale.order'
	
	cliente_final = fields.Many2one(
		'res.partner',
		string='Cliente Final',
		store=True,
	)
	
	guia_remision = fields.Char(
		string="Guía de Remisión",
		store=True,
	)

# class ResPartner(models.Model):
	# _inherit = 'res.partner'

	# codigo_cliente = fields.Char(
		# string="Codigo Cliente",
		# store=True,
	# )
	
		
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
	
	
	guia_remision = fields.Char(
		string="Guía de Remisión",
		store=True,
	)
	
	peso_total = fields.Float(
		string='Peso Total',
		help='Peso total de productos en esta operación.',
		store=True,
		compute='calcular_peso'
	)
	volumen_total = fields.Float(
		string='Volumen Total',
		help='Volumen total de productos en esta operación.',
		store=True,
	)
	
	
	@api.depends('move_lines')
	def calcular_peso(self):
		
		for record in self:
			peso = 0
			for line in record.move_lines:
				
				cantidad = line.qty_done
				producto = line.product_id
				
				if producto.x_unidades_por_empaque <= 0: continue
				
				line.peso += (cantidad / producto.x_unidades_por_empaque) * producto.x_peso_empaque
			
			record.peso_total = peso
		

class StockMoveLine(models.Model):
	_inherit = "stock.move.line"
	
	remaining_stock = fields.Float(
		string='Remaining Stock',
		store=True,
	)
	
	empaques = fields.Float(
		string='Número de Empaques',
		store=True,
		compute='_compute_empaques',
	)
	
	@api.depends('qty_done')
	def _compute_empaques(self):
		for record in self:
			if record.product_id.x_unidades_por_empaque > 0:
				record.empaques =  record.qty_done / record.product_id.x_unidades_por_empaque

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
		required=False
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
		('CUÑ', 'Cuñete'),
		('UND', 'Unidad')],
		string='Unidad Principal (Presentación)',
		store=True,
		required=False
	)
	
	x_unidad_secundaria = fields.Selection(
		[
		('Kg', 'Kilogramos'),
		('K', 'Kilo'),
		('g', 'gramos'),
		('lb', 'Libra'),
		('Lt', 'Litros'),
		('ml', 'Mililitros'),
		('Gl', 'Galón'),],
		string='Unidad Secundaria',
		store=True,
		required=False
	)
	
	x_familia = fields.Selection(
		[
		('ABONOS','Abonos'),
		('ACARICIDA', 'Acaricida'),
		('AGROQUIMICOS','Agroquímicos'),
		('ALIMENTO VACUNO','Alimento Vacuno'),
		('AUTOMOTRIZ','Automotriz'),
		('BACTERICIDA','Bactericida'),
		('BANDEJAS','Bandejas'),
		('BIOLOGICOS','Biológicos'),
		('CABLES','Cables'),
		('CAJA','Caja'),
		('CERAMICAS','Cerámicas'),
		('COADYUVANTE','Coadyuvante'),
		('COLOMBINA','Colombina'),
		('EQUIPO DE APLICACION','Equipo de Aplicación'),
		('EQUIPO F & B','Equipo F & B'),
		('EQUIPO INSTITUCIONAL','Equipo Institucional'),
		('EQUIPOS TECNOLOGICOS','Equipos Tecnológicos'),
		('FERTILIZANTE','Fertilizante'),
		('FUNGICIDA', 'Fungicida'),
		('HERBICIDA', 'Herbicida'),
		('HUMECTANTE-DISPERSANTE','Humectante - Dispersante'),
		('IMPRESORAS','Impresoras'),
		('INSECTICIDA', 'Insecticida'),
		('KAY QSR','Kay Qsr'),
		('LINEA F & B','Línea F & B'),
		('LINEA INSTITUCIONAL','Línea Institucional'),
		('MAQUINA','Máquina'),
		('MAQUINAS','Máquinas'),
		('MASCOTAS','Mascotas'),
		('MATERIAL DE EMPAQUE','Material de Empaque'),
		('MOLUSQUICIDA','Molusquicida'),
		('NEMATICIDA','Nematicida'),
		('ORGANICOS','Orgánicos'),
		('OTROS','Otros'),
		('QUIMICO INDUSTRIAL','Químico Industrial'),
		('QUIMICOS EN GENERAL','Químicos en General'),
		('SANIDAD ANIMAL','Sanidad Animal'),
		('SOLUCION DE ABONO','Solución de Abono'),
		('SUPLEMENTO','Suplemento'),
		('TRATAMIENTO DE AGUAS','Tratamiento de Aguas'),
		('VARIOS','Varios'),
		],
		string='Familia',
		store=True,
		required=False
	)
	
	x_tipo_empaque = fields.Selection(
		[
		('BALDE', 'Balde'),
		('BASE','Base'),
		('BOMBA','Bomba'),
		('CAJAS','Cajas'),
		('CANECA','Caneca'),
		('CAPSULAS','Cápsulas'),
		('CISTERNA','Cisterna'),
		('CUÑETE','Cuñete'),
		('ENVASE','Envase'),
		('FRASCO','Frasco'),
		('FUNDA','Funda'),
		('GALON','Galón'),
		('GARRAFA','Garrafa'),
		('IBC','IBC'),
		('IMPRESORA','Impresora'),
		('KILOGRAMOS','Kilogramos'),
		('LIBRAS','Libras'),
		('LITRO','Litro'),
		('MAQUINARIA','Maquinaria'),
		('METROS','Metros'),
		('ONZAS','Onzas'),
		('PALLETS','Pallets'),
		('SACO','Saco'),
		('SOBRES','Sobres'),
		('TAMBOR','Tambor'),
		('TARRO','Tarro'),
		('UNIDADES','Unidades'),
		],
		string='Tipo de Empaque',
		store=True,
		required=False
	)
	
	x_color_franja = fields.Selection(
		[
		('VERDE', 'Verde'),
		('AMARILLO', 'Amarillo'),
		('AZUL', 'Azul'),
		('ROJO', 'Rojo'),
		],
		string= 'Color de Franja',
		store=True,
		required=False
	)
	
	x_peso_bruto = fields.Float(
		string='Peso Bruto (Kg)',
		store=True,
		required=False
	)
	
	x_peso_neto = fields.Float(
		string='Peso Neto (Kg)',
		store=True,
		required=False
	)
	
	x_total_peso_pallet = fields.Float(
		compute='_compute_peso_pallet',
		store=True,
		string='Total de Peso por Pallet',
	)
	
	x_coeficiente = fields.Float(
		string='Coeficiente',
		store=True,
		required=False
	)
	
	x_unidades_por_empaque = fields.Float(
		string= 'Unidades por Empaque',
		store=True,
		required=False
	)
	
	x_empaques_por_pallet = fields.Integer(
		string= 'Empaques por Pallet',
		store=True,
		required=False
	)
	
	x_registro_nacional = fields.Char(
		string= 'No. Registro Nacional',
		store=True,
	)
	
	x_peso_empaque = fields.Float(
		string= 'Peso por Empaque / Peso Bruto (Kg)',
		store=True,
		required=False
	)
	
	x_volumen_empaque = fields.Float(
		string= 'Volumen por Empaque (m3)',
		store=True,
		required=False
	)
	
	
	
	

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.depends('x_peso_bruto', 'x_empaques_por_pallet')
	def _compute_peso_pallet(self):
		for record in self:
			record.x_total_peso_pallet = record.x_peso_bruto * record.x_empaques_por_pallet
			
	
	