from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    def _default_partner_id(self):
        return self.env.user

    active = fields.Boolean(default=True, invisible=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ], 
        copy=False,
        required=True,
        default="new",
    )
    name = fields.Char(string="Title", default="New House")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=_default_date_availability)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
        ],
    )

    # Relations
    property_type_id = fields.Many2one("estate.property.type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=_default_partner_id)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area  + property.garden_area

    total_area = fields.Float(string="Total Area", compute="_compute_total_area")


    @api.depends('offer_ids')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max( property.offer_ids.mapped('price') or [0] )

    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    # On change
    # on change method's are executed only in form view context with 1 record
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
