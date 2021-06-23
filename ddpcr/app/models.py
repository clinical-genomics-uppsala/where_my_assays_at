from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MaxValueValidator

from datetime import date
from django.urls import reverse

from django.db import models
from django.utils import timezone

# Create your models here.

class Enzyme(models.Model):
    """ Model representing enzymes in assays """
    name = models.CharField(max_length=10)

    def __str__(self):
        """ String for representing the Model objext. """
        return self.name

class AssayType(models.Model):
    """ Model representing assay type """
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
        CHRX = 23, _('Chromosome 23')
        CHRY = 24, _('Chromosome 24')
        CHRMT = 25, _('Chromosome 25')

    class Status(models.IntegerChoices):
        PENDING = 0, _('Pending')
        DESIGN_FAIL = 1, _('Design failed')
        RUN_FAIL = 2, _('Run failed')
        GRADIENT = 3, _('Gradient PCR')
        OK = 4, _('Ok')

    assay_name = models.CharField(max_length=100)
    assay_id = models.CharField(max_length=100)
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
    protein = models.CharField(max_length=100, default="Not applicable")
    enzymes = models.ManyToManyField(Enzyme, help_text='Select enzymes for this assay.')
    temperature = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    comment = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['chromosome','position_from']

    def __str__(self):
        return self.assay_name

    def statlab(self):
        """ Show status label not integer """
        return AssayType.Status(self.status).label

    def display_enzymes(self):
        """ Display enzymes for assay type """
        return ', '.join(enzyme.name for enzyme in self.enzymes.all()[:3])

    display_enzymes.short_description = 'Enzymes'

    #Add method that returns the url to access a particular instance on my model name?
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('assayType-detail', args=[str(self.id)])


class AssayLOT(models.Model): #Add validators for dates not to be out of order

    assay = models.ForeignKey(AssayType, on_delete=models.CASCADE)
    date_order = models.DateTimeField('date ordered', validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )]) #bara DateField?
    date_scanned = models.DateTimeField('date scanned',null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now() )]) #bara DateField?
    lot = models.CharField(max_length=10, unique=True)
    date_validated = models.DateTimeField('date validated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )]) #bara DateField?
    test_id = models.CharField(max_length=20,null=True, blank=True)
    date_activated = models.DateTimeField('date activated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )]) #bara DateField?
    volume_low = models.BooleanField(default=False)
    date_inactivated = models.DateTimeField('date inactivated', null=True, blank=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )]) #bara DateField?
    fridge_id = models.CharField(max_length=10, null=True, blank=True)
    box_id = models.CharField(max_length=20, null=True, blank=True)
    box_position = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['assay']
        permissions = (("can_update", "Update assay lot"),) # Vi borde ju kunna definera olika permissions, en read only, en edit och en delete. Dessa ar bara hittepa

    def __str__(self):
        return f'{self.lot}-{self.lot}'

    def status(self):
        if self.date_inactivated is not None:
            return 'Inactive'
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
    assay = models.ForeignKey(AssayType, on_delete=models.CASCADE)
    study_id = models.CharField(max_length=10)
    date_added = models.DateTimeField('date added', null=True, validators=[MaxValueValidator(limit_value=timezone.now, message=_('Make sure the date is not in the future. Todays date is %s') % timezone.now )]) #bara DateField?
    comment = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return "{0}_{1}".format(self.assay, self.study_id)

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('assayPatient-detail', args=[str(self.id)])
