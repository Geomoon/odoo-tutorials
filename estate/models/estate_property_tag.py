from odoo import fields, models 


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(string="Name", required=True)
    