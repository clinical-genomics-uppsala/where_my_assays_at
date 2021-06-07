from django.contrib import admin

from .models import AssayType, Enzyme, AssayLOT, AssayPatient

# Register your models here.

# admin.site.register([
#     AssayType,
#     Enzyme,
#     AssayLOT,
#     AssayPatient
# ])

# class EnzymeAdmin(admin.ModelAdmin):
#     pass
admin.site.register(Enzyme) #, EnzymeAdmin)

class AssayLOTInline(admin.StackedInline):
    model = AssayLOT
    extra = 0
    fields = ['lot','status','date_order','date_scanned','freezer_id','box_position','comment']

class AssayTypeAdmin(admin.ModelAdmin):
    list_display = ('assay_id', 'assay_id_sec', 'gene', 'display_enzymes','transcript', 'status')
    fields = ['assay_id', 'assay_id_sec','gene','sequence','ref_build',
                ('chromosome','position_from','position_to'),'transcript','cdna','protein',
                'enzyme','temperature','status','comment']
    search_fields = ['assay_id', 'gene']
    list_filter = ['enzyme', 'gene', 'status']
    inlines=[AssayLOTInline,]

admin.site.register(AssayType, AssayTypeAdmin)

class AssayLOTAdmin(admin.ModelAdmin):
    list_display = ('assay', 'lot', 'status','freezer_id', 'box_position','volume_low')
    search_fields = ['assay']
    list_filter=['status','volume_low']
    # inlines=[AssayPatient]

admin.site.register(AssayLOT, AssayLOTAdmin)

class AssayPatientAdmin(admin.ModelAdmin):
    list_display = ('assay','study_id','date_added')
    search_fields = ['assay']
    list_filter=['date_added']

admin.site.register(AssayPatient, AssayPatientAdmin)
