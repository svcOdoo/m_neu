from odoo import models, fields, api
from odoo import tools

import logging
import re
import os
import csv

_logger = logging.getLogger(__name__)


class MarkanPostObject(models.TransientModel):
    _name = 'markant.post.object'
    _description = 'Markant Post Object'

    @api.model
    def update_paper_format(self):
        _logger.info("============= START: update_paper_format =============")
        paper_format_a4 = self.env.ref('base.paperformat_euro')
        new_paper_format = paper_format_a4.copy({'name': 'A4 Querformat', 'orientation': 'Landscape'})
        reports = self.env['ir.actions.report'].search(['|', ('paperformat_id', '=', paper_format_a4.id),
                                                        ('paperformat_id', '=', False)])
        reports.write({'paperformat_id': new_paper_format.id})
        _logger.info("============= END: update_paper_format =============")
        return True

    @api.model
    def recompute_location_full_seq(self):
        _logger.info("============= START: recompute_location_full_seq =============")
        locations = self.env['stock.location'].search([])
        if locations:
            locations.compute_axx_full_seq()
        _logger.info("============= END: recompute_location_full_seq =============")
        return True

    def recompute_location_full_seq2(self):
        self.recompute_location_full_seq()

    @api.model
    def set_signup_stock_parameters(self):
        _logger.info("============= START: set_signup_stock_parameters =============")
        settings = self.env['res.config.settings'].create({
            'group_stock_tracking_lot': True,
            'group_stock_packaging': True,
            'group_stock_multi_locations': True,
            'group_stock_production_lot': True,
            'group_lot_on_delivery_slip': False,
            'group_product_pricelist': True,
            'default_invoice_policy': 'delivery',
            'group_stock_adv_location': True,
        })
        settings.execute()
        _logger.info("============= END: set_signup_stock_parameters =============")
        return True

    @api.model
    def set_signup_stock_parameters2(self):
        _logger.info("============= START: set_signup_stock_parameters2 =============")
        settings = self.env['res.config.settings'].create({
            'group_lot_on_delivery_slip': False,
        })
        settings.execute()
        _logger.info("============= END: set_signup_stock_parameters2 =============")
        return True

    @api.model
    def set_default_barcode(self):
        _logger.info(" START: set_default_barcode ".center(60, '='))
        self.env.company.nomenclature_id = self.env.ref('barcodes.default_barcode_nomenclature')
        _logger.info(" START: set_default_barcode ".center(60, '='))

    @api.model
    def set_signup_sale_parameters(self):
        _logger.info("============= START: set_signup_sale_parameters =============")
        settings = self.env['res.config.settings'].create({
            'group_sale_order_template': True,
        })
        settings.execute()
        _logger.info("============= END: set_signup_sale_parameters =============")
        return True

    @api.model
    def setup_stock_operation_types_new(self):
        _logger.info(" START: setup_stock_operation_types ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])
        warehouse_ids and warehouse_ids.write({'delivery_steps': 'pick_pack_ship'})

        for warehouse in warehouse_ids:
            warehouse.pick_type_id.write({'use_create_lots': False})
            warehouse.pick_type_id.write({'restrict_scan_source_location': 'mandatory'})
            warehouse.pick_type_id.write({'restrict_put_in_pack': 'optional'})
            warehouse.pick_type_id.write({'barcode_validation_all_product_packed': True})

            warehouse.pack_type_id.write({'show_entire_packs': True})
            warehouse.pack_type_id.write({'show_operations': False})

            warehouse.out_type_id.write({'show_entire_packs': True})
            warehouse.out_type_id.write({'show_operations': False})

        _logger.info(" END: setup_stock_operation_types ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new2(self):
        _logger.info(" START: setup_stock_operation_types_new2 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.in_type_id.write({'show_operations': True})
            warehouse.in_type_id.write({'restrict_put_in_pack': 'mandatory'})

        _logger.info(" END: setup_stock_operation_types_new2 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new3(self):
        _logger.info(" START: setup_stock_operation_types_new3 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.pack_type_id.write({'create_backorder': 'always'})

        _logger.info(" END: setup_stock_operation_types_new3 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new4(self):
        _logger.info(" START: setup_stock_operation_types_new4 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.out_type_id.write({'create_backorder': 'always'})

        _logger.info(" END: setup_stock_operation_types_new4 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new5(self):
        _logger.info(" START: setup_stock_operation_types_new5 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.pick_type_id.write({'create_backorder': 'always'})

        _logger.info(" END: setup_stock_operation_types_new5 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new6(self):
        _logger.info(" START: setup_stock_operation_types_new6 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.int_type_id.write({'axx_default_package_move': True})

        _logger.info(" END: setup_stock_operation_types_new6 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new7(self):
        _logger.info(" START: setup_stock_operation_types_new7 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.pick_type_id.write({'use_create_lots': False})

        _logger.info(" END: setup_stock_operation_types_new7 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_new8(self):
        _logger.info(" START: setup_stock_operation_types_new8 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.pick_type_id.write({'create_backorder': 'always'})

        _logger.info(" END: setup_stock_operation_types_new8 ".center(60, '='))

    @api.model
    def setup_stock_operation_types_int_1(self):
        _logger.info(" START: setup_stock_operation_types_int_1 ".center(60, '='))
        warehouse_ids = self.env['stock.warehouse'].search([])

        for warehouse in warehouse_ids:
            warehouse.in_type_id.write({'use_create_lots': True})

        _logger.info(" END: setup_stock_operation_types_int_1 ".center(60, '='))

    @api.model
    def setup_stock_scheduler(self):
        _logger.info(" START: setup_stock_scheduler ".center(60, '='))
        scheduler_cron = self.sudo().env.ref('stock.ir_cron_scheduler_action')
        scheduler_cron.write({
            'interval_type': 'minutes',
            'interval_number': 15
        })

        _logger.info(" END: setup_stock_scheduler ".center(60, '='))

    @api.model
    def setup_barcode_nomenclatures2(self):
        _logger.info(" START: setup_barcode_nomenclatures ".center(60, '='))

        default_gs1_nomenclature = self.env.ref('barcodes_gs1_nomenclature.default_gs1_nomenclature')
        default_barcode_nomenclature = self.env.ref('barcodes.default_barcode_nomenclature')

        incoming_operation_types = self.env['stock.picking.type'].search([('code', '=', 'incoming')])
        other_operation_types = self.env['stock.picking.type'].search([('code', '!=', 'incoming')])

        incoming_operation_types.write({'axx_nomenclature_id': default_gs1_nomenclature.id})
        other_operation_types.write({'axx_nomenclature_id': default_barcode_nomenclature.id})

        settings = self.env['res.config.settings'].create({
            'barcode_nomenclature_id': default_gs1_nomenclature.id
        })
        settings.execute()

        _logger.info(" END: setup_barcode_nomenclatures ".center(60, '='))
