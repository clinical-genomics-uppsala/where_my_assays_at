from django.contrib import admin

from .models import AssayType, Enzyme, AssayLOT, AssayPatient

# Register your models here.

admin.site.register([
    AssayType,
    Enzyme,
    AssayLOT,
    AssayPatient
])
