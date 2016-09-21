from django.views.generic import FormView, TemplateView

from .forms import ContactForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/form.html"

    def form_valid(self, form):
        form.save()
        return redirect(reverse('contact:success'))


class SuccessView(TemplateView):
    template_name = "contact/success.html"
