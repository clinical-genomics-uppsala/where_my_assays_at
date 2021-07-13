from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from computed_property import ComputedTextField
from datetime import date

class Enzyme(models.Model):
    """ Model representing enzymes in assay type """

    # Absolute properties
    name = models.CharField(max_length=10)

    # Functions
    def __str__(self):
        """ Give string representation of enzyme """
        return self.name

class AssayType(models.Model):
    """ Model representing assay type """

    # Choices
    class GenomeBuildVersion(models.TextChoices):
        HG38 = 'hg38', _('GRCh38')
        HG19 = 'hg19', _('GRCh37')

    class Chromosomes(models.IntegerChoices):
        CHR1 = 1, _('Chromosome 1')
        CHR2 = 2, _('Chromosome 2')
        CHR3 = 3, _('Chromosome 3')
        CHR4 = 4, _('Chromosome 4')
        CHR5 = 5, _('Chromosome 5')
        CHR6 = 6, _('Chromosome 6')
        CHR7 = 7, _('Chromosome 7')
        CHR8 = 8, _('Chromosome 8')
        CHR9 = 9, _('Chromosome 9')
        CHR10 = 10, _('Chromosome 10')
        CHR11 = 11, _('Chromosome 11')
        CHR12 = 12, _('Chromosome 12')
        CHR13 = 13, _('Chromosome 13')
        CHR14 = 14, _('Chromosome 14')
        CHR15 = 15, _('Chromosome 15')
        CHR16 = 16, _('Chromosome 16')
        CHR17 = 17, _('Chromosome 17')
        CHR18 = 18, _('Chromosome 18')
        CHR19 = 19, _('Chromosome 19')
        CHR20 = 20, _('Chromosome 20')
        CHR21 = 21, _('Chromosome 21')
        CHR22 = 22, _('Chromosome 22')
        CHRX = 23, _('Chromosome X')
        CHRY = 24, _('Chromosome Y')
        CHRMT = 25, _('Chromosome MT')

    class Status(models.IntegerChoices):
        PENDING = 0, _('Pending')
        DESIGN_FAIL = 1, _('Design failed')
        RUN_FAIL = 2, _('Run failed')
        OK = 3, _('Ok')

    # Absolute properties
    assay_id = models.CharField(max_length=100, null=True, blank=True)
    assay_id_sec = models.CharField(max_length=100, null=True, blank=True)
    tube_id = models.CharField(max_length=100, null=True, blank=True)
    gene = models.CharField(max_length=100)
    sequence = models.CharField(max_length=500, null=True, blank=True)
    ref_build = models.CharField(
        max_length=4,
        choices=GenomeBuildVersion.choices,
        default=GenomeBuildVersion.HG38
    )
    chromosome = models.IntegerField(
        choices=Chromosomes.choices,
        default=Chromosomes.CHR1
    )
    position_from = models.PositiveIntegerField(default=0)
    position_to = models.PositiveIntegerField(default=1)
    transcript = models.CharField(max_length=100)
    cdna = models.CharField(max_length=100)
    protein = models.CharField(max_length=100, default="p.?")
    enzymes = models.ManyToManyField(Enzyme)
    temperature = models.PositiveIntegerField(null=True, blank=True)
    limit_of_detection = models.FloatField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    comment = models.CharField(max_length=500, null=True, blank=True)

    # Computed properties
    assay_name = ComputedTextField(compute_from='get_assay_name')

    class Meta:
        ordering = ['-status','assay_name']

    # Functions
    def __str__(self):
        """ Give string representation of assay type """
        return self.assay_name

    @property
    def get_assay_name(self):
        if self.protein != "p.?":
            return "%s_%s" % (self.gene, self.protein.replace("p.", "", 1))
        else:
            return "%s_%s" % (self.gene, self.cdna)

    def statlab(self):
        """ Show status label not integer """
        return AssayType.Status(self.status).label

    def display_enzymes(self):
        """ Display enzymes for assay type """
        return ', '.join(enzyme.name for enzyme in self.enzymes.all())

    display_enzymes.short_description = 'Enzymes'

    #Add method that returns the url to access a particular instance on my model name?
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('assayType-detail', args=[str(self.id)])


class AssayLOT(models.Model):

    # Linked properties
    assay = models.ForeignKey(AssayType, on_delete=models.CASCADE)

    # Absolute properties
    project_id = models.CharField(default="CGU201813", max_length=20)
    lot = models.CharField(max_length=10, unique=True)
    report_id = models.CharField(max_length=20, null=True, blank=True)
    fridge_id = models.CharField(max_length=10, null=True, blank=True)
    box_id = models.CharField(max_length=20, null=True, blank=True)
    box_position = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)

    date_order = models.DateTimeField('date ordered', validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )])
    date_scanned = models.DateTimeField('date scanned',null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now() )])
    date_validated = models.DateTimeField('date validated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )])
    date_activated = models.DateTimeField('date activated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )])
    date_low_volume = models.DateTimeField('date low volume', null=True, blank=True)
    date_inactivated = models.DateTimeField('date inactivated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )])

    # Computed properties
    status = ComputedTextField(compute_from='get_status')

    class Meta:
        ordering = ['assay', 'status']
        permissions = (("can_update", "Update assay lot"),)

    def __str__(self):
        return f'{self.lot}-{self.lot}'

    @property
    def get_status(self):
        if self.date_inactivated is not None:
            return 'Inactive'
        elif self.date_low_volume is not None:
            return 'Low Volume'
        elif self.date_activated is not None:
            return 'Active'
        elif self.date_validated is not None:
            return 'Validated'
        elif self.date_scanned is not None:
            return 'Scanned'
        elif self.date_order is not None:
            return 'Ordered'
        else:
            return None

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('assayLot-detail', args=[str(self.id)])


class AssayPatient(models.Model):

    # Absolute properties
    study_id = models.CharField(max_length=10, unique=True)
    assay = models.ManyToManyField(AssayType)
    date_added = models.DateTimeField('date added', null=True)
    comment = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['study_id']

    def __str__(self):
        return "{0}_{1}".format(self.assay, self.study_id)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('assayPatient-detail', args=[str(self.id)])
