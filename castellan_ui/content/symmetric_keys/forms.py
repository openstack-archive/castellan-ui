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


import re

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client


NEW_LINES = re.compile(r"\r|\n")

NAME_REGEX = re.compile(r"^\w+(?:[- ]\w+)*$", re.UNICODE)
ERROR_MESSAGES = {
    'invalid': _('Key name may only contain letters, '
                 'numbers, underscores, spaces, and hyphens '
                 'and may not be white space.')}


class ImportSymmetricKey(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                widget=forms.TextInput())
    bit_length = forms.IntegerField(label=_("Bit Length"))
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)
    key = forms.CharField(label=_("Symmetric Key Bytes (in hex)"),
                          widget=forms.Textarea())

    def handle(self, request, data):
        try:
            # Remove any new lines in the public key
            data['key'] = NEW_LINES.sub("", data['key'])
            key_uuid = client.import_symmetric_key(
                request,
                algorithm=data['algorithm'],
                bit_length=data['bit_length'],
                key=data['key'],
                name=data['name'])

            if data['name']:
                key_identifier = data['name']
            else:
                key_identifier = key_uuid
            messages.success(request,
                             _('Successfully imported symmetric key: %s')
                             % key_identifier)
            return key_uuid
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import symmetric key.'))
            return False


class GenerateSymmetricKey(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                widget=forms.TextInput())
    length = forms.IntegerField(label=_("Bit Length"))
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)

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
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to generate symmetric key.'))
            return False
