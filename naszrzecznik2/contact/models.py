from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class ContactQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Contact(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(verbose_name=_("Telephone"), blank=True, max_length=25)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    objects = ContactQuerySet.as_manager()

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['created', ]

    def __str__(self):
        return self.name
