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
import re

from castellan.common.objects import passphrase
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client


NEW_LINES = re.compile(r"\r|\n")

NAME_REGEX = re.compile(r"^\w+(?:[- ]\w+)*$", re.UNICODE)
ERROR_MESSAGES = {
    'invalid': _('Name may only contain letters, '
                 'numbers, underscores, spaces, and hyphens '
                 'and may not be white space.')}


class ImportPassphrase(forms.SelfHandlingForm):
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Passphrase Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)
    direct_input = forms.CharField(
        label=_('Passphrase'),
        help_text=_('The text of the passphrase'),
        widget=forms.widgets.Textarea(),
        required=True)

    def handle(self, request, data):
        try:
            # Remove any new lines in the public object
            direct_input = data.get('direct_input')
            direct_input = NEW_LINES.sub("", direct_input)
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
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import passphrase.'))
            return False
