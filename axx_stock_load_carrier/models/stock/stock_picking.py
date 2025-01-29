from odoo import api, fields, models, _
from odoo import Command


class StockPickingInherited(models.Model):
    _inherit = "stock.picking"

    def _validations_axx_create_sale_line_carrier(self, stock_quant_package):
        if not self.sale_id:
            return False
        package_type = stock_quant_package.package_type_id
        loading_aid_product = package_type and package_type.axx_product_id
        if not loading_aid_product:
            return False
        if loading_aid_product.detailed_type != 'service' and not \
                (loading_aid_product._origin and loading_aid_product.sales_count > 0):
            loading_aid_product.write({'detailed_type': 'service'})
        package_already_added_to_sol = False
        for order_line in self.sale_id.order_line:
            if stock_quant_package in order_line.axx_stock_quant_package_ids:
                package_already_added_to_sol = True
        if package_already_added_to_sol:
            return False
        return loading_aid_product

    def _axx_create_sale_line_carrier(self, stock_quant_packages):
        self.ensure_one()
        sol_env = self.env['sale.order.line']
        for package in stock_quant_packages:
            loading_aid_product = self._validations_axx_create_sale_line_carrier(package)
            if not loading_aid_product:
                continue
            existing_sol = sol_env.browse()
            for order_line in self.sale_id.order_line:
                if order_line.axx_stock_quant_package_ids and order_line.product_id == loading_aid_product:
                    existing_sol = order_line
            if not existing_sol:
                sale_line_values = {
                    'order_id': self.sale_id.id,
                    'product_id': loading_aid_product.id,
                    'product_uom_qty': 1.0,
                    'qty_delivered': 1.0,
                    'price_unit': loading_aid_product.lst_price or 0.0,
                    'axx_stock_quant_package_ids': [Command.link(package.id)],
                    'sequence': self.sale_id.order_line and self.sale_id.order_line[-1].sequence or 99
                }
                sol_env.create(sale_line_values)
            else:
                existing_sol.write({
                    'product_uom_qty': existing_sol.product_uom_qty + 1.0,
                    'qty_delivered': existing_sol.qty_delivered + 1.0,
                    'axx_stock_quant_package_ids': [Command.link(package.id)]
                })
        return True
