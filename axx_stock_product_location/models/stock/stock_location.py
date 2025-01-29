from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    def axx_is_child_of(self, main_location):
        """
        Checks whether the current stock location is a child of the specified location.

        :param main_location: The main location to check against.
        :return: True if the current stock location is a child of the main location, False otherwise.
        """
        if self.location_id:
            if self.location_id == main_location:
                return True
            else:
                return self.location_id.axx_is_child_of(main_location)
        else:
            return False
