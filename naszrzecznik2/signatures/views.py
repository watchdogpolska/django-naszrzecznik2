from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, RedirectView

from cached_property import cached_property

from .forms import SignatureForm
from .models import Petition, Signature


class HomeView(RedirectView):
    def get_redirect_url(self):
        return Petition.objects.latest().get_absolute_url()


class CategoryView(RedirectView):
    def get_redirect_url(self, category_slug):
        return (Petition.objects.
                filter(category__slug=category_slug).
                latest().get_absolute_url())


class SignatureListView(ListView):
    model = Signature
    paginate_by = 25

    def get_queryset(self):
        qs = super(SignatureListView, self).get_queryset()
        return qs.filter(petition=self.petition)

    @cached_property
    def petition(self):
        return get_object_or_404(Petition, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(SignatureListView, self).get_context_data(**kwargs)
        context['petition'] = self.petition
        context['form'] = SignatureForm(petition=self.petition)
        context['petitions'] = (Petition.objects.
                                filter(category=self.petition.category_id).
                                with_signature_count().all())
        return context


class PetitionDetailView(DetailView):
    model = Petition

    def get_context_data(self, **kwargs):
        context = super(PetitionDetailView, self).get_context_data(**kwargs)
        context['form'] = SignatureForm(petition=self.object)
        return context


class FormView(CreateView):
    model = Signature
    form_class = SignatureForm

    @cached_property
    def petition(self):
        return get_object_or_404(Petition, slug=self.kwargs['slug'], active=True)

    def get_form_kwargs(self, *args, **kwargs):
        kw = super(FormView, self).get_form_kwargs(*args, **kwargs)
        kw['petition'] = self.petition
        return kw

    def get_success_url(self):
        return reverse('signatures:thanks', kwargs={'slug': self.object.petition.slug})

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['object'] = self.petition
        return context


class ThanksView(DetailView):
    model = Petition
    template_name_suffix = "_thank"

    def get_context_data(self, **kwargs):
        context = super(ThanksView, self).get_context_data(**kwargs)
        return context
