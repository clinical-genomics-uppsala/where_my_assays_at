# from django.shortcuts import render
import datetime
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.conf import settings

from .models import AssayType, AssayLOT, AssayPatient, Enzyme

from app.forms import AssayLotForm, AssayTypeForm
#For login req views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    """ View function for home page """
    num_assay=AssayType.objects.all().count()
    num_patient=AssayPatient.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_assay': num_assay,
        'num_patient': num_patient,
        'num_visits': num_visits,
    }
    return render(request, 'app/index.html', context=context)

# Assay Type
class AssayTypeView(LoginRequiredMixin, generic.ListView):
    model = AssayType
    # paginate_by = 10
    context_object_name = 'assaytype_list'
    queryset = AssayType.objects.all() #filter(sequence__icontains='AA')[:5]
    template_name = 'app/assaytype_list.html'
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(AssayTypeView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context
    # def get_queryset(self):
    #     """ Return all Assays ids """
    #     return AssayType.objects.all()


class AssayTypeDetailView(LoginRequiredMixin,generic.DetailView):
    model = AssayType
    # paginate_by = 10
    # template_name = 'app/detail.html'
    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())
class AssayTypeCreate(LoginRequiredMixin, CreateView):
    model = AssayType
    # fields = '__all__' #not recommended should be explicit
    form_class = AssayTypeForm

class AssayTypeUpdate(LoginRequiredMixin, UpdateView):
    model = AssayType
    # fields = '__all__' #not recommended should be explicit
    form_class = AssayTypeForm

class AssayTypeDelete(LoginRequiredMixin, DeleteView):
    model = AssayType
    success_url = reverse_lazy('assayType')

# Assay lot

class AssayLotView(LoginRequiredMixin, generic.ListView):
    model = AssayLOT
    # paginate_by = 10
    context_object_name = 'assaylot_list'
    queryset = AssayLOT.objects.all() # Eller ska vi filtrera pa bara activated etc?
    template_name = 'app/assaylot_list.html'

class AssayLotDetailView(LoginRequiredMixin, generic.DetailView):
    model = AssayLOT

class AssayLotCreate(LoginRequiredMixin, CreateView):
    model = AssayLOT
    # form_class = AssayLotCreateForm
    fields = '__all__' #not recommended should be explicit

class AssayLotUpdate(LoginRequiredMixin, UpdateView):
    model = AssayLOT
    form_class = AssayLotForm
    # fields = '__all__' #not recommended should be explicit

class AssayLotDelete(LoginRequiredMixin, DeleteView):
    model = AssayLOT
    success_url = reverse_lazy('assaylot')

# Assay Patient
class AssayPatientView(LoginRequiredMixin, generic.ListView):
    model = AssayPatient
    # paginate_by = 10

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
