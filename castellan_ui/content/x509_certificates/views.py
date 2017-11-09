#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

import binascii
from castellan.common.objects import x_509
from castellan_ui.api import client
from castellan_ui.content.x509_certificates import forms as x509_forms
from castellan_ui.content.x509_certificates import tables
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509 import load_der_x509_certificate

from datetime import datetime
from horizon import exceptions
from horizon import forms
from horizon.tables import views as tables_views
from horizon.utils import memoized
from horizon import views


def download_cert(request, object_id):
    try:
        obj = client.get(request, object_id)
        der_data = obj.get_encoded()
        cert_obj = load_der_x509_certificate(der_data, default_backend())
        data = cert_obj.public_bytes(Encoding.PEM)
        response = HttpResponse()
        response.write(data)
        response['Content-Disposition'] = ('attachment; '
                                           'filename="%s.pem"' % object_id)
        response['Content-Length'] = str(len(response.content))
        return response

    except Exception:
        redirect = reverse('horizon:project:x509_certificates:index')
        msg = _('Unable to download x509_certificate "%s".')\
            % (object_id)
        exceptions.handle(request, msg, redirect=redirect)


class IndexView(tables_views.MultiTableView):
    table_classes = [
        tables.X509CertificateTable
    ]
    template_name = 'x509_certificates.html'

    def get_x509_certificate_data(self):
        try:
            return client.list(self.request, object_type=x_509.X509)
        except Exception as e:
            msg = _('Unable to list certificates: "%s".') % (e.message)
            exceptions.handle(self.request, msg)
            return []


class ImportView(forms.ModalFormView):
    form_class = x509_forms.ImportX509Certificate
    template_name = 'x509_certificate_import.html'
    submit_url = reverse_lazy(
        "horizon:project:x509_certificates:import")
    success_url = reverse_lazy('horizon:project:x509_certificates:index')
    submit_label = page_title = _("Import X.509 Certificate")

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def get_object_id(self, key_uuid):
        return key_uuid


class DetailView(views.HorizonTemplateView):
    template_name = 'x509_certificate_detail.html'
    page_title = _("X.509 Certificate Details")

    @memoized.memoized_method
    def _get_data(self):
        try:
            obj = client.get(self.request, self.kwargs['object_id'])
        except Exception:
            redirect = reverse('horizon:project:x509_certificates:index')
            msg = _('Unable to retrieve details for x509_certificate "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return obj

    @memoized.memoized_method
    def _get_data_created_date(self, obj):
        try:
            created_date = datetime.utcfromtimestamp(obj.created).isoformat()
        except Exception:
            redirect = reverse('horizon:project:x509_certificates:index')
            msg = _('Unable to retrieve details for x509_certificate "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return created_date

    @memoized.memoized_method
    def _get_crypto_obj(self, obj):
        der_data = obj.get_encoded()
        return load_der_x509_certificate(der_data, default_backend())

    @memoized.memoized_method
    def _get_certificate_version(self, obj):
        return self._get_crypto_obj(obj).version

    @memoized.memoized_method
    def _get_certificate_fingerprint(self, obj):
        return binascii.hexlify(
            self._get_crypto_obj(obj).fingerprint(hashes.SHA256()))

    @memoized.memoized_method
    def _get_serial_number(self, obj):
        return self._get_crypto_obj(obj).serial_number

    @memoized.memoized_method
    def _get_validity_start(self, obj):
        return self._get_crypto_obj(obj).not_valid_before

    @memoized.memoized_method
    def _get_validity_end(self, obj):
        return self._get_crypto_obj(obj).not_valid_after

    @memoized.memoized_method
    def _get_issuer(self, obj):
        result = ""
        issuer = self._get_crypto_obj(obj).issuer
        for attribute in issuer:
            result = (result + str(attribute.oid._name) + "=" +
                      str(attribute.value) + ",")
        return result[:-1]

    @memoized.memoized_method
    def _get_subject(self, obj):
        result = ""
        issuer = self._get_crypto_obj(obj).subject
        for attribute in issuer:
            result = (result + str(attribute.oid._name) + "=" +
                      str(attribute.value) + ",")
        return result[:-1]

    @memoized.memoized_method
    def _get_data_bytes(self, obj):
        try:
            data = self._get_crypto_obj(obj).public_bytes(Encoding.PEM)
        except Exception:
            redirect = reverse('horizon:project:x509_certificates:index')
            msg = _('Unable to retrieve details for x509_certificate "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return data

    def get_context_data(self, **kwargs):
        """Gets the context data for key."""
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self._get_data()
        context['object'] = obj
        context['object_created_date'] = self._get_data_created_date(obj)
        context['object_bytes'] = self._get_data_bytes(obj)
        context['cert_version'] = self._get_certificate_version(obj)
        context['cert_fingerprint'] = self._get_certificate_fingerprint(obj)
        context['cert_serial_number'] = self._get_serial_number(obj)
        context['cert_validity_start'] = self._get_validity_start(obj)
        context['cert_validity_end'] = self._get_validity_end(obj)
        context['cert_issuer'] = self._get_issuer(obj)
        context['cert_subject'] = self._get_subject(obj)
        return context
