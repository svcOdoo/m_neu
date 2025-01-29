from odoo import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        """
        Retrieve the quants for a given product and location, applying the appropriate removal strategy.
        When the product's standard location (axx_standard_location_id) is set and the location is a
        child of the main warehouse's lot_stock_id, prioritize the quants in the standard location.
        We must be careful about performance here, _gather is called many times even if validating just one picking
        with one move line

        :return: Recordset of stock.quant records sorted based on the removal strategy and
                 prioritizing the standard location when applicable.
        """
        quants = super(StockQuant, self)._gather(product_id, location_id, lot_id, package_id, owner_id, strict)

        if not self.env.context.get('import_file', False):
            standard_loc_id = product_id.axx_standard_location_id.id if product_id.axx_standard_location_id else False
            main_loc = location_id.warehouse_id.lot_stock_id
            if standard_loc_id and main_loc and (location_id == main_loc or location_id.axx_is_child_of(main_loc)):
                matching_quants = quants.filtered(lambda q: q.location_id.id == standard_loc_id)
                non_matching_quants = quants - matching_quants

                result_quants = matching_quants + non_matching_quants
                return result_quants

        return quants
