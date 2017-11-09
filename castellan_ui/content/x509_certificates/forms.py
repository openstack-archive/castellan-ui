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


import base64
from django.utils.translation import ugettext_lazy as _
import re

from castellan.common.objects import x_509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509 import load_pem_x509_certificate
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client

NAME_REGEX = re.compile(r"^\w+(?:[- ]\w+)*$", re.UNICODE)
ERROR_MESSAGES = {
    'invalid': _('Name may only contain letters, '
                 'numbers, underscores, spaces, and hyphens '
                 'and may not be white space.')}


class ImportX509Certificate(forms.SelfHandlingForm):
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Certificate Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)
    source_type = forms.ChoiceField(
        label=_('Source'),
        required=False,
        choices=[('file', _('Import File')),
                 ('raw', _('Direct Input'))],
        widget=forms.ThemableSelectWidget(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    cert_file = forms.FileField(
        label=_("Choose file"),
        widget=forms.FileInput(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-file': _('PEM Certificate File')}),
        required=False)
    direct_input = forms.CharField(
        label=_('PEM Certificate'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-raw': _('PEM Certificate')}),
        required=False)

    def clean(self):
        data = super(ImportX509Certificate, self).clean()

        # The cert can be missing based on particular upload
        # conditions. Code defensively for it here...
        cert_file = data.get('cert_file', None)
        cert_raw = data.get('direct_input', None)

        if cert_raw and cert_file:
            raise forms.ValidationError(
                _("Cannot specify both file and direct input."))
        if not cert_raw and not cert_file:
            raise forms.ValidationError(
                _("No input was provided for the certificate value."))
        try:
            if cert_file:
                cert_pem = self.files['cert_file'].read()
            else:
                cert_pem = str(data['direct_input'])
            cert_obj = load_pem_x509_certificate(
                cert_pem.encode('utf-8'), default_backend())
            cert_der = cert_obj.public_bytes(Encoding.DER)
        except Exception as e:
            msg = _('There was a problem loading the certificate: %s. '
                    'Is the certificate valid and in PEM format?') % e
            raise forms.ValidationError(msg)

        data['cert_data'] = base64.b64encode(cert_der).decode('utf-8')

        return data

    def handle(self, request, data):
        try:
            cert_pem = data.get('cert_data')
            cert_uuid = client.import_object(
                request,
                data=cert_pem,
                name=data['name'],
                object_type=x_509.X509)

            if data['name']:
                identifier = data['name']
            else:
                identifier = cert_uuid
            messages.success(request,
                             _('Successfully imported certificate: %s')
                             % identifier)
            return cert_uuid
        except Exception as e:
            msg = _('Unable to import certificate: %s')
            messages.error(request, msg % e)
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import certificate.'))
            return False
