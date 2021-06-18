from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from app.models import Enzyme, AssayType, AssayLOT, AssayPatient
#Test index view?
# redirect if not logged in, test num assays? num visits?
class AssayTypeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        # test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD') # incase of different kinds of users

        test_user1.save()
        # test_user2.save()
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

    def test_create_new_link(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("assayType"))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">New</span></button></a>' % reverse("assayType-create"), html=True)

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayType"))
        self.assertContains(response, '<a href="%s"><button type="button" class="btn btn-light ">{% bs_icon "pencil-square" %}</button></a>' % reverse("assayType-update", args=[pk]), html=True)


# DetailView
#Borde man testa att alla lots displays? How?
    def test_redirect_if_not_logged_in_assayDetail(self):
        pk=3 #Gar nog att losa snyggare?
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
        pk=3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayType-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaytype_detail.html')

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayType-detail", args=[pk]))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">Update record</span></button></a>' % reverse("assayType-update", args=[pk]), html=True)

    # def test_delete_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     pk=3
    #     response = self.client.get(reverse("assayType-detail", args=[pk]))
    #     self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-danger text-light">Delete record</span></button></a>' % reverse("assayType-delete", args=[pk]), html=True)

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

class AssayLotUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        # test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        # test_user2.save()
        #Set up number of AssayTypes to test paginate
        number_of_assayLots = 13
        assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)

        for assayLot_id in range(number_of_assayLots):
            AssayLOT.objects.create(assay = assay, date_order=timezone.now() + timedelta(days=1),
                                        date_scanned = timezone.now() + timedelta(days = 1), lot = f'Test{assayLot_id}',
                                        date_validated = timezone.now() + timedelta(days = 1),
                                        date_activated = timezone.now() + timedelta(days = 1), volume_low = False,
                                        date_inactivated = timezone.now() + timedelta(days = 1), status = 'ordered',
            )

