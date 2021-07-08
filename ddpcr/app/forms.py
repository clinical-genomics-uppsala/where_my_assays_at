from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from .models import AssayType, AssayLOT

class AssayForm(ModelForm):

    class Meta:
        model = AssayType
        fields = ['assay_name',
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
                  'status',
                  'comment']
        widgets = {
            "comment": forms.Textarea
        }

    def __init__(self, *args, **kwargs):
        super(AssayForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = "Specify %s" % (k.capitalize().replace("_", " "))

# Standard form for lots
class LotForm(ModelForm):

    class Meta:
        model = AssayLOT
        fields = [
            "assay",
            "lot",
            "test_id",
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
        self.check_location(cleaned_data)
        return cleaned_data

    def check_location(self, data):
        ids = [
            "fridge_id",
            "box_id",
            "box_position",
        ]
        values = [data.get(id) for id in ids]
        if any(values) and not all(values):
            for id in ids:
                self._errors[id] = self.error_class([
                    "A Location consists of Fridge id, Box id and Box position.",
                ])

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

# Form to specify test_id for validation
class LotValidateForm(LotForm):
    test_id = forms.CharField(
        required = True
    )

    class Meta:
        model = AssayLOT
        fields = [
            'test_id',
            'comment',
        ]
        widgets = {
            "comment": forms.Textarea
        }
