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
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket asociado',
		store=True
	)
	guia_remision = fields.Char(
		string="Guía de Remisión",
		store=True,
	)
	
	is_reclamo = fields.Boolean(
		store = True,
	)
	
	tipo_reclamo = fields.Selection(
		[
		('ERROR EN DESPACHO', 'Error En Despacho'),
		('ERROR DE ENTREGA', 'Error De Entrega'),
		('TIEMPO DE ENTREGA', 'Tiempo De Entrega'),
		('FALTA DE ATENCION', 'Falta De Atencion'),
		('INFORMES ERRADOS', 'Informes Errados'),
		('INFORME ATRASADO', 'Informe Atrasado'),
		('DIFERENCIA DE INVENTARIO', 'Diferencia De Inventario'),
		('FALTANTE DE PRODUCTO', 'Faltante De Producto'),
		('AVERIA DE PRODUCTO', 'Averia De Producto'),
		('INSTALACIONES', 'Instalaciones'),
		],
		string = "Tipo de reclamo",
		store = True,
	)
		
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.onchange('partner_id', 'ticket_type_id')
	def _nombre_ticket(self):
		if self.ticket_type_id:
			if 'Reclamo' not in self.ticket_type_id.name:
				self.name = str('' if not self.partner_id.name else self.partner_id.name) + ' | ' + str('' if not self.ticket_type_id.name else self.ticket_type_id.name)
				self.is_reclamo = False
			else:
				self.is_reclamo = True
	

class HelpdeskTeam(models.Model):
	_inherit = 'helpdesk.team'
	
	city = fields.Selection(
		[('UIO', 'Quito'),('GYE', 'Guayaquil')],
		string='Ciudad',
		store=True,
		required=True
	)
	
	def url_querytree(self):
		# thread = threading.Thread(target=extract, args=(self))
		# thread.start()
		extract(self)
		
		return {
			'name'     : 'Go to website',
            'type'     : 'ir.actions.act_url',
            'target'   : 'new',
            "url": "http://138.128.244.200:54182/"
        }
	
	def url_grafana(self):
		# thread = threading.Thread(target=extract, args=(self))
		# thread.start()
		return {'warning': {'title': 'Warning Title Here', 'message': 'Your warning message here'}}
		# return {
			# 'name'     : 'Go to website',
            # 'type'     : 'ir.actions.act_url',
            # 'target'   : 'new',
            # "url": "http://138.128.244.200:3000"
        # }
	

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'
	
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket',
		store=True,
		required=True
	)
	
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.onchange('helpdesk_ticket')
	def _set_gr(self):
		self.guia_remision = self.helpdesk_ticket.guia_remision

	
class SaleOrder(models.Model):
	_inherit = 'sale.order'
	
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket',
		store=True,
		required=True
	)

	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––– @api ––––––––––––––––––––––––––––––––––––––––––––––––––––––
	# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
	@api.onchange('helpdesk_ticket')
	def _set_gr(self):
		self.guia_remision = self.helpdesk_ticket.guia_remision
		
class StockPicking(models.Model):
	_inherit = "stock.picking"
	
	# ---------------------
	# DEFINICION DE CAMPOS
	# ---------------------
	
	
	helpdesk_ticket = fields.Many2one(
		'helpdesk.ticket',
		string='Ticket',
		help='Ticket de servicio creado en Helpdesk',
		store=True,
	)
	


			
	
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
	
	
	

