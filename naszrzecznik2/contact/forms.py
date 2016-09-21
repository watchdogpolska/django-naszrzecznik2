# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings

from .models import Contact


class ContactForm(forms.Form):
    sender = forms.EmailField(label=_("E-mail"), required=False)
    recipient = forms.ModelChoiceField(queryset=Contact.objects.all(),
                                       label=_("Recipient"))
    text = forms.CharField(widget=forms.Textarea(), label=_("Message"))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('action', "Send", css_class="btn-primary"))
        self.helper.form_action = reverse('contact:form')

    def get_message(self):
        return u"Sender: %s\nText: %s" % (self.cleaned_data['sender'],
                                          self.cleaned_data['text'])

    def save(self):
        send_mail(subject="Rzecznikowy e-mail",
                  message=self.get_message(),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[self.cleaned_data['recipient'].email])
