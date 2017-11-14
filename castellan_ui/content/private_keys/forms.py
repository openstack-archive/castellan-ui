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

from castellan.common.objects import private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from castellan_ui.content import shared_forms


class ImportPrivateKey(shared_forms.ImportKey):

    def __init__(self, request, *args, **kwargs):
        super(ImportPrivateKey, self).__init__(
            request, *args, algorithms=shared_forms.KEY_PAIR_ALGORITHMS,
            **kwargs)
        self.fields['direct_input'].help_text = _(
            "PEM formatted private key.")
        self.fields['key_file'].help_text = _(
            "PEM formatted private key file.")

    def clean_key_data(self, key_data):
        key_obj = load_pem_private_key(
            key_data.encode('utf-8'), password=None, backend=default_backend())
        key_der = key_obj.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption())
        return base64.b64encode(key_der)

    def handle(self, request, data):
        return super(ImportPrivateKey, self).handle(
            request, data, private_key.PrivateKey)
