from django.contrib import admin

from .models import AssayType, Enzyme, AssayLOT, AssayPatient

admin.site.register(Enzyme)

class AssayLOTInline(admin.StackedInline):
    model = AssayLOT
    extra = 0
    fields = [
        "lot",
        "fridge_id",
        "box_id",
        "box_position",
        "comment",
    ]

class AssayTypeAdmin(admin.ModelAdmin):
    list_display = (
        "assay_name",
        "assay_id",
        "assay_id_sec",
        "gene",
        "transcript",
        "cdna",
        "protein",
        "display_enzymes",
        "status",
    )
    fields = [
        "assay_id",
        "assay_id_sec",
        "tube_id",
        "gene",
        "transcript",
        "cdna",
        "protein",
        "ref_build",
        ("chromosome",
         "position_from",
         "position_to"),
        "sequence",
        "enzymes",
        "temperature",
        "limit_of_detection",
        "status",
        "comment",
    ]
    search_fields = ["assay_name"]
    list_filter = [
        "enzymes",
        "gene",
        "status"
    ]
    inlines=[AssayLOTInline]

admin.site.register(AssayType, AssayTypeAdmin)

class AssayLOTAdmin(admin.ModelAdmin):
    list_display = (
        "assay",
        "lot",
        "report_id",
        "fridge_id",
        "box_id",
        "box_position",
    )
    search_fields = [
        "assay__assay_name",
        "lot",
    ]

admin.site.register(AssayLOT, AssayLOTAdmin)

class AssayPatientAdmin(admin.ModelAdmin):
    list_display = (
        "study_id",
        "date_added",
    )
    search_fields = [
        "assay__assay_name",
        "study_id",
    ]
    list_filter=["date_added"]

admin.site.register(AssayPatient, AssayPatientAdmin)
