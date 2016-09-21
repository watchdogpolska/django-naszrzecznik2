from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from .forms import ContactForm
from .models import Contact


class ContactObjectMixin(object):
    def setUp(self):
        self.contact = Contact.objects.create(name="Jobs",
                                              email="jobs@example.com")


class ContactFormTestCase(ContactObjectMixin, TestCase):

    def test_send_message(self):
        form = ContactForm(data={'sender': 'steve@example.com',
                                 'recipient': self.contact.pk,
                                 'text': "Lorem ipsum"})
        self.assertTrue(form.is_valid(), msg=form.errors)
        form.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("jobs@example.com", mail.outbox[0].to)
        self.assertIn("Lorem ipsum", mail.outbox[0].body)
        self.assertIn('steve@example.com', mail.outbox[0].body)


class ContactViewTestCase(ContactObjectMixin, TestCase):
    def get_url(self):
        return reverse('contact:form')

    def test_render_form(self):
        response = self.client.get(self.get_url())
        self.assertContains(response, "Jobs")

    def test_send_message(self):
        response = self.client.post(path=self.get_url(),
                                    data={'email': 'steve@example.com',
                                          'recipient': self.contact.pk,
                                          'text': "Lorem ipsum"})
        self.assertEqual(response.status_code, 302)


class SuccessViewTestCase(TestCase):
    def get_url(self):
        return reverse('contact:success')

    def test_render(self):
        self.client.get(self.get_url())
