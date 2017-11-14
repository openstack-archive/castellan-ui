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

from castellan.common.objects import opaque_data
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client
from castellan_ui.content import shared_forms


NEW_LINES = re.compile(r"\r|\n")

NAME_REGEX = re.compile(r"^\w+(?:[- ]\w+)*$", re.UNICODE)
ERROR_MESSAGES = {
    'invalid': _('Name may only contain letters, '
                 'numbers, underscores, spaces, and hyphens '
                 'and may not be white space.')}


class ImportOpaqueData(forms.SelfHandlingForm):
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Object Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)
    source_type = forms.ChoiceField(
        label=_('Source'),
        required=False,
        choices=[('file', _('File')),
                 ('raw', _('Direct Input'))],
        widget=forms.ThemableSelectWidget(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    object_file = forms.FileField(
        label=_("Choose file"),
        help_text=_("A local file to upload."),
        widget=forms.FileInput(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-file': _('File')}),
        required=False)
    direct_input = forms.CharField(
        label=_('Object Bytes'),
        help_text=_('The bytes of the object, represented in hex.'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-raw': _('Bytes')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        super(ImportOpaqueData, self).__init__(request, *args, **kwargs)

    def clean(self):
        data = super(ImportOpaqueData, self).clean()

        # The key can be missing based on particular upload
        # conditions. Code defensively for it here...
        key_file = data.get('object_file', None)
        key_raw = data.get('direct_input', None)

        if key_raw and key_file:
            raise forms.ValidationError(
                _("Cannot specify both file and direct input."))
        if not key_raw and not key_file:
            raise forms.ValidationError(
                _("No input was provided for the object value."))
        try:
            if key_file:
                key_bytes = self.files['object_file'].read()
            else:
                key_str = data['direct_input']
                key_bytes = codecs.decode(key_str, 'hex_codec')
        except Exception as e:
            msg = _('There was a problem loading the key: %s.') % e
            raise forms.ValidationError(msg)

        data['object_bytes'] = key_bytes

        return data

    def handle(self, request, data):
        try:
            # Remove any new lines in the public key
            key_bytes = data.get('object_bytes')
            key_bytes = NEW_LINES.sub("", key_bytes)
            key_uuid = client.import_object(
                request,
                data=key_bytes,
                name=data['name'],
                object_type=opaque_data.OpaqueData)

            if data['name']:
                key_identifier = data['name']
            else:
                key_identifier = key_uuid
            messages.success(request,
                             _('Successfully imported object: %s')
                             % key_identifier)
            return key_uuid
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import object.'))
            return False
