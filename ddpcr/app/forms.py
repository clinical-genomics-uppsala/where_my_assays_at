from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
import re
from searchableselect.widgets import SearchableSelect

from .models import AssayType, AssayLOT, AssayPatient

class AssayForm(ModelForm):

    class Meta:
        model = AssayType
        fields = [
            'assay_id',
            'assay_id_sec',
            'tube_id',
            'gene',
            'transcript',
            'cdna',
            'protein',
            'ref_build',
            'chromosome',
            'position_from',
            'position_to',
            'sequence',
            'enzymes',
            'temperature',
            'limit_of_detection',
            'status',
            'comment',
        ]
        widgets = {
            "sequence": forms.Textarea,
            "comment": forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(AssayForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = "Specify %s" % (k.capitalize().replace("_", " "))

    def clean(self):
        cleaned_data = super(AssayForm, self).clean()
        self.check_regex(cleaned_data)
        return cleaned_data

    def check_regex(self, data):
        regexs = {
            "transcript": {
                "regex": r"^NM_\d+\.*\d$",
                "message": "Enter valid Transcript id."
            },
            "cdna": {
                "regex": r"^c\.\d+[_,\-,+]*\d+[A,C,G,T,d,e,l,u,p,i,n,s]+>?[A,C,G,T,l,o,s]+$",
                "message": "Enter valid cDNA id."
            },
            "protein": {
                "regex": r"^p\..+",
                "message": "Enter valid Protein id.",
            },
            "sequence": {
                "regex": r"^[A,T,G,C]+\[[A,G,T,C,-]+\/[A,T,G,C,-]+\][G,T,C,A]+",
                "message": "Enter valid Sequence.",
            }
        }
        for k, v in regexs.items():
            target = data.get(k)
            if target and not re.match(v["regex"], target):
                self._errors[k] = self.error_class([
                    v["message"],
                ])

# Standard form for lots
class LotForm(ModelForm):

    class Meta:
        model = AssayLOT
        fields = [
            "assay",
            "lot",
            "project_id",
            "report_id",
            "fridge_id",
            "box_id",
            "box_position",
            "comment",
        ]
        widgets = {
            "comment": forms.Textarea
        }

    def __init__(self, *args, **kwargs):
        super(LotForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = "Specify %s" % (k.capitalize().replace("_", " "))

    def clean(self):
        cleaned_data = super(LotForm, self).clean()
        self.check_lot(cleaned_data)
        self.check_location(cleaned_data)
        return cleaned_data

    def check_lot(self, data):
        target = data.get("lot")
        if target and not re.match(r"^\d+$", target):
            self._errors["lot"] = self.error_class([
                "Enter valid lot id",
            ])

    def check_location(self, data):
        ids = [
            "fridge_id",
            "box_id",
            "box_position",
        ]
        values = [data.get(id) for id in ids]
        regexs = {
            "fridge_id": {
                "regex": "^K\d+$",
                "message": "Enter valid Fridge id."
            },
            "box_id": {
                "regex": "^\d+$",
                "message": "Enter valid Box id."
            },
            "box_position": {
                "regex": "^\D\d+$",
                "message": "Enter valid Box position."
            },
        }
        if any(values) and not all(values):
            for id in ids:
                self._errors[id] = self.error_class([
                    "A Location consists of Fridge id, Box id and Box position.",
                ])
        else:
            for k, v in regexs.items():
                target = data.get(k)
                if target and not re.match(v["regex"], target):
                    self._errors[k] = self.error_class([
                        v["message"],
                    ])

# Form to add received lot
class LotOrderForm(LotForm):

    class Meta:
        model = AssayLOT
        fields = [
            "project_id",
            "comment",
        ]
        widgets = {
            "comment": forms.Textarea
        }


# Form to add received lot
class LotScanForm(LotForm):

    class Meta:
        model = AssayLOT
        fields = [
            "lot",
            "fridge_id",
            "box_id",
            "box_position",
            "comment",
        ]
        widgets = {
            "comment": forms.Textarea
        }

# Form to specify report_id for validation
class LotValidateForm(LotForm):
    report_id = forms.CharField(
        required = True
    )

    class Meta:
        model = AssayLOT
        fields = [
            'report_id',
            'comment',
        ]
        widgets = {
            "comment": forms.Textarea
        }

# Standard form for patients
class PatientForm(ModelForm):
    class Meta:
        model = AssayPatient
        fields = [
            "study_id",
            "assay",
            "comment",
        ]
        widgets = {
            "assay": SearchableSelect(model='app.AssayType', search_field='assay_name', many=True),
            "comment": forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = "Specify %s" % (k.capitalize().replace("_", " "))

    def clean(self):
        cleaned_data = super(PatientForm, self).clean()
        self.check_study_id(cleaned_data)
        return cleaned_data

    def check_study_id(self, data):
        target = data.get("study_id")
        if target and not re.match(r"^[D,F,N,S]\d{3,4}$", target):
            self._errors["study_id"] = self.error_class([
                "Enter valid Study id.",
            ])
