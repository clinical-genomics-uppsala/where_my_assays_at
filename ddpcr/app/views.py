from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import AssayType, AssayLOT, AssayPatient, Enzyme

from app.forms import AssayForm, LotScanForm, LotValidateForm, LotForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    context = {
        'num_assay': AssayType.objects.all().count(),
        'num_assay_order': AssayType.objects.filter(status=4).count() + AssayType.objects.filter(status=3).count(),
        'num_order': AssayLOT.objects.filter(status='Ordered').count(),
        'num_patient': AssayPatient.objects.all().count(),
        'num_scan': AssayLOT.objects.filter(status='Scanned').count(),
    }
    return render(request, 'app/index.html', context=context)

# List of objects
class BasicList(View):
    model = AssayLOT
    template = "app/lot_list.html"
    message = None
    redirect_url = "lots"

    def get(self, request, *args, **kwargs):
        objects = self.get_object_list()
        context = self.get_context_data(objects)
        if len(objects) == 0:
            messages.error(request, self.message)
            if self.redirect_url:
                return redirect(self.redirect_url)
        return render(request, self.template, context)

    def get_object_list(self):
        objects = self.model.objects.all()
        return objects

    def get_context_data(self, objects):
        return {"objects": objects}

# Template for form
class BasicForm(View):
    model = AssayLOT
    template = "app/lot_update.html"
    form = LotForm
    redirect_url = "lots"

    def get(self, request, pk, *args, **kwargs):
        context= {
            "form": self.get_instance_form(request, pk),
            "object": self.model.objects.get(pk=pk),
        }
        return render(request, self.template, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.get_instance_form(request, pk)
        if form.is_valid():
            obj = self.set_date(form.save(commit = False))
            messages.success(request, self.get_message(obj))
            return redirect(self.redirect_url)
        else:
            return self.get(request, pk)

    def get_instance_form(self, request, pk):
        return self.form(request.POST or None, instance = self.model.objects.get(pk=pk))

    def set_date(self, obj):
        obj.save()
        return obj

    def get_message(self, obj):
        return "%s / %s was updated." % (obj.assay, obj.lot)

### Assays ###

# List of assays
class AssayList(LoginRequiredMixin, BasicList):
    model = AssayType
    template = 'app/assay_list.html'
    redirect_url = None

# Update existing assay
class AssayUpdate(LoginRequiredMixin, BasicForm):
    model = AssayType
    template = "app/assay_update.html"
    form = AssayForm
    redirect_url = "assays"

    def get_message(self, obj):
        return "%s was updated." % (obj.assay_name)

# Add new assay
class AssayCreate(LoginRequiredMixin, CreateView):
    model = AssayType
    form_class = AssayForm
    template_name = "app/assay_create.html"
    success_url = reverse_lazy("assays")

### Lots ###

# Unrendered view for lot update
class AutoUpdateObjectView(View):
    model = AssayLOT
    redirect_url = "lots"

    def get(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        self.update_object(obj)
        messages.success(request, self.get_message(obj))
        return redirect(self.redirect_url)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    def update_object(self, obj):
        object.save()
        return

    def get_message(self, obj):
        return "%s was updated" % (obj)

# Overview over all lots
class LotList(LoginRequiredMixin, BasicList):
    model = AssayLOT
    message = "Could not find any lots in database."

# Edit and Update lot
class LotUpdate(LoginRequiredMixin, BasicForm):
    model = AssayLOT

# Order new lot from list of assay types
class LotOrderList(LoginRequiredMixin, BasicList):
    model = AssayType
    template = "app/lot_order_list.html"
    message = "Could not find any assays eligible for ordering."
    redirect_url = "assays"

    def get_object_list(self):
        objects = AssayType.objects.filter(status=4) | AssayType.objects.filter(status=3)
        return objects

# Create new lot with assay type and order date
class LotOrder(LoginRequiredMixin, AutoUpdateObjectView):
    model = AssayType
    redirect_url = "lot-order-list"

    def update_object(self, obj):
        AssayLOT.objects.create(assay=obj, date_order=timezone.now())
        return

    def get_message(self, obj):
        return "Order for %s was registered." % (obj)

# Register received order from list of ordered lots
class LotScanList(LoginRequiredMixin, BasicList):
    template = "app/lot_scan_list.html"
    message = "Could not find any ordered lots."

    def get_object_list(self):
        objects = [lot for lot in self.model.objects.all() if lot.status == "Ordered"]
        return objects

# Form for details on received lot
class LotScan(LoginRequiredMixin, BasicForm):
    form = LotScanForm
    template = "app/lot_scan.html"
 
    def set_date(self, obj):
        obj.date_scanned = timezone.now()
        obj.save()
        return obj

    def get_message(self, obj):
        return "%s/%s was marked as scanned." % (obj.assay, obj.lot)

# Registered validated lot from list of received lots
class LotValidateList(LoginRequiredMixin, BasicList):
    template = "app/lot_validate_list.html"
    message = "Could not find any scanned lots."

    def get_object_list(self):
        objects = [lot for lot in AssayLOT.objects.all() if lot.status == "Scanned"]
        return objects

# Form for details on validated lot
class LotValidate(LoginRequiredMixin, BasicForm):
    form = LotValidateForm
    template = "app/lot_validate.html"
 
    def set_date(self, obj):
        obj.date_validated = timezone.now()
        obj.save()
        return obj

    def get_message(self, obj):
        return "%s/%s was marked as validated." % (obj.assay, obj.lot)

# Activate lot from list of validated lots
class LotActivateList(LoginRequiredMixin, BasicList):
    template = 'app/lot_activate_list.html'
    message = "Could not find any validated lots."

    def get_object_list(self):
        objects = [lot for lot in AssayLOT.objects.all() if lot.status == 'Validated']
        return objects

# Activate lot
class LotActivate(LoginRequiredMixin, AutoUpdateObjectView):

    def update_object(self, obj):
        obj.date_activated = timezone.now()
        obj.save()
        return

    def get_message(self, obj):
        return (" %s-%s was activated." % (obj.assay, obj.lot))

# Mark lot with low volume from list of activated lots
class LotLowVolumeList(LoginRequiredMixin, BasicList):
    template = 'app/lot_low_volume_list.html'
    message = "Could not find any active lots with adequate volume."

    def get_object_list(self):
        objects = [lot for lot in AssayLOT.objects.all() if lot.status == 'Active']
        return objects

# Mark lot with low volume
class LotLowVolume(LoginRequiredMixin, AutoUpdateObjectView):

    def update_object(self, obj):
        obj.date_low_volume = timezone.now()
        obj.save()
        return

    def get_message(self, obj):
        return (" %s-%s was marked as low volume." % (obj.assay, obj.lot))

# Inactivate lot from list of activated lots
class LotInactivateList(LoginRequiredMixin, BasicList):
    template = 'app/lot_inactivate_list.html'
    message = "Could not find any active lots."

    def get_object_list(self):
        objects = [lot for lot in AssayLOT.objects.all() if lot.status == 'Active' or lot.status == 'Low Volume']
        return objects

# Inactivate lot
class LotInactivate(LoginRequiredMixin, AutoUpdateObjectView):

    def update_object(self, obj):
        obj.date_inactivated = timezone.now()
        obj.save()
        return

    def get_message(self, obj):
        return (" %s-%s was inactivated." % (obj.assay, obj.lot))

# Assay Patient

class AssayPatientView(LoginRequiredMixin, generic.ListView):
    model = AssayPatient

class AssayPatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = AssayPatient

class AssayPatientCreate(LoginRequiredMixin, CreateView):
    model = AssayPatient
    fields = '__all__' #not recommended should be explicit

class AssayPatientUpdate(LoginRequiredMixin, UpdateView):
    model = AssayPatient
    fields = '__all__' #not recommended should be explicit

class AssayPatientDelete(LoginRequiredMixin, DeleteView):
    model = AssayPatient
    success_url = reverse_lazy('assayPatient')

#Enzyme

class EnzymeView(LoginRequiredMixin, generic.ListView):
    model = Enzyme
    context_object_name='enzyme_list'
    queryset = Enzyme.objects.all()
    template_name = 'app/enzyme_list.html'

class EnzymeCreate(LoginRequiredMixin, CreateView):
    model = Enzyme
    fields = '__all__'
    success_url = reverse_lazy('enzyme')

class EnzymeUpdate(LoginRequiredMixin, UpdateView):
    model = Enzyme
    fields = '__all__' #not recommended should be explicit
    success_url = reverse_lazy('enzyme')
