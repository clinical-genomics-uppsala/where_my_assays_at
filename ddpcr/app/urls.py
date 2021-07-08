from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('assays/', views.AssayList.as_view(), name='assays'),
    path('assays/create/', views.AssayCreate.as_view(), name='assay-create'),
    path('assays/update/<int:pk>/', views.AssayUpdate.as_view(), name='assay-update'),

    path("lots/", views.LotList.as_view(), name="lots"),
    path("lots/update/<int:pk>", views.LotUpdate.as_view(), name="lot-update"),
    path("lots/order/", views.LotOrderList.as_view(), name="lot-order-list"),
    path("lots/order/<int:pk>", views.LotOrder.as_view(), name="lot-order"),
    path("lots/scan/", views.LotScanList.as_view(), name="lot-scan-list"),
    path("lots/scan/<int:pk>", views.LotScan.as_view(), name="lot-scan"),
    path("lots/validate/", views.LotValidateList.as_view(), name="lot-validate-list"),
    path("lots/validate/<int:pk>", views.LotValidate.as_view(), name="lot-validate"),
    path("lots/activate/", views.LotActivateList.as_view(), name="lot-activate-list"),
    path("lots/activate/<int:pk>", views.LotActivate.as_view(), name="lot-activate"),
    path("lots/lowvol/", views.LotLowVolumeList.as_view(), name="lot-low-volume-list"),
    path("lots/lowvol/<int:pk>", views.LotLowVolume.as_view(), name="lot-low-volume"),
    path("lots/inactivate/", views.LotInactivateList.as_view(), name="lot-inactivate-list"),
    path("lots/inactivate/<int:pk>", views.LotInactivate.as_view(), name="lot-inactivate"),

    path('patients/', views.AssayPatientView.as_view(), name='assayPatient'),
    path('patients/create/', views.AssayPatientCreate.as_view(), name='assayPatient-create'),
    path('patients/<int:pk>/', views.AssayPatientDetailView.as_view(), name='assayPatient-detail'),
    path('patients/<int:pk>/update/', views.AssayPatientUpdate.as_view(), name='assayPatient-update'),

    path('enzymes/', views.EnzymeView.as_view(), name='enzymes'),
    path('enzymes/create/', views.EnzymeCreate.as_view(), name='enzyme-create'),
    path('enzymes/<int:pk>/update/', views.EnzymeUpdate.as_view(), name='enzyme-update'),
]