def extract(self):

	base_mateo_string = "138.128.244.200:5432"
	user_password_psql = "postgres:Prizma@2020"
	base_driver_psql = "postgresql+psycopg2"
	schema_psql = "public"
	database = "postgres"

	con_string = base_driver_psql+"://"+user_password_psql+"@"+base_mateo_string+'/'+database
	connection = sqlalchemy.create_engine(con_string)
	
	
	# Query a la tabla de timestamp de la DB. Esta contiene la datetime de la última vez que se corrió este código.
	sql_query = """
	SELECT *
	FROM database_timestamp
	"""
	result = connection.execute(sql_query)
	timestamp = str(result.first()[1])
	
	
	

	result_sale_order = self.env['sale.order'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'guia_remision','helpdesk_ticket','partner_id', 'user_id', 'warehouse_id'])


	result_sale_order_line = self.env['sale.order.line'].search([['write_date', '>', timestamp]]).read(['id','product_id','product_uom_qty','order_id','create_date','order_partner_id','price_total'])


	result_move = self.env['stock.move'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'location_id', 'location_dest_id', 'picking_id', 'product_id', 'name', 'scrapped', 'date', 'move_line_ids','remaining_qty'])


	result_picking = self.env['stock.picking'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'name', 'helpdesk_ticket', 'cliente_final', 'date', 'date_done', 'has_scrap_move', 'location_id', 'location_dest_id', 'message_attachment_count', 'move_line_ids', 'origin', 'owner_id', 'partner_id'])


	result_move_line = self.env['stock.move.line'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'move_id', 'product_id', 'lot_id', 'owner_id', 'picking_id', 'location_id', 'location_dest_id', 'qty_done','remaining_stock'])


	# result_partner = self.env['res.partner'].search([['write_date', '>', timestamp]]).read()


	result_product = self.env['product.product'].search([]).read(['id', 'product_tmpl_id'])


	result_product_template = self.env['product.template'].search([]).read(['__last_update', 'id', 'default_code' , 'name', 'owner_id',  'x_coeficiente', 'x_empaques_por_pallet', 'x_familia', 'x_peso_empaque', 'x_pvp', 'x_registro_nacional', 'x_unidad_principal', 'x_unidad_secundaria', 'x_unidades_por_empaque', 'x_volumen_empaque', 'x_color_franja', 'x_peso_bruto', 'x_peso_neto', 'x_total_peso_pallet', 'x_tipo_empaque', 'list_price'])


	result_lot = self.env['stock.production.lot'].search([]).read(['__last_update', 'name', 'id', 'life_date' , 'alert_date', 'product_id'])


	result_quant = self.env['stock.quant'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'display_name', 'location_id', 'lot_id', 'owner_id', 'product_id', 'quantity'])


	result_ticket = self.env['helpdesk.ticket'].search([['write_date', '>', timestamp]]).read(['id', 'name', 'partner_id', 'ticket_type_id' ,'stage_id', 'team_id', 'user_id','create_date','x_datetime_en_proceso','x_datetime_por_confirmar','x_datetime_resuelto','__last_update','description','helpdesk_ticket','guia_remision','tag_ids','tipo_reclamo'])


	result_team = self.env['helpdesk.team'].search([]).read(['id', 'name', 'city'])
	
	
	result_mrp = self.env['mrp.production'].search([['write_date', '>', timestamp]]).read(['__last_update', 'id', 'display_name','notes','date_finished', 'product_qty','helpdesk_ticket', 'product_id','routing_id', 'user_id','state'])



	# Aquí se crean los DataFrames para cada tabla
	
	df_product = pd.DataFrame.from_dict(result_product_template)
	df_product_pr = pd.DataFrame.from_dict(result_product)
	
	if not df_product.empty and not df_product_pr.empty:
		df_product_pr['product_tmpl_id'] = df_product_pr['product_tmpl_id'].apply(lambda x : x[0])
		df_product_pr.set_index('product_tmpl_id', inplace = True)

		df_product['id']= df_product['id'].apply(lambda x : df_product_pr.loc[x])
		df_product.set_index('id',inplace = True)

	df_lot = pd.DataFrame.from_dict(result_lot)
	if not df_lot.empty:
		df_lot.set_index('id', inplace = True)

	df_quant = pd.DataFrame.from_dict(result_quant)
	if not df_quant.empty:
		df_quant.set_index('id', inplace = True)

	df_ticket = pd.DataFrame.from_dict(result_ticket)
	if not df_ticket.empty:
		df_ticket.set_index('id', inplace = True)

	# df_order = pd.DataFrame.from_dict(result_order)

	df_picking = pd.DataFrame.from_dict(result_picking)
	if not df_picking.empty:
		df_picking.set_index('id', inplace = True)

	df_move = pd.DataFrame.from_dict(result_move)
	if not df_move.empty:
		df_move.set_index('id', inplace = True)

	df_move_line = pd.DataFrame.from_dict(result_move_line)
	if not df_move_line.empty:
		df_move_line.set_index('id', inplace = True)

	df_team = pd.DataFrame.from_dict(result_team)
	if not df_team.empty:
		df_team.set_index('id',inplace = True)

	df_sale = pd.DataFrame.from_dict(result_sale_order)
	if not df_sale.empty:
		df_sale.set_index('id',inplace = True)

	df_sale_line = pd.DataFrame.from_dict(result_sale_order_line)
	if not df_sale_line.empty:
		df_sale_line.set_index('id',inplace = True)
	
	df_mrp = pd.DataFrame.from_dict(result_mrp)
	if not df_mrp.empty:
		df_mrp.set_index('id',inplace = True)

	# df_partner = pd.DataFrame.from_dict(result_partner)




	# # Crea el DataFrame para flujos, cada flujo es 1 ticket

	# In[4]:


	df_flujo = df_ticket.copy()

	# Asigna los valores de tickets en picking al número del ticket solamente: [4, Adama|OIMP] -> 4
	if not df_picking.empty:
		df_picking['helpdesk_ticket'] = df_picking['helpdesk_ticket'][df_picking['helpdesk_ticket'] != False].apply(lambda x: x[0])


	# In[5]:


	if not df_flujo.empty:
		cities = []
		for i, flujo in df_flujo.iterrows():
			team_id = flujo['team_id'][0]
			city = df_team.loc[team_id]['city']
			cities.append(city)

		df_flujo['ciudad'] = cities




	# Añade las operaciones de bodega respectivas a sus Tickets
	
	if not df_flujo.empty and not df_picking.empty:
		ops = []
		for i, flujo in df_flujo.iterrows():
			ticket = i
			ops.append(df_picking[df_picking['helpdesk_ticket'].values == ticket]['name'].values.tolist())
			
		df_flujo['operaciones'] = ops
		
	##################################################################################################


	# ### Formateo

	# In[7]:


	# Asigna los valores de picking_id en move_line al nombre del picking solamente: [54, UIO/OIMP/9] -> UIO/OIMP/9
	if not df_move_line.empty:
		df_move_line['picking_id'] = df_move_line['picking_id'][df_move_line['picking_id'] != False].apply(lambda x: x[1])
	if not df_move.empty:
		df_move['picking_id'] = df_move['picking_id'][df_move['picking_id'] != False].apply(lambda x: x[1])


	# # Añade movimientos a flujos (recuerda: 1 operación = varios movimientos)

	# In[8]:


	
	if not df_flujo.empty and not df_move_line.empty:
		moves = []
		for i, flujo in df_flujo.iterrows():
			pickings = flujo['operaciones']
			move = df_move_line[df_move_line['picking_id'].apply(lambda x: x in pickings)].index.values.tolist()
			
			moves.append(move)

		df_flujo['moves'] = moves


	# # Añade Lote y Fecha de expiración en Quants y Moves

	# In[9]:


	# Asigna lotes y fechas de expiración a cada existencia
	if not df_quant.empty:
		lots = []
		lots_expiries = []
		lots_alert = []
		for i, quant in df_quant.iterrows():
			lot = quant.lot_id
			lot_expiry = False
			lot_alert = False
			
			if lot:
				lot_id = lot[0]
				lot = lot[1]
				lot_expiry = df_lot.loc[lot_id]['life_date']
				lot_alert= df_lot.loc[lot_id]['alert_date']
			
			lots.append(lot)
			lots_expiries.append(lot_expiry)
			lots_alert.append(lot_alert)

		df_quant['lot'] = lots
		df_quant['lot_expiry'] = lots_expiries
		df_quant['lot_alert'] = lots_alert


	# In[10]:


	# Asigna lotes y fechas de expiración a cada movimient
	if not df_move_line.empty:
		lots = []
		lots_expiries = []
		for i, move in df_move_line.iterrows():
			lot = move['lot_id']
			lot_expiry = False
				
			if lot:
				lot_id = lot[0]
				lot = lot[1]
				lot_expiry = df_lot.loc[lot_id]['life_date']
			
			lots.append(lot)
			lots_expiries.append(lot_expiry)

		df_move_line['lot'] = lots
		df_move_line['lot_expiry'] = lots_expiries


	# # Añade el ticket correspondiente a cada move

	# In[11]:


	# Asigna el ticket correspondiente a cada movimiento
	if not df_move_line.empty and not df_flujo.empty:
		df_move_line['ticket'] = np.nan
		for i, flujo in df_flujo.iterrows():
			ticket = flujo.name
			moves = flujo['moves']
			
			for move in moves:
				df_move_line.loc[move, 'ticket'] = ticket
			


	# ### Formato

	# In[12]:


	if not df_flujo.empty:
		df_flujo['ticket_type_id'] = df_flujo['ticket_type_id'][df_flujo['ticket_type_id'] != False].apply(lambda x: x[1])
		df_flujo['user_id'] = df_flujo['user_id'][df_flujo['user_id'] != False].apply(lambda x: x[1])
		df_flujo['partner_id'] = df_flujo['partner_id'][df_flujo['partner_id'] != False].apply(lambda x: x[1])
		df_flujo['stage_id'] = df_flujo['stage_id'][df_flujo['stage_id'] != False].apply(lambda x: x[1])
		df_flujo['team_id'] = df_flujo['team_id'][df_flujo['team_id'] != False].apply(lambda x: x[1])
	if not df_product.empty:	
		df_product['owner_id'] = df_product['owner_id'][df_product['owner_id'] != False].apply(lambda x: x[1])
	if not df_move_line.empty:
		df_move_line['product_id'] = df_move_line['product_id'].apply(lambda x: x[0])
		df_move_line['location_dest_id'] = df_move_line['location_dest_id'][df_move_line['location_dest_id'] != False].apply(lambda x: x[1])
		df_move_line['location_id'] = df_move_line['location_id'][df_move_line['location_id'] != False].apply(lambda x: x[1])
		df_move_line['move_id'] = df_move_line['move_id'][df_move_line['move_id'] != False].apply(lambda x: x[1])
		df_move_line['owner_id'] = df_move_line['owner_id'][df_move_line['owner_id'] != False].apply(lambda x: x[1])
		df_move_line['lot_id'] = df_move_line['lot_id'][df_move_line['lot_id'] != False].apply(lambda x: x[1])
	if not df_picking.empty:
		df_picking['location_dest_id'] = df_picking['location_dest_id'][df_picking['location_dest_id'] != False].apply(lambda x: x[1])
		df_picking['location_id'] = df_picking['location_id'][df_picking['location_id'] != False].apply(lambda x: x[1])
		df_picking['owner_id'] = df_picking['owner_id'][df_picking['owner_id'] != False].apply(lambda x: x[1])
		df_picking['partner_id'] = df_picking['partner_id'][df_picking['partner_id'] != False].apply(lambda x: x[1])
		df_picking['cliente_final'] = df_picking['cliente_final'][df_picking['cliente_final'] != False].apply(lambda x: x[1])
	if not df_quant.empty:
		df_quant['product_id'] = df_quant['product_id'].apply(lambda x: x[0])
		df_quant['location_id'] = df_quant['location_id'].apply(lambda x: x[1])
		df_quant['owner_id'] = df_quant['owner_id'][df_quant['owner_id'] != False].apply(lambda x: x[1])
		df_quant.drop(columns=['lot_id'], inplace=True)
	if not df_sale.empty:
		df_sale['partner_id'] = df_sale['partner_id'][df_sale['partner_id'] != False].apply(lambda x : x[1])
		df_sale['helpdesk_ticket'] = df_sale['helpdesk_ticket'][df_sale['helpdesk_ticket'] != False].apply(lambda x : x[0])
		df_sale['user_id'] = df_sale['user_id'][df_sale['user_id'] != False].apply(lambda x : x[1])
		df_sale['warehouse_id'] = df_sale['warehouse_id'][df_sale['warehouse_id'] != False].apply(lambda x : x[1])
	if not df_sale_line.empty:
		df_sale_line['order_id'] = df_sale_line['order_id'][df_sale_line['order_id'] != False].apply(lambda x : x[0])
		df_sale_line['order_partner_id'] = df_sale_line['order_partner_id'][df_sale_line['order_partner_id'] != False].apply(lambda x : x[1])
		df_sale_line['product_id'] = df_sale_line['product_id'][df_sale_line['product_id'] != False].apply(lambda x : x[0])
	if not df_mrp.empty:
		df_mrp['helpdesk_ticket'] = df_mrp['helpdesk_ticket'][df_mrp['helpdesk_ticket'] != False].apply(lambda x : x[0])
		df_mrp['product_id'] = df_mrp['product_id'][df_mrp['product_id'] != False].apply(lambda x : x[0])
		df_mrp['routing_id'] = df_mrp['routing_id'][df_mrp['routing_id'] != False].apply(lambda x : x[1])
		df_mrp['user_id'] = df_mrp['user_id'][df_mrp['user_id'] != False].apply(lambda x : x[1])

	# # Ejemplo de renaming de columnas

	# In[13]:

	if not df_move_line.empty:
		df_move_line.rename(columns= {'id':'movimientos_id',
							'date':'fecha',
							'location_dest_id':'destino',
							'location_id':'origen',
							'name':'nombre_del_movimiento',
							'lot':'lote',
							'lot_expiry':'fecha_caducidad'}, inplace=True)

	if not df_product.empty:
		df_product.rename(columns= {'id':'product_id',
							   'name':'nombre',
							   'default_code' : 'referencia',
							   'owner_id':'propietario',
							   'x_coeficiente':'coeficiente',
							   'x_unidades_por_empaque': 'unidades_por_empaque',
							   'x_empaques_por_pallet': 'empaques_por_pallet',
							   'x_familia':'familia',
							   'x_pvp':'pvp', 
							   'x_registro_nacional':'registro_nacional',
							   'x_unidad_principal':'presentacion',
							   'x_unidad_secundaria':'unidad_secundaria',
							   'x_peso_empaque':'peso_por_empaque',
							   'x_volumen_empaque':'volumen_por_empaque',
							   'x_color_franja': 'color_de_franja',
							   'x_peso_bruto' : 'peso_bruto',
							   'x_peso_neto':'peso_neto',
							   'x_total_peso_pallet' : 'total_peso_pallet',
							   'x_tipo_empaque':'tipo_empaque',
							   'list_price': 'precio'}, inplace=True)

	if not df_quant.empty:
		df_quant.rename(columns= {'display_name':'nombre',
							 'location_id':'ubicacion',
							 'owner_id':'propietario',
							 'quantity':'cantidad',
							 'lot':'lote',
							 'lot_expiry':'fecha_expiracion',
							 'lot_alert' :'fecha_de_alerta'}, inplace=True)

	if not df_flujo.empty:
		df_flujo.rename(columns= {'id':'flujo_id',
							   'name':'nombre',
							   'create_date':'fecha_creado',
							   'x_datetime_en_proceso' : 'fecha_en_proceso',
							   'x_datetime_por_confirmar':'fecha_por_confirmar',
							   'x_datetime_resuelto':'fecha_resuelto'}, inplace=True)


	# In[14]:

	if not df_quant.empty and not df_product.empty:
		empaques = []
		for i,quant in df_quant.iterrows():
			product_id = quant['product_id']
			u_empaque = df_product.loc[product_id]['unidades_por_empaque']
			if quant['cantidad'] <=0 or u_empaque <=0:
				empaques.append(0)
			else:
				empaques.append(int(quant['cantidad']/u_empaque))

		df_quant['empaques'] = empaques

		unidades_sueltas = []
		for i,quant in df_quant.iterrows():
			product_id = quant['product_id']
			u_empaque = df_product.loc[product_id]['unidades_por_empaque']
			if quant['cantidad'] <=0 or u_empaque <=0:
				unidades_sueltas.append(0)
			else:
				unidades_sueltas.append(int(quant['cantidad']%u_empaque))
		df_quant['unidades_sueltas'] = unidades_sueltas


	# # Añade posiciones y peso a Existencias

	# In[15]:

	if not df_move_line.empty and not df_product.empty:
		empaques = []
		for i,move in df_move_line.iterrows():
			product_id = move['product_id']
			u_empaque = df_product.loc[product_id]['unidades_por_empaque']
			if move['qty_done'] <=0 or u_empaque <=0:
				empaques.append(0)
			else:
				empaques.append(int(move['qty_done']/u_empaque))

		df_move_line['empaques'] = empaques

		unidades_sueltas = []
		for i,move in df_move_line.iterrows():
			product_id = move['product_id']
			u_empaque = df_product.loc[product_id]['unidades_por_empaque']
			if move['qty_done'] <=0 or u_empaque <=0:
				unidades_sueltas.append(0)
			else:
				unidades_sueltas.append(int(move['qty_done']%u_empaque))

		df_move_line['unidades_sueltas'] = unidades_sueltas


	# In[16]:

	if not df_quant.empty and not df_product.empty:
		posiciones =[]
		pesos =[]
		for i, quant in df_quant.iterrows():
			producto = df_product.loc[quant['product_id']]
			if producto['empaques_por_pallet']<= 0 or quant['cantidad'] <=0:
				posicion = 0
				peso=0
			else:
				posicion = math.ceil(quant['empaques']/producto['empaques_por_pallet'])
				peso = quant['cantidad']*producto['peso_bruto']
			posiciones.append(posicion)
			pesos.append(peso)

		df_quant['posiciones'] = posiciones
		df_quant['peso_total'] = pesos


	# # Fill False with NaN

	# In[17]:

	if not df_product.empty:
		df_product.replace(False, np.nan, inplace=True)
	if not df_flujo.empty:
		df_flujo.replace(False, np.nan, inplace=True)
	if not df_move_line.empty:
		df_move_line.replace(False, np.nan, inplace=True)
	if not df_picking.empty:
		df_picking.replace(False, np.nan, inplace=True);
	if not df_sale.empty:
		df_sale['guia_remision'].replace(False,np.nan, inplace=True)
	if not df_mrp.empty:
		df_mrp.replace(False, np.nan, inplace = True)


	# In[18]:

	if not df_quant.empty:
		df_quant['lote'].replace(np.nan, 99, inplace=True)
		df_quant['propietario'].replace(np.nan, 'NO ASIGNADO', inplace=True)
		df_quant.replace(False, np.nan, inplace=True);
		df_flujo.drop(columns=['operaciones'], inplace=True);
		df_flujo.drop(columns=['moves'], inplace=True);







	# # Conexión con DB

	


	# In[20]:

	if not df_flujo.empty:
		df_flujo = df_flujo[['partner_id','ticket_type_id','stage_id','team_id','user_id','fecha_creado','fecha_en_proceso','fecha_por_confirmar','fecha_resuelto','__last_update','ciudad','description','helpdesk_ticket','guia_remision','tag_ids','tipo_reclamo','nombre']]

	if not df_move_line.empty:
		df_move_line = df_move_line[['move_id','product_id','lot_id','owner_id','picking_id','origen','destino','qty_done','remaining_stock','__last_update','lote','fecha_caducidad','ticket','empaques','unidades_sueltas']]
		
	if not df_product.empty:
		df_product = df_product[['referencia','nombre','propietario','coeficiente','empaques_por_pallet','familia','peso_por_empaque','pvp','registro_nacional','presentacion','unidad_secundaria','unidades_por_empaque','volumen_por_empaque','color_de_franja','peso_bruto','peso_neto','total_peso_pallet','tipo_empaque','__last_update', 'precio']]
	df_timestamp = pd.DataFrame([{'last_update':datetime.datetime.now()}])

	# In[21]:
	
	if not df_flujo.empty:
		df_flujo.to_sql('b_flujos', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP, 'fecha_creado': sqlalchemy.types.TIMESTAMP,'fecha_en_proceso':sqlalchemy.types.TIMESTAMP,'fecha_por_confirmar':sqlalchemy.types.TIMESTAMP, 'fecha_resuelto':sqlalchemy.types.TIMESTAMP}) 
	if not df_product.empty:
		df_product.to_sql('b_productos', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP})
	if not df_move_line.empty:
		df_move_line.to_sql('b_movimientos', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP, 'fecha_caducidad': sqlalchemy.types.TIMESTAMP, 'ticket': sqlalchemy.types.BIGINT}) 
	if not df_picking.empty:
		df_picking.to_sql('b_operaciones', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP, 'helpdesk_ticket' : sqlalchemy.types.BIGINT, 'date' : sqlalchemy.types.TIMESTAMP, 'date_done': sqlalchemy.types.TIMESTAMP})
	if not df_quant.empty:
		df_quant.to_sql('b_existencias', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP, 'fecha_de_alerta': sqlalchemy.types.TIMESTAMP,'fecha_expiracion': sqlalchemy.types.TIMESTAMP})
	if not df_sale.empty:
		df_sale_line.to_sql('b_ventas_linea', connection,  schema=schema_psql, if_exists='replace', dtype={'create_date': sqlalchemy.types.TIMESTAMP}) 
	if not df_mrp.empty:
		df_mrp.to_sql('b_manufactura', connection,  schema=schema_psql, if_exists='replace', dtype={'__last_update': sqlalchemy.types.TIMESTAMP, 'date_finished': sqlalchemy.types.TIMESTAMP})
	

	query1 = '''
	BEGIN TRANSACTION;
	CALL update_all();
	COMMIT TRANSACTION;
	'''
	connection.execute(query1)
	
	query2 = '''
	BEGIN TRANSACTION;
	CALL create_historico_existencias();
	COMMIT TRANSACTION;
	'''
	connection.execute(query2)
	
	df_timestamp.to_sql('database_timestamp', connection,  schema=schema_psql, if_exists='replace', dtype={'last_update': sqlalchemy.types.TIMESTAMP}) 
	