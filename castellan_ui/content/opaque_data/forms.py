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

from castellan.common.objects import opaque_data
from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client
from castellan_ui.content import shared_forms


class ImportOpaqueData(forms.SelfHandlingForm):
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Data Name"),
                            regex=shared_forms.NAME_REGEX,
                            error_messages=shared_forms.ERROR_MESSAGES)
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

        # The data can be missing based on particular upload
        # conditions. Code defensively for it here...
        data_file = data.get('object_file', None)
        data_raw = data.get('direct_input', None)

        if data_raw and data_file:
            raise forms.ValidationError(
                _("Cannot specify both file and direct input."))
        if not data_raw and not data_file:
            raise forms.ValidationError(
                _("No input was provided for the object value."))
        try:
            if data_file:
                data_bytes = self.files['object_file'].read()
            else:
                data_str = data['direct_input']
                data_bytes = binascii.unhexlify(data_str)
            data['object_bytes'] = base64.b64encode(data_bytes)
        except Exception as e:
            msg = _('There was a problem loading the object: %s. '
                    'Is the object valid and in the correct format?') % e
            raise forms.ValidationError(msg)

        return data

    def handle(self, request, data):
        try:
            data_bytes = data.get('object_bytes')
            data_uuid = client.import_object(
                request,
                data=data_bytes,
                name=data['name'],
                object_type=opaque_data.OpaqueData)

            if data['name']:
                data_identifier = data['name']
            else:
                data_identifier = data_uuid
            messages.success(request,
                             _('Successfully imported object: %s')
                             % data_identifier)
            return data_uuid
        except Exception as e:
            msg = _('Unable to import object: %s')
            messages.error(msg % e)
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import object.'))
            return False
