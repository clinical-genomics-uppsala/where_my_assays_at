from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import io, json, math, re
import pandas as pd

from .models import AssayType, AssayLOT, AssayPatient, Enzyme

from app.forms import AssayForm, LotOrderForm, LotScanForm, LotValidateForm, LotForm, PatientForm

class Index(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        to_plot = {
            "entriesInDatabase": {
                "data": self.entriesInDatabase(),
                "colors": ["#0d6efd"],
            },
            "lotsPerAssay": {
                "data": self.lotsPerAssay(),
                "colors": ["#ffc107", "#fd7e14", "#0d6efd", "#198754", "#dc3545", "#6c757d"],
            },
            "assaysPerPatient": {
                "data": self.assaysPerPatient(),
                "colors": ["#0d6efd", "#6c757d"],
            }
        }
        plots = []
        for k, v in to_plot.items():
            plots.append(self.get_plot_data(
                k,
                v["data"]["x_title"],
                {},
                {},
                v["colors"],
                v["data"]["series"]
            ))
        context = {
            "plots": plots,
            }

        return render(request, 'app/index.html', context)

    def get_plot_data(self, plot_id, plot_x_title, plot_options, tooltip, colors, series):
        plot_data = {
            "plot_id": plot_id,
            "title": self.get_plot_title(plot_id),
            "x_title": plot_x_title,
            "y_title": self.get_plot_y_title(plot_id),
            "plot_options": plot_options,
            "tooltip": tooltip,
            "colors": colors,
            "series": series,
        }
        return plot_data

    def get_plot_title(self, plot_id):
        array = re.findall('[a-zA-Z][^A-Z]*', plot_id)
        return ' '.join(array).capitalize()

    def get_plot_y_title(self, plot_id):
        array = re.findall('[a-zA-Z][^A-Z]*', plot_id)
        return "Number of %s" % array[0]

    def assaysPerPatient(self):
        data = AssayPatient.objects.values('study_id').annotate(acount=Count('assay')).order_by()
        mean = AssayPatient.objects.values('study_id').annotate(acount=Count('assay')).aggregate(Avg('acount'))['acount__avg']
        return {
            "x_title": [ entry["study_id"] for entry in data ],
            "series": [
                {
                    "type": "column",
                    "name": "Assays per patient",
                    "data": [ entry["acount"] for entry in data ],
                },
                {
                    "type": "spline",
                    "name": "Average",
                    "marker": {
                        "enabled": False,
                    },
                    "data": [mean] * data.count(),
                },
            ]
        }

    def entriesInDatabase(self):
        return {
            "x_title": ["Assays", "Lots", "Patients"],
            "series": [
                {
                    "type": "bar",
                    "name": "Entries in Database",
                    "data": [
                        AssayType.objects.all().count(),
                        AssayLOT.objects.all().count(),
                        AssayPatient.objects.all().count(),
                    ],
                },
            ]
        }

    def lotsPerAssay(self):
        statCount = {
            "Ordered": [],
            "Scanned": [],
            "Validated": [],
            "Active": [],
            "Low Volume": [],
            "Inactive": [],
        }
        data = {
            "x_title": [],
            "series": [],
        }
        for entry in AssayType.objects.all():
            if AssayLOT.objects.filter(assay=entry.pk).count() > 1:
                data["x_title"].append(entry.assay_name)
                for k,v in statCount.items():
                    statCount[k].append(len([ lot for lot in AssayLOT.objects.filter(assay=entry.pk) if lot.status == k ]))
        for k,v in statCount.items():
            data["series"].append({
                "name": k,
                "type": "column",
                "data": v,
            })
        return data

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
            messages.info(request, self.message)
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
        context = {
            "form": self.get_instance_form(request, pk),
            "object": self.model.objects.get(pk=pk),
        }
        return render(request, self.template, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.get_instance_form(request, pk)
        if form.is_valid():
            obj = self.set_date(form.save(commit = False))
            form.save_m2m()
            messages.success(request, self.get_message(obj))
            if "Shortcut" in request.POST:
                return redirect("assay-update", obj.assay.pk)
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
    message = "Could not find any assays in database."
    redirect_url = None

    def get_context_data(self, objects):
        lots = {}
        for obj in objects:
            lots[obj.pk] = [lot for lot in AssayLOT.objects.filter(assay=obj) if lot.status != "Inactive"]
        patients = {}
        for obj in objects:
            patients[obj.pk] = AssayPatient.objects.filter(assay=obj)
        return {
            "objects": objects,
            "lots": lots,
            "patients": patients,
        }

# Update existing assay
class AssayUpdate(LoginRequiredMixin, BasicForm):
    model = AssayType
    template = "app/assay_update.html"
    form = AssayForm
    redirect_url = "assays"

    def get_message(self, obj):
        return "%s was updated." % (obj.assay_name)

# Add new assay
class AssayCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssayType
    form_class = AssayForm
    template_name = "app/assay_create.html"
    success_url = reverse_lazy("assays")
    success_message = "Assay successfully created."

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
    redirect_url = None

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
        objects = AssayType.objects.filter(status=3) | AssayType.objects.filter(status=0)
        return objects

# Create new lot with assay type and order date
class LotOrder(LoginRequiredMixin, View):
    model = AssayLOT
    template = "app/lot_order.html"
    form = LotOrderForm
    redirect_url = "lot-order-list"

    def get(self, request, pk, *args, **kwargs):
        context = {
            "form": self.form,
            "object": self.get_assay(pk),
        }
        return render(request, self.template, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            assay = self.get_assay(pk)
            project = form.cleaned_data.get("project_id")
            self.create_new_lot(assay, project)
            messages.success(request, self.get_message(assay))
            return redirect(self.redirect_url)
        else:
            return self.get(request, pk)

    def get_assay(self, pk):
        return AssayType.objects.get(pk=pk)

    def create_new_lot(self, obj, project):
        AssayLOT.objects.create(assay=obj, date_order=timezone.now(), project_id=project)
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

### Patients ###

# List of patients
class PatientList(LoginRequiredMixin, BasicList):
    model = AssayPatient
    template = 'app/patient_list.html'
    message = "Could not find any patients in database."
    redirect_url = None

# Update existing patient
class PatientUpdate(LoginRequiredMixin, BasicForm):
    model = AssayPatient
    template = "app/patient_update.html"
    form = PatientForm
    redirect_url = "patients"

    def get_message(self, obj):
        return "%s was updated." % (obj.study_id)

# Add new patient
class PatientCreate(LoginRequiredMixin, View):
    model = AssayPatient
    form = PatientForm
    template = "app/patient_create.html"
    redirect_url = "patients"

    def get(self, request, *args, **kwargs):
        context = {
            "form": self.form(request.POST or None),
        }
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_added = timezone.now()
            obj.save()
            form.save_m2m()
            messages.success(request, self.get_message(obj))
            return redirect(self.redirect_url)
        else:
            return self.get(request)

    def get_message(self, obj):
        return "Patient %s was added." % (obj)

# Add new patients from file
class PatientsCreate(LoginRequiredMixin, View):
    template = "app/patients_create.html"
    redirect_url = "patients"

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

    def post(self, request, *args, **kwargs):
        if "upload" in request.FILES:
            if not self.check_tsv_ext(request):
                return self.get(request)
            upload = self.get_tsv_data(request)
            if upload.empty:
                return self.get(request)
            else:
                self.add_tsv_data(request, upload)
                return redirect(self.redirect_url)
        else:
            messages.error(request, "No tsv file chosen for upload.")
            return self.get(request)

    def check_tsv_ext(self, request):
        if request.FILES["upload"].name.endswith(".tsv"):
            return True
        else:
            messages.error(request, "%s is not a tsv file." % request.FILES["upload"].name)
            return False

    def get_tsv_data(self, request):
        data = request.FILES["upload"].read().decode("UTF-8")
        upload = pd.read_table(io.StringIO(data))
        if not self.check_tsv_col(upload):
            messages.error(request, "%s does not contain required columns." % request.FILES["upload"].name)
            return pd.DataFrame()
        return upload

    def check_tsv_col(self, data):
        expected = ["study_id", "gene", "protein", "cdna", "comment"]
        return set(expected).issubset(data.columns)

    def add_tsv_data(self, request, data):
        for _, row in data.iterrows():
            if not AssayPatient.objects.filter(study_id=row["study_id"]).exists():
                if self.check_study_id(row["study_id"]):
                    patient, created = AssayPatient.objects.update_or_create(
                        study_id = row["study_id"],
                        date_added = timezone.now(),
                        comment = row["comment"],
                    )
                    messages.success(request, "%s was added." % row["study_id"])
                else:
                    messages.error(request, "%s is not a valid study_id." % row["study_id"])
                    break
            else:
                patient = AssayPatient.objects.get(study_id=row["study_id"])
            if self.check_assay(request, row):
                assay_id = AssayType.objects.get(
                    gene=row["gene"],
                    protein=row["protein"],
                    cdna=row["cdna"],
                )
                patient.assay.add(assay_id)
                messages.info(request, "Updating %s." % row["study_id"])
            else:
                break
        return

    def check_study_id(self, study_id):
        return re.match(r"^[D,F,N,S]\d{3,4}$", study_id)

    def check_assay(self, request, row):
        if AssayType.objects.filter(gene=row["gene"], protein=row["protein"], cdna=row["cdna"]).exists():
            return True
        else:
            messages.error(request, "Assay represented by %s %s %s does not exist in database." % (row["gene"], row["protein"], row["cdna"]))
            return False

# Add new assays from file
class AssaysCreate(PatientsCreate):
    template = "app/assays_create.html"
    redirect_url = "assays"

    def check_tsv_col(self, data):
        expected = [field.name for field in AssayType._meta.get_fields()]
        for entry in ["assaylot", "assaypatient", "id", "assay_name"]:
            expected.remove(entry)
        return set(expected).issubset(data.columns)

    def add_tsv_data(self, request, data):
        for _, row in data.iterrows():
            if not AssayType.objects.filter(gene=row["gene"], protein=row["protein"], cdna=row["cdna"]).exists():
                if self.check_columns(request, row):
                    assay, created = AssayType.objects.update_or_create(
                        assay_id = row["assay_id"],
                        assay_id_sec = row["assay_id_sec"],
                        tube_id = row["tube_id"],
                        gene = row["gene"],
                        sequence = row["sequence"],
                        ref_build = row["ref_build"],
                        chromosome = row["chromosome"],
                        position_from = row["position_from"],
                        position_to = row["position_to"],
                        transcript = row["transcript"],
                        cdna = row["cdna"],
                        protein = row["protein"],
                        temperature = row["temperature"],
                        limit_of_detection = row["limit_of_detection"],
                        status = row["status"],
                        comment = row["comment"],
                    )
                    for enzyme in row["enzymes"].split(","):
                        enzyme = Enzyme.objects.get(name=enzyme)
                        assay.enzymes.add(enzyme)
                    messages.success(request, "Assay represented by %s %s %s was added." % (row["gene"], row["protein"], row["cdna"]))
                else:
                    break
            else:
                messages.info(request, "Assay represented by %s %s %s already exists." % (row["gene"], row["protein"], row["cdna"]))
        return

    def check_columns(self, request, row):
        if type(row["gene"]) is float:
            messages.error(request, "Gene name is required.")
            return False
        elif type(row["sequence"]) is not float and not re.match(r"^[A,T,G,C]+\[[A,G,T,C,-]+\/[A,T,G,C,-]+\][G,T,C,A]+", row["sequence"]):
            messages.error(request, "%s is not a valid sequence." % row["sequence"])
            return False
        elif not re.match(r"^hg[1,3][8,9]", row["ref_build"]):
            messages.error(request, "%s is not a valid reference build format. Either hg19 or hg38." % row["ref_build"])
            return False
        elif not row["chromosome"] in list(range(1, 26)):
            messages.error(request, "%s is not a valid Chromosome. Any integer from 1 to 25." % row["chromosome"])
            return False
        elif not isinstance(row["position_from"], int) and not isinstance(row["position_to"], int):
            messages.error(request, "%s or %s is not a valid Position. Position has to be a positive integer." % (row["position_from"], row["position_to"]))
            return False
        elif not re.match(r"^NM_\d+\.*\d$", row["transcript"]):
            messages.error(request, "%s is not a valid transcript id." % row["transcript"])
            return False
        elif not re.match(r"^c\.[A,C,G,T]*\d+[-,+]*\d*[_,\-,+]*\d*[+]*\d*[A,C,G,T,d,e,l,u,p,i,n,s]+>?[A,C,G,T,l,o,s]*$", row["cdna"]):
            messages.error(request, "%s is not a valid cdna id." % row["cdna"])
            return False
        elif not re.match(r"^p\..+", row["protein"]):
            messages.error(request, "%s is not a valid protein id." % row["protein"])
            return False
        elif not isinstance(row["temperature"], int):
            messages.error(request, "%s is not a valid temperature." % row["temperature"])
            return False
        elif type(row["status"]) is float or not row["status"] in list(range(0, 4)):
            messages.error(request, "%s is not a valid status. 0 = Pending, 1 = Design failed, 2 = Run failed, 3 = Ok." % row["status"])
            return False
        else:
            for enzyme in row["enzymes"].split(","):
                if not Enzyme.objects.filter(name=enzyme).exists():
                    messages.error(request, "%s does not exist in database." % enzyme)
                    return False
        return True
