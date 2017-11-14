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

from castellan.common.objects import public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client
from castellan_ui.content import shared_forms

ALGORITHMS = ('RSA', 'DSA')


class ImportPublicKey(shared_forms.ImportKey):

    def __init__(self, request, *args, **kwargs):
        super(ImportPublicKey, self).__init__(
            request, *args, algorithms=ALGORITHMS, **kwargs)

    def clean_key_data(self, key_data):
        key_obj = load_pem_public_key(
            key_data.encode('utf-8'), backend=default_backend())
        key_der = key_obj.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return base64.b64encode(key_der)

    def handle(self, request, data):
        return super(ImportPublicKey, self).handle(
            request, data, public_key.PublicKey)


class GenerateKeyPair(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                widget=shared_forms.ListTextWidget(
                                    data_list=ALGORITHMS,
                                    name='algorithm-list'))
    length = forms.IntegerField(label=_("Bit Length"))
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=shared_forms.NAME_REGEX,
                            error_messages=shared_forms.ERROR_MESSAGES)

    def handle(self, request, data):
        try:
            key_uuid = client.generate_key_pair(
                request,
                algorithm=data['algorithm'],
                length=data['length'],
                name=data['name'])

            if data['name']:
                key_identifier = data['name']
            else:
                key_identifier = key_uuid
            messages.success(request,
                             _('Successfully generated key pair with UUIDs %s')
                             % key_identifier)
            return key_uuid
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to generate public key.'))
            return False
