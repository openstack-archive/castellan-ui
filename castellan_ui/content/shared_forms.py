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


import codecs
import re

from django.utils.translation import ugettext_lazy as _

from castellan.common.objects import symmetric_key
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


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name,
                                                       value,
                                                       attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)


class ImportKey(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"))
    bit_length = forms.IntegerField(label=_("Bit Length"))
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)
    source_type = forms.ChoiceField(
        label=_('Source'),
        required=False,
        choices=[('file', _('Key File')),
                 ('raw', _('Direct Input'))],
        widget=forms.ThemableSelectWidget(
            attrs={'class': 'switchable', 'data-slug': 'source'}))
    key_file = forms.FileField(
        label=_("Choose file"),
        help_text=_("A local key file to upload."),
        widget=forms.FileInput(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-file': _('Key File')}),
        required=False)
    direct_input = forms.CharField(
        label=_('Key Bytes'),
        help_text=_('The JSON formatted contents of a namespace.'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-raw': _('Key Bytes')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        algorithms = kwargs.pop('algorithms', None)
        super(ImportKey, self).__init__(request, *args, **kwargs)
        self.fields['algorithm'].widget = ListTextWidget(data_list=algorithms,
                                                         name='algorithms')

    def clean(self):
        data = super(ImportKey, self).clean()

        # The key can be missing based on particular upload
        # conditions. Code defensively for it here...
        key_file = data.get('key_file', None)
        key_raw = data.get('direct_input', None)

        if key_raw and key_file:
            raise forms.ValidationError(
                _("Cannot specify both file and direct input."))
        if not key_raw and not key_file:
            raise forms.ValidationError(
                _("No input was provided for the key value."))
        try:
            if key_file:
                key_bytes = self.files['key_file'].read()
            else:
                key_str = data['direct_input']
                key_bytes = codecs.decode(key_str, 'hex_codec')
        except Exception as e:
            msg = _('There was a problem loading the key: %s.') % e
            raise forms.ValidationError(msg)

        data['key_bytes'] = key_bytes

        return data

    def handle(self, request, data, key_type):
        try:
            # Remove any new lines in the public key
            key_bytes = data.get('key_bytes')
            key_bytes = NEW_LINES.sub("", key_bytes)
            key_uuid = client.import_object(
                request,
                algorithm=data['algorithm'],
                bit_length=data['bit_length'],
                key=key_bytes,
                name=data['name'],
                object_type=symmetric_key.SymmetricKey)

            if data['name']:
                key_identifier = data['name']
            else:
                key_identifier = key_uuid
            messages.success(request,
                             _('Successfully imported key: %s')
                             % key_identifier)
            return key_uuid
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import key.'))
            return False
