from django.urls import path

from . import views

# app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('assay/', views.AssayTypeView.as_view(), name='assayType'),
    path('assay/create/', views.AssayTypeCreate.as_view(), name='assayType-create'),
    path('assay/<int:pk>/', views.AssayTypeDetailView.as_view(), name='assayType-detail'),
    path('assay/<int:pk>/update/', views.AssayTypeUpdate.as_view(), name='assayType-update'),
    path('assay/<int:pk>/delete/', views.AssayTypeDelete.as_view(), name='assayType-delete'),

    path('lots/', views.AssayLotView.as_view(), name='assayLot'),
    path('lots/create/', views.AssayLotCreate.as_view(), name='assayLot-create'),
    path('lots/<int:pk>/', views.AssayLotDetailView.as_view(), name='assayLot-detail'),
    path('lots/<int:pk>/update/', views.AssayLotUpdate.as_view(), name='assayLot-update'),
    path('lots/<int:pk>/delete/', views.AssayLotDelete.as_view(), name='assayLot-delete'),

    path('patients/', views.AssayPatientView.as_view(), name='assayPatient'),
    path('patients/create/', views.AssayPatientCreate.as_view(), name='assayPatient-create'),
    path('patients/<int:pk>/', views.AssayPatientDetailView.as_view(), name='assayPatient-detail'),
    path('patients/<int:pk>/update/', views.AssayPatientUpdate.as_view(), name='assayPatient-update'),
    path('patients/<int:pk>/delete/', views.AssayPatientDelete.as_view(), name='assayPatient-delete'),

    path('enzymes/', views.EnzymeView.as_view(), name='enzyme'),
    path('enzymes/create/', views.EnzymeCreate.as_view(), name='enzyme-create'),
    path('enzymes/<int:pk>/update/', views.EnzymeUpdate.as_view(), name='enzyme-update'),
]
