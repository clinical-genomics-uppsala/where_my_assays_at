from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from app.models import Enzyme, AssayType, AssayLOT, AssayPatient

class AssayTypeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        #Set up number of AssayTypes to test paginate
        number_of_assayTypes = 13

        for assayType_id in range(number_of_assayTypes):
            AssayType.objects.create(
                assay_id = f'Test {assayType_id}',
                gene = 'TP53',
                ref_build = 'hg19',
                chromosome = '17',
                status = 4,
            )
# Listview
    def test_redirect_if_not_logged_in_assayList(self):
        response = self.client.get(reverse('assayType'))
        self.assertRedirects(response, '/accounts/login/?next=/app/assay/')

    def test_view_url_exists_at_desired_location_assayList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/assay/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_list.html')

    def test_pagination_is_ten_assayList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaytype_list']), 10) #html-file

    def test_lists_all_assayType(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaytype_list']), 3)
    #borde det vara tester for detail, create, update och delete ocksa?

# DetailView
    def test_redirect_if_not_logged_in_assayDetail(self):
        pk=3
        response = self.client.get(reverse('assayType-detail', args=[pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/assay/'+str(pk)+'/')

    def test_view_url_exists_at_desired_location_assayDetail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/assay/3/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayDetail(self):
        pk=3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayDetail(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_detail.html')

# CreateView
    def test_redirect_if_not_logged_in_assayCreate(self):
        response = self.client.get(reverse('assayType-create'))
        self.assertRedirects(response, '/accounts/login/?next=/app/assay/create/')

    def test_view_url_exists_at_desired_location_assayCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/assay/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayCreate(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_form.html')
        
# UpdateView
    def test_redirect_if_not_logged_in_assayUpdate(self):
        pk = 3
        response = self.client.get(reverse('assayType-update', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/assay/'+str(pk)+'/update/')

    def test_view_url_exists_at_desired_location_assayUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/assay/'+str(pk)+'/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-update', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayUpdate(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-update', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_form.html')

# DeleteView
    def test_redirect_if_not_logged_in_assayDelete(self):
        pk = 3
        response = self.client.get(reverse('assayType-delete', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/assay/'+str(pk)+'/delete/')

    def test_view_url_exists_at_desired_location_assayDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/assay/'+str(pk)+'/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayDelete(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_confirm_delete.html')

# class AssayLotUpdateFormTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create two users
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
#
#         test_user1.save()
#         test_user2.save()
#         #Set up number of AssayTypes to test paginate
#         number_of_assayLots = 13
#         assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)
#
#         for assayLot_id in range(number_of_assayLots):
#             AssayLOT.objects.create(assay = assay, date_order=timezone.now() + timedelta(days=1),
#                                         date_scanned = timezone.now() + timedelta(days = 1), lot = f'Test{assayLot_id}',
#                                         date_validated = timezone.now() + timedelta(days = 1),
#                                         date_activated = timezone.now() + timedelta(days = 1), volume_low = False,
#                                         date_inactivated = timezone.now() + timedelta(days = 1), status = 'ordered',
#             )
#
#         # def test_redirect_if_not_logged_in(self):
#         #     response = self.client.get(reverse('my-borrowed'))
#         #     self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#
#     def test_view_url_exists_at_desired_location(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get('/app/lots/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('assayLot'))
#         self.assertEqual(response.status_code, 200)
#
#
#     def test_view_uses_correct_template(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('assayLot'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'app/assaylot_list.html')
#
#     def test_pagination_is_ten(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('assayLot'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertEqual(len(response.context['assaylot_list']), 10) #html-file
#
#     def test_lists_all_assayLot(self):
#         # Get second page and confirm it has (exactly) remaining 3 items
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('assayLot')+'?page=2')
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('is_paginated' in response.context)
#         self.assertTrue(response.context['is_paginated'] == True)
#         self.assertEqual(len(response.context['assaylot_list']), 3)
#
# class AssayPatientUpdateFormTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create two users
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
#
#         test_user1.save()
#         test_user2.save()
#         #Set up number of AssayTypes to test paginate
#         number_of_assayPatients = 13
#         assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)
#
#         for assayPatient_id in range(number_of_assayPatients):
#             AssayPatient.objects.create(study_id = f'Test{assayPatient_id}', assay = assay, date_added = timezone.now() + timedelta(days = 1) )
#

    # def test_redirect_if_not_logged_in(self):
    #     response = self.client.get(reverse('my-borrowed'))
    # #     self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
    #
    # def test_view_url_exists_at_desired_location(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get('/app/patients/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_view_url_accessible_by_name(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('assayPatient'))
    #     self.assertEqual(response.status_code, 200)
    #
    #
    # def test_view_uses_correct_template(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('assayPatient'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'app/assaypatient_list.html')
    #
    # def test_pagination_is_ten(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('assayPatient'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEqual(len(response.context['assaypatient_list']), 10) #html-file
    #
    # def test_lists_all_assayPatient(self):
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('assayPatient')+'?page=2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEqual(len(response.context['assaypatient_list']), 3)
