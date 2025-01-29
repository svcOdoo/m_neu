from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'
    _order = 'axx_full_seq, id'  # required for significant performance increase, see comment below
    _rec_name = 'name'
    _rec_names_search = ['barcode', 'name', 'complete_name']

# SELECT "stock_location".id FROM "stock_location" WHERE (("stock_location"."active" = true) AND ("stock_location"."
# parent_path"::text like '1/7/8/%')) ORDER BY  "stock_location"."complete_name" ,"stock_location"."id"
# -- 4,392 sec
#
# SELECT "stock_location".id FROM "stock_location" WHERE (("stock_location"."active" = true) AND ("stock_location".
# "parent_path"::text like '1/7/8/%'))
# -- 0,110 sec
#
# SELECT "stock_location".id FROM "stock_location" WHERE (("stock_location"."active" = true) AND ("stock_location".
# "parent_path"::text like '1/7/8/%')) ORDER BY  "stock_location"."axx_full_seq" ,"stock_location"."id"
# -- 0,144
