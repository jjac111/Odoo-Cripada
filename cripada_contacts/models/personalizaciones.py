# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from odoo import models, fields, api



class ResPartner(models.Model):
	_inherit = 'res.partner'

	codigo_cliente = fields.Char(
		string="Codigo Cliente",
		store=True,
	)
