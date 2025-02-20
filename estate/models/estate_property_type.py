from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Propety Type Model"

    name = fields.Char(string="Name", required=True)
