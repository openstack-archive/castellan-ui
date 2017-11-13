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


from django.utils.translation import ugettext_lazy as _

from castellan.common.objects import passphrase
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client
from castellan_ui.content import shared_forms


class ImportPassphrase(forms.SelfHandlingForm):
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Passphrase Name"),
                            regex=shared_forms.NAME_REGEX,
                            error_messages=shared_forms.ERROR_MESSAGES)
    direct_input = forms.CharField(
        label=_('Passphrase'),
        help_text=_('The text of the passphrase in plaintext'),
        widget=forms.widgets.Textarea(),
        required=True)

    def handle(self, request, data):
        try:
            # Remove any new lines in the passphrase
            direct_input = data.get('direct_input')
            direct_input = shared_forms.NEW_LINES.sub("", direct_input)
            object_uuid = client.import_object(
                request,
                passphrase=direct_input,
                name=data['name'],
                object_type=passphrase.Passphrase)

            if data['name']:
                object_identifier = data['name']
            else:
                object_identifier = object_uuid
            messages.success(request,
                             _('Successfully imported passphrase: %s')
                             % object_identifier)
            return object_uuid
        except Exception as e:
            msg = _('Unable to import passphrase: %s')
            messages.error(request, msg % e)
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import passphrase.'))
            return False
