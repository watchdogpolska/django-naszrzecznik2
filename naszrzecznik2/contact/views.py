from django.views.generic import FormView, TemplateView

from .forms import ContactForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import Contact


class ContactListMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ContactListMixin, self).get_context_data(**kwargs)
        context['contact_list'] = Contact.objects.all()
        return context


class ContactView(ContactListMixin, FormView):
    form_class = ContactForm
    template_name = "contact/form.html"

    def form_valid(self, form):
        form.save()
        return redirect(reverse('contact:success'))


class SuccessView(ContactListMixin, TemplateView):
    template_name = "contact/success.html"
