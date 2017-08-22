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
import binascii
from django.utils.translation import ugettext_lazy as _

from castellan.common.objects import symmetric_key
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client
from castellan_ui.content import shared_forms

ALGORITHMS = ('AES', 'DES', 'DESEDE')

ALG_HELP_TEXT = _(
    "Check which algorithms your key manager supports. "
    "Some common algorithms are: %s") % ', '.join(ALGORITHMS)
LENGTH_HELP_TEXT = _(
    "Only certain bit lengths are valid for each algorithm. "
    "Some common bit lengths are: 128, 256")


class ImportSymmetricKey(shared_forms.ImportKey):

    def __init__(self, request, *args, **kwargs):
        super(ImportSymmetricKey, self).__init__(
            request, *args, algorithms=ALGORITHMS, **kwargs)
        self.fields['direct_input'].help_text = _(
            "Key bytes represented as hex characters. Acceptable values are "
            "0-9, a-f, A-F")
        self.fields['key_file'].help_text = _(
            "The file should contain the raw bytes of the key.")

    def clean_key_data(self, key_data):
        if self.files.get('key_file'):
            key_bytes = key_data
        else:
            key_bytes = binascii.unhexlify(key_data)
        b64_key_data = base64.b64encode(key_bytes)

        return b64_key_data

    def handle(self, request, data):
        return super(ImportSymmetricKey, self).handle(
            request, data, symmetric_key.SymmetricKey)


class GenerateSymmetricKey(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                widget=shared_forms.ListTextWidget(
                                    data_list=ALGORITHMS,
                                    name='algorithm-list'),
                                help_text=ALG_HELP_TEXT)
    length = forms.IntegerField(label=_("Bit Length"), min_value=0,
                                help_text=LENGTH_HELP_TEXT)
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=shared_forms.NAME_REGEX,
                            error_messages=shared_forms.ERROR_MESSAGES)

    def handle(self, request, data):
        try:
            key_uuid = client.generate_symmetric_key(
                request,
                algorithm=data['algorithm'],
                length=data['length'],
                name=data['name'])

            if data['name']:
                key_identifier = data['name']
            else:
                key_identifier = key_uuid
            messages.success(request,
                             _('Successfully generated symmetric key: %s')
                             % key_identifier)
            return key_uuid
        except Exception as e:
            msg = _('Unable to generate symmetric key: %s')
            messages.error(request, msg % e)
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to generate symmetric key.'))
            return False
