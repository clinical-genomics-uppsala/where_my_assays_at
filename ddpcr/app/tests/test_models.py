from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

from app.models import Enzyme, AssayType, AssayLOT, AssayPatient
# Do we need to test that dates in future fail?

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass
#
#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass
#
#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)
class EnzymeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up a non-modified objects used by all test methods
        Enzyme.objects.create(name = 'AluI')

    def test_name_label(self):
        enzyme = Enzyme.objects.get(id=1)
        field_label = enzyme._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        enzyme = Enzyme.objects.get(id=1)
        max_length = enzyme._meta.get_field('name').max_length
        self.assertEqual(max_length, 4)

# borde vi testa choices pa ngt satt?
    def test_object_name_is_name(self):
        enzyme = Enzyme.objects.get(id=1)
        expected_object_name = f'{enzyme.name}'
        self.assertEqual(expected_object_name, str(enzyme))


class AssayTypeModelTest(TestCase):
    @classmethod
    #Borde ha anvant Model baker? https://github.com/model-bakers/model_bakery
    def setUpTestData(cls):
        #Set up a non-modified objects used by all test methods
        AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)

    def test_assay_id_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('assay_id').verbose_name
        self.assertEqual(field_label, 'assay id')

    def test_assay_id_sec_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('assay_id_sec').verbose_name
        self.assertEqual(field_label, 'assay id sec')

    def test_gene_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('gene').verbose_name
        self.assertEqual(field_label, 'gene')

    def test_sequence_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('sequence').verbose_name
        self.assertEqual(field_label, 'sequence')

    def test_ref_build_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('ref_build').verbose_name
        self.assertEqual(field_label, 'ref build')

    def test_chromosome_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('chromosome').verbose_name
        self.assertEqual(field_label, 'chromosome')

    def test_position_from_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('position_from').verbose_name
        self.assertEqual(field_label, 'position from')

    def test_position_to_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('position_to').verbose_name
        self.assertEqual(field_label, 'position to')

    def test_transcript_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('transcript').verbose_name
        self.assertEqual(field_label, 'transcript')

    def test_cdna_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('cdna').verbose_name
        self.assertEqual(field_label, 'cdna')

    def test_protein_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('protein').verbose_name
        self.assertEqual(field_label, 'protein')

    def test_enzyme_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('enzyme').verbose_name
        self.assertEqual(field_label, 'enzyme')

    def test_temperature_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('temperature').verbose_name
        self.assertEqual(field_label, 'temperature')

    def test_status_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_comment_label(self):
        assayType = AssayType.objects.get(id=1)
        field_label = assayType._meta.get_field('comment').verbose_name
        self.assertEqual(field_label, 'comment')

    def test_assay_id_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('assay_id').max_length
        self.assertEqual(max_length, 100)

    def test_assay_id_sec_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('assay_id_sec').max_length
        self.assertEqual(max_length, 100)

    def test_gene_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('gene').max_length
        self.assertEqual(max_length, 100)

    def test_sequence_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('sequence').max_length
        self.assertEqual(max_length, 500)

    def test_ref_build_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('ref_build').max_length
        self.assertEqual(max_length, 4)

    def test_transcript_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('transcript').max_length
        self.assertEqual(max_length, 100)

    def test_cdna_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('cdna').max_length
        self.assertEqual(max_length, 100)

    def test_protein_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('protein').max_length
        self.assertEqual(max_length, 100)

    def test_comment_max_length(self):
        assayType = AssayType.objects.get(id=1)
        max_length = assayType._meta.get_field('comment').max_length
        self.assertEqual(max_length, 500)

    def test_enzyme_many_to_many(self):
        assayType = AssayType.objects.get(id=1)
        enzymeOne = Enzyme.objects.create(name = 'A1')
        enzymeTwo = Enzyme.objects.create(name = 'C1')
        assayType.enzyme.set([enzymeOne.pk, enzymeTwo.pk])
        self.assertEqual(assayType.enzyme.count(), 2)

# Borde vi testa integer, choices pa ngt satt?

    def test_object_name_is_assay(self):
        assayType = AssayType.objects.get(id=1)
        expected_object_name = f'{assayType.assay_id}'
        self.assertEqual(expected_object_name, str(assayType))

    def test_get_absolut_url(self):
        assayType = AssayType.objects.get(id=1)
        #This will also fail if urlconf is not defined
        self.assertEqual(assayType.get_absolute_url(), '/app/assay/1/')


class AssayLOTModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)
        AssayLOT.objects.create(assay = assay, date_order=timezone.now() + timedelta(days=1), \
                                date_scanned = timezone.now() + timedelta(days = 1), lot = '42424242',\
                                date_validated = timezone.now() + timedelta(days = 1), \
                                date_activated = timezone.now() + timedelta(days = 1), volume_low = False, \
                                date_inactivated = timezone.now() + timedelta(days = 1), status = 'ordered')

    def test_assay_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('assay').verbose_name
        self.assertEqual(field_label, 'assay')

    def test_date_order_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('date_order').verbose_name
        self.assertEqual(field_label, 'date ordered')

    def test_date_scanned_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('date_scanned').verbose_name
        self.assertEqual(field_label, 'date scanned')

    def test_lot_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('lot').verbose_name
        self.assertEqual(field_label, 'lot')

    def test_date_validated_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('date_validated').verbose_name
        self.assertEqual(field_label, 'date validated')

    def test_test_id_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('test_id').verbose_name
        self.assertEqual(field_label, 'test id')

    def test_date_activated_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('date_activated').verbose_name
        self.assertEqual(field_label, 'date activated')

    def test_volume_low_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('volume_low').verbose_name
        self.assertEqual(field_label, 'volume low')

    def test_date_inactivated_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('date_inactivated').verbose_name
        self.assertEqual(field_label, 'date inactivated')

    def test_freezer_id_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('freezer_id').verbose_name
        self.assertEqual(field_label, 'freezer id')

    def test_box_position_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('box_position').verbose_name
        self.assertEqual(field_label, 'box position')

    def test_comment_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('comment').verbose_name
        self.assertEqual(field_label, 'comment')

    def test_status_label(self):
        assayLot = AssayLOT.objects.get(id=1)
        field_label = assayLot._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_lot_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('lot').max_length
        self.assertEqual(max_length, 10)

    def test_test_id_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('test_id').max_length
        self.assertEqual(max_length, 20)

    def test_freezer_id_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('freezer_id').max_length
        self.assertEqual(max_length, 10)

    def test_box_position_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('box_position').max_length
        self.assertEqual(max_length, 20)

    def test_comment_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('comment').max_length
        self.assertEqual(max_length, 500)

    def test_status_max_length(self):
        assayLot = AssayLOT.objects.get(id=1)
        max_length = assayLot._meta.get_field('status').max_length
        self.assertEqual(max_length, 15)

    #Testa att future dates inte funkar och att det är det som raises error.
    def test_date_order_not_in_future(self):
        assayLot = AssayLOT.objects.get(id=1)
        try:
            assayLot.full_clean()
        except ValidationError as e:
            self.assertTrue('date_order' in e.message_dict)

    def test_date_scanned_not_in_future(self):
        assayLot = AssayLOT.objects.get(id=1)
        try:
            assayLot.full_clean()
        except ValidationError as e:
            self.assertTrue('date_scanned' in e.message_dict)

    def test_date_validated_not_in_future(self):
        assayLot = AssayLOT.objects.get(id=1)
        try:
            assayLot.full_clean()
        except ValidationError as e:
            self.assertTrue('date_validated' in e.message_dict)

    def test_date_activated_not_in_future(self):
        assayLot = AssayLOT.objects.get(id=1)
        try:
            assayLot.full_clean()
        except ValidationError as e:
            self.assertTrue('date_activated' in e.message_dict)

    def test_date_inactivated_not_in_future(self):
        assayLot = AssayLOT.objects.get(id=1)
        try:
            assayLot.full_clean()
        except ValidationError as e:
            self.assertTrue('date_inactivated' in e.message_dict)

    def test_object_name_is_lot(self):
        assayLot = AssayLOT.objects.get(id=1)
        expected_object_name = f'{assayLot.lot}'
        self.assertEqual(expected_object_name, str(assayLot))

    def test_get_absolut_url(self):
        assayLot = AssayLOT.objects.get(id=1)
        #This will also fail if urlconf is not defined
        self.assertEqual(assayLot.get_absolute_url(), '/app/lots/1/')


class AssayPatientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up a non-modified objects used by all test methods
        assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)
        AssayPatient.objects.create(study_id = 'T42', assay = assay, date_added = timezone.now() + timedelta(days = 1))

    def test_assay_label(self):
        assayPatient = AssayPatient.objects.get(id=1)
        field_label = assayPatient._meta.get_field('assay').verbose_name
        self.assertEqual(field_label, 'assay')

    def test_study_id_label(self):
        assayPatient = AssayPatient.objects.get(id=1)
        field_label = assayPatient._meta.get_field('study_id').verbose_name
        self.assertEqual(field_label, 'study id')

    def test_date_addded_label(self):
        assayPatient = AssayPatient.objects.get(id=1)
        field_label = assayPatient._meta.get_field('date_added').verbose_name
        self.assertEqual(field_label, 'date added')

    def test_comment_label(self):
        assayPatient = AssayPatient.objects.get(id=1)
        field_label = assayPatient._meta.get_field('study_id').verbose_name
        self.assertEqual(field_label, 'study id')

    def test_study_id_max_length(self):
        assayPatient = AssayPatient.objects.get(id=1)
        max_length = assayPatient._meta.get_field('study_id').max_length
        self.assertEqual(max_length, 10)

    def test_comment_max_length(self):
        assayPatient = AssayPatient.objects.get(id=1)
        max_length = assayPatient._meta.get_field('comment').max_length
        self.assertEqual(max_length, 500)

    def test_date_added_not_in_future(self):
        assayPatient = AssayPatient.objects.get(id=1)
        try:
            assayPatient.full_clean()
        except ValidationError as e:
            self.assertTrue('date_added' in e.message_dict)

    def test_object_name_is_assay_underline_studyid(self):
        assayPatient = AssayPatient.objects.get(id=1)
        expected_object_name = f'{assayPatient.assay}_{assayPatient.study_id}'
        self.assertEqual(expected_object_name, str(assayPatient))

    def test_get_absolut_url(self):
        assayPatient = AssayPatient.objects.get(id=1)
        #This will also fail if urlconf is not defined
        self.assertEqual(assayPatient.get_absolute_url(), '/app/patients/1/')
