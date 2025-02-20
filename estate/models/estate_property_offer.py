from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"


    @api.depends('validity', 'property_id.create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.property_id.create_date or fields.Date.today()) + relativedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.property_id.create_date or fields.Date.today()
            offer.validity = (offer.date_deadline - create_date.date()).days

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status", 
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Salesman", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, invisible=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise exceptions.UserError("Error, there is already a accepted offer")
        self.status = "accepted"


