from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Signature


class SignatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.petition = kwargs.pop('petition')
        super(SignatureForm, self).__init__(*args, **kwargs)
        for field in ['organization_name', 'first_name', 'second_name', 'place', 'email']:
            if getattr(self.petition, field + "_use"):
                self.fields[field].required = True
            else:
                del self.fields[field]

        if self.petition.privacy_text:
            self.fields['privacy'].label = self.petition.privacy_text
            self.fields['privacy'].required = True
        else:
            del self.fields['privacy']

        if self.petition.newsletter_text:
            self.fields['newsletter'].label = self.petition.newsletter_text
            self.fields['newsletter'].required = False

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('action', "Sign", css_class="btn-warning"))
        self.helper.form_action = reverse('signatures:form',
                                          kwargs={'slug': self.petition.slug})

    def save(self, *args, **kwargs):
        self.instance.petition = self.petition
        return super(SignatureForm, self).save(*args, **kwargs)

    class Meta:
        model = Signature
        fields = ('organization_name', 'first_name', 'second_name', 'place', 'email',
                  'privacy', 'newsletter')
