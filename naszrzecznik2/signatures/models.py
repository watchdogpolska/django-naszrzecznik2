from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from model_utils.models import TimeStampedModel


class CategoryQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Category(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    ordering = models.SmallIntegerField(verbose_name=("Ordering"))
    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['created', ]
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('signatures:category', kwargs={'category_slug': self.slug})


class PetitionQuerySet(models.QuerySet):
    def with_signature_count(self):
        return self.annotate(signature_count=models.Count('signature'))


@python_2_unicode_compatible
class Petition(TimeStampedModel):
    category = models.ForeignKey(Category, verbose_name=_("Category"))
    slug = AutoSlugField(populate_from='title', verbose_name=_("Slug"), unique=True)
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_("Text"))
    thank_you = models.TextField(verbose_name=_("Thank you text"))
    side_text = models.TextField(verbose_name=_("Side text"))
    organization_name_use = models.BooleanField(verbose_name=_("Use organization name field?"))
    first_name_use = models.BooleanField(verbose_name=_("Use first name field?"))
    second_name_use = models.BooleanField(verbose_name=_("Use second name field?"))
    place_use = models.BooleanField(verbose_name=_("Use place field?"))
    email_use = models.BooleanField(verbose_name=_("Use email field?"))
    active = models.BooleanField(verbose_name=_("Active status"))
    privacy_text = models.TextField(verbose_name=_("Privacy aggrement"), blank=True)
    newsletter_text = models.TextField(verbose_name=_("Newsletter aggrement"), blank=True)
    objects = PetitionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Petition")
        verbose_name_plural = _("Petitions")
        ordering = ['created', ]
        get_latest_by = 'created'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('signatures:text', kwargs={'slug': self.slug})


class SignatureQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Signature(TimeStampedModel):
    petition = models.ForeignKey(to=Petition, verbose_name=_("Petition"))
    # Text fields
    organization_name = models.CharField(max_length=100, verbose_name=_("Organization"), blank=True)
    first_name = models.CharField(max_length=100, verbose_name=_('First name'), blank=True)
    second_name = models.CharField(max_length=100, verbose_name=_('Second name'), blank=True)
    place = models.CharField(max_length=100, verbose_name=_("Place"), blank=True)
    email = models.EmailField(verbose_name=_("E-mail"), blank=True)
    # Checkbox fields
    privacy = models.BooleanField(verbose_name=_("Privacy acceptation"), default=False)
    newsletter = models.BooleanField(verbose_name=_("Newsletter acceptation"), default=False)
    # Location fields
    lat = models.FloatField(null=True, blank=True, verbose_name=_("Latitude"))
    lng = models.FloatField(null=True, blank=True, verbose_name=_("Longitude"))
    # Status field
    visible = models.BooleanField(default=True, verbose_name=_("Visible"))

    objects = SignatureQuerySet.as_manager()

    class Meta:
        verbose_name = _("Signature")
        verbose_name_plural = _("Signatures")
        ordering = ['created', ]
        get_latest_by = 'created'

    def __str__(self):
        return self.organization_name or "%s %s" % (self.first_name, self.second_name)
