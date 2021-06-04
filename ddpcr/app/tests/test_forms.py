# Status field should be dependent on if there is a value for the corresponding date.

import datetime

from django.test import TestCase
from django.utils import timezone

from app.models import AssayType, AssayLOT
from app.forms import AssayLotUpdateForm

#testar bara non-default forms...
class AssayLotUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)
# Borde vi testa om datumen är exakt samma också?
    def test_assay_lot_update_form_all_ok_values(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        date_inactivated = date_order + datetime.timedelta(weeks=4) #1 vecka sen
        #Maste inkludera alla obligatoriska falt
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })
        self.assertTrue(form.is_valid(), form.errors)

#inactivated
    def test_assay_lot_update_form_date_inactivated_before_activated_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=4) #1 vecka sen
        date_inactivated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_inactivated_before_validated_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=4) #1 vecka sen
        date_inactivated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_inactivated_before_scanned_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=4) #1 vecka sen
        date_inactivated = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_inactivated_before_order_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=2) #2 veckor sen
        date_inactivated = date_order - datetime.timedelta(weeks=1) #6 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_inactivated_wo_activated_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        # date_activated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        date_inactivated = date_order + datetime.timedelta(weeks=4) #1 vecka sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'volume_low': True, 'date_inactivated': date_inactivated, 'status': 'inactivated' })

#activated

    def test_assay_lot_update_form_date_activated_before_validated_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=2) #3 veckor sen

        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'status': 'activated' })
        self.assertFalse(form.is_valid(), form.errors)


    def test_assay_lot_update_form_date_activated_before_scanned_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=1) #4 veckor sen

        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'status': 'activated' })
        self.assertFalse(form.is_valid(), form.errors)


    def test_assay_lot_update_form_date_activated_before_scanned_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=1) #4 veckor sen

        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'status': 'activated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_activated_before_order_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        date_activated = date_order - datetime.timedelta(weeks=3) #2 veckor sen

        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'status': 'activated' })
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_activated_wo_validated_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        # date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        test_id = 'Test42'
        date_activated = date_order + datetime.timedelta(weeks=3) #2 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'test_id': test_id, \
                                    'date_activated': date_activated, 'volume_low': True, 'status': 'activated' })
        self.assertFalse(form.is_valid(), form.errors)

#validated
    def test_assay_lot_update_form_date_validated_wo_test_id_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        # test_id = 'Test42'
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'date_validated': date_validated, 'volume_low': False, 'status': 'validated'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_validated_before_scanned_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=2) #3 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        test_id = 'Test42'
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'test_id': test_id, 'date_validated': date_validated, \
                                    'volume_low': False, 'status': 'validated'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_validated_before_order_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order + datetime.timedelta(weeks=1) #4 veckor sen
        date_validated = date_order - datetime.timedelta(weeks=2) #7 veckor sen
        test_id = 'Test42'
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'test_id': test_id, 'date_validated': date_validated, \
                                    'volume_low': False, 'status': 'validated'})
        self.assertFalse(form.is_valid(), form.errors)

    def test_assay_lot_update_form_date_validated_wo_scanned_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        # date_scanned = date_order + datetime.timedelta(weeks=1) #3 veckor sen
        date_validated = date_order + datetime.timedelta(weeks=2) #4 veckor sen
        test_id = 'Test42'
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order,  \
                                    'lot': '4242-2', 'test_id': test_id, 'date_validated': date_validated, \
                                    'volume_low': False, 'status': 'validated'})
        self.assertFalse(form.is_valid(), form.errors)

# scanned
    def test_assay_lot_update_form_date_scanned_before_order_fail(self):
        assayType = AssayType.objects.get(id=1)
        date_order = datetime.date.today() - datetime.timedelta(weeks=5) #5 veckor sen
        date_scanned = date_order - datetime.timedelta(weeks=1) #6 veckor sen
        form = AssayLotUpdateForm(data={'assay': assayType,'date_order': date_order, 'date_scanned': date_scanned, \
                                    'lot': '4242-2', 'volume_low': False, 'status': 'scanned' })
        self.assertFalse(form.is_valid(), form.errors)
