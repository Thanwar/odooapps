from odoo import api, fields, models

class SaleProduct(models.Model):
    _inherit = "product.template"
    product_mrp = fields.Float(string='Product MRP', default=1.0, digits='Product Price',
                               help="Price after 10% increase",
                               compute='_compute_mrp', readonly=True)

    def _compute_mrp(self):
        original_price = self.list_price
        increased_amount = (original_price * 0.1)
        after_increase = original_price + increased_amount
        self.product_mrp = after_increase