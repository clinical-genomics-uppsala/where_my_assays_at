from datetime import datetime
from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# class UpdateStatusAssayLotForm(forms.Form):
#     update_date_scanned = forms.DateField(help_text="Enter date when lot scanned (must be after Date Ordered and not in the future).")
#     # new_status = forms.
#     def clean_update_date_scanned(self):
#         data = self.cleaned_data['update_date_scanned']
#
#         # Check date is not in future
#         if data > datetime.date.today():
#             raise ValidationError(_('Invalid date - date in future'))
#
#         # Check date is not before Ordered datetime
#         # if data < date_order :
#         #     raise ValidationError(_('Invalid date - date before Date Ordered'))
#
#         return data

from django.forms import ModelForm
from .models import AssayType, AssayLOT

class AssayTypeForm(ModelForm):
    class Meta:
        model = AssayType
        fields = ['assay_name', 'assay_id', 'assay_id_sec', 'tube_id', 'gene', 'sequence', 'ref_build', 'chromosome', 'position_from', 'position_to', 'transcript', 'cdna', 'protein', 'enzymes','temperature','status','comment']
        widgets = {
            'assay_name': forms.TextInput(attrs={'placeholder': _('Gene_Protein_cDNA')}),
        }

class AssayLotForm(ModelForm):
    # Status field should be dependent on if there is a value for the corresponding date. How?
    #Should we start with just ValidationError if there is a date and not the corresponding status?
    class Meta:
        model = AssayLOT
        fields = ['assay','date_order','date_scanned','lot','date_validated','test_id','date_activated','volume_low','date_inactivated','fridge_id', 'box_id', 'box_position','comment']

    def clean(self):
        cleaned_data = super(AssayLotForm, self).clean()
        date_ordered = cleaned_data.get("date_order")
        date_scanned = cleaned_data.get("date_scanned")
        date_validated = cleaned_data.get("date_validated")
        test_id = cleaned_data.get("test_id")
        date_activated = cleaned_data.get("date_activated")
        date_inactivated = cleaned_data.get("date_inactivated")

        #date_order earlier than all other dates
        if date_ordered and date_scanned:
            if date_scanned < date_ordered:
                raise forms.ValidationError("Date scanned cannot be earlier than date ordered!")

        if date_ordered and date_validated:
            if date_validated < date_ordered:
                raise forms.ValidationError("Date validated cannot be earlier than date ordered!")

        if date_ordered and date_activated:
            if date_activated < date_ordered:
                raise forms.ValidationError("Date activated cannot be earlier than date ordered!")

        if date_ordered and date_inactivated:
            if date_inactivated < date_ordered:
                raise forms.ValidationError("Date inactivated cannot be earlier than date ordered!")

        #date_scanned ealier then date_validated, activated, inactivated
        if date_scanned and date_validated:
            if not test_id: #should also be id Status is either validated, activated, or inactivated(?).
                raise forms.ValidationError("You need a Test ID to validate the lot!")
            if date_validated < date_scanned:
                raise forms.ValidationError("Date validated cannot be earlier than date scanned!")

        if date_scanned and date_activated:
            if date_activated < date_scanned:
                raise forms.ValidationError("Date activated cannot be earlier than date scanned!")

        if date_scanned and date_inactivated:
            if date_inactivated < date_scanned:
                raise forms.ValidationError("Date inactivated cannot be earlier than date scanned!")

        # date_validated need date_scanned and less than activated, inactivated
        if date_validated and not date_scanned:
            raise forms.ValidationError("Date validated cannot be set without a date scanned!")

        if date_validated and date_activated:
            if date_activated < date_validated:
                raise forms.ValidationError("Date activated cannot be earlier than date validated!")

        if date_validated and date_inactivated:
            if date_inactivated < date_validated:
                raise forms.ValidationError("Date inactivated cannot be earlier than date validated!")

        # date_activated need date_validated and less than inactivated
        if date_activated and not date_validated:
            raise forms.ValidationError("Date activated cannot be set without a date validated!")

        if date_activated and date_inactivated:
            if date_inactivated < date_activated:
                raise forms.ValidationError("Date inactivated cannot be earlier than date activated!")
        # date_inactivated
        if date_inactivated and not date_activated:
            raise forms.ValidationError("Cannot have a Inactivation date without a Activation date!")

        return cleaned_data
    # def clean_date_scanned(self):
    #     data = self.cleaned_data['date_scanned']
    #     # Check date is not in future
    #     if data > timezone.now():
    #         raise ValidationError(_('Invalid date - date in future'))


    # some normal ModelForm setup goes here
    # def clean(self):
    #     cleaned_data = super(PriceOptionForm, self).clean()
    #     from_time = cleaned_data.get("from_time")
    #     end_time = cleaned_data.get("end_time")
    #
    #     if from_time and end_time:
    #         if end_time < from_time:
    #             raise forms.ValidationError("End time cannot be earlier than start time!")
    #     return cleaned_data