# Listview
    def test_redirect_if_not_logged_in_assayLotList(self):
        response = self.client.get(reverse('assayLot'))
        self.assertRedirects(response, '/accounts/login/?next=/app/lots/')

    def test_view_url_exists_at_desired_location_assayLotList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/lots/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayLotList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayLotList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaylot_list.html')

    def test_pagination_is_ten_assayLotList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaylot_list']), 10) #html-file

    def test_lists_all_assayLotType(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaylot_list']), 3)

    def test_create_new_link(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("assayLot"))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">New</span></button></a>' % reverse("assayLot-create"), html=True)

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayLot"))
        self.assertContains(response, '<a href="%s"><button type="button" class="btn btn-light ">{% bs_icon "pencil-square" %}</button></a>' % reverse("assayLot-update", args=[pk]), html=True)

# DetailView
    def test_redirect_if_not_logged_in_assayLotDetail(self):
        pk=3 #Gar nog att losa snyggare?
        response = self.client.get(reverse('assayLot-detail', args=[pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/lots/'+str(pk)+'/')

    def test_view_url_exists_at_desired_location_assayLotDetail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/lots/3/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayLotDetail(self):
        pk=3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayLotDetail(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaylot_detail.html')

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayLot-detail", args=[pk]))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">Update record</span></button></a>' % reverse("assayLot-update", args=[pk]), html=True)
    #
    # def test_delete_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     pk=3
    #     response = self.client.get(reverse("assayLot-detail", args=[pk]))
    #     self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-danger text-light">Delete record</span></button></a>' % reverse("assayLot-delete", args=[pk]), html=True)


# CreateView
    def test_redirect_if_not_logged_in_assayLotCreate(self):
        response = self.client.get(reverse('assayLot-create'))
        self.assertRedirects(response, '/accounts/login/?next=/app/lots/create/')

    def test_view_url_exists_at_desired_location_assayLotCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/lots/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayLotCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayLotCreate(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaylot_form.html')

# UpdateView
    def test_redirect_if_not_logged_in_assayLotUpdate(self):
        pk = 3
        response = self.client.get(reverse('assayLot-update', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/lots/'+str(pk)+'/update/')

    def test_view_url_exists_at_desired_location_assayLotUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/lots/'+str(pk)+'/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayLotUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-update', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayLotUpdate(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-update', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaylot_form.html')

# DeleteView
    def test_redirect_if_not_logged_in_assayLotDelete(self):
        pk = 3
        response = self.client.get(reverse('assayLot-delete', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/lots/'+str(pk)+'/delete/')

    def test_view_url_exists_at_desired_location_assayLotDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/lots/'+str(pk)+'/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayLotDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayLotDelete(self): #Kanske inte ens ska testas? Eller? "ndra om delar upp create och update"
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayLot-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaylot_confirm_delete.html')


class AssayPatientUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        # test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        # test_user2.save()
        #Set up number of AssayTypes to test paginate
        number_of_assayPatients = 13
        assay = AssayType.objects.create(assay_id = 'Test42', gene = 'TP53', ref_build = 'hg19', chromosome = '17', status = 4)

        for assayPatient_id in range(number_of_assayPatients):
            AssayPatient.objects.create(study_id = f'Test{assayPatient_id}', assay = assay, date_added = timezone.now() + timedelta(days = 1) )

# Listview
    def test_redirect_if_not_logged_in_assayPatientList(self):
        response = self.client.get(reverse('assayPatient'))
        self.assertRedirects(response, '/accounts/login/?next=/app/patients/')

    def test_view_url_exists_at_desired_location_assayPatientList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/patients/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayPatientList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayPatientList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaypatient_list.html')

    def test_pagination_is_ten_assayPatientList(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaypatient_list']), 10) #html-file

    def test_lists_all_assayPatientType(self): # Waring if class Meta ordering not activated
        # Get second page and confirm it has (exactly) remaining 3 items
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['assaypatient_list']), 3)

    def test_create_new_link(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("assayPatient"))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">New</span></button></a>' % reverse("assayPatient-create"), html=True)

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayPatient"))
        self.assertContains(response, '<a href="%s"><button type="button" class="btn btn-light ">{% bs_icon "pencil-square" %}</button></a>' % reverse("assayPatient-update", args=[pk]), html=True)

# DetailView
    def test_redirect_if_not_logged_in_assayPatientDetail(self):
        pk=3 #Gar nog att losa snyggare?
        response = self.client.get(reverse('assayPatient-detail', args=[pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/patients/'+str(pk)+'/')

    def test_view_url_exists_at_desired_location_assayPatientDetail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/patients/3/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayPatientDetail(self):
        pk=3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayPatientDetail(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-detail', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaypatient_detail.html')

    def test_update_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        pk=3
        response = self.client.get(reverse("assayPatient-detail", args=[pk]))
        self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-light text-dark">Update record</span></button></a>' % reverse("assayPatient-update", args=[pk]), html=True)

    # def test_delete_button(self): #kommer ju faila om vi byter design pa knappen, hur fixar man?
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     pk=3
    #     response = self.client.get(reverse("assayPatient-detail", args=[pk]))
    #     self.assertContains(response, '<a href="%s"><button type="button" class = "btn btn-default"><span class="badge bg-danger text-light">Delete record</span></button></a>' % reverse("assayPatient-delete", args=[pk]), html=True)


# CreateView
    def test_redirect_if_not_logged_in_assayPatientCreate(self):
        response = self.client.get(reverse('assayPatient-create'))
        self.assertRedirects(response, '/accounts/login/?next=/app/patients/create/')

    def test_view_url_exists_at_desired_location_assayPatientCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/patients/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayPatientCreate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayPatientCreate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaypatient_form.html')

# UpdateView
    def test_redirect_if_not_logged_in_assayPatientUpdate(self):
        pk = 3
        response = self.client.get(reverse('assayPatient-update', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/patients/'+str(pk)+'/update/')

    def test_view_url_exists_at_desired_location_assayPatientUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/patients/'+str(pk)+'/update/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayPatientUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-update', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayPatientUpdate(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-update', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaypatient_form.html')

# DeleteView
    def test_redirect_if_not_logged_in_assayPatientDelete(self):
        pk = 3
        response = self.client.get(reverse('assayPatient-delete', args = [pk]))
        self.assertRedirects(response, '/accounts/login/?next=/app/patients/'+str(pk)+'/delete/')

    def test_view_url_exists_at_desired_location_assayPatientDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/app/patients/'+str(pk)+'/delete/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_assayPatientDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_assayPatientDelete(self):
        pk = 3
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('assayPatient-delete', args = [pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/assaypatient_confirm_delete.html')
