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


import abc
import re

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import client


KEY_PAIR_ALGORITHMS = ('RSA', 'DSA')

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
        help_text=_('The bytes of the key (represented as hex characters)'),
        widget=forms.widgets.Textarea(
            attrs={'class': 'switched', 'data-switch-on': 'source',
                   'data-source-raw': _('Key Bytes')}),
        required=False)

    def __init__(self, request, *args, **kwargs):
        algorithms = kwargs.pop('algorithms', None)
        super(ImportKey, self).__init__(request, *args, **kwargs)
        self.fields['algorithm'].widget = ListTextWidget(data_list=algorithms,
                                                         name='algorithms')

    @abc.abstractmethod
    def clean_key_data(self, key_pem):
        """This should be implemented for the specific key import form"""
        return

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
                key_pem = self.files['key_file'].read()
            else:
                key_pem = data['direct_input']
        except Exception as e:
            msg = _('There was a problem loading the key: %s.') % e
            raise forms.ValidationError(msg)

        data['key_data'] = self.clean_key_data(key_pem)

        return data

    def handle(self, request, data, key_type):
        try:
            key_uuid = client.import_object(
                request,
                algorithm=data['algorithm'],
                bit_length=data['bit_length'],
                key=data['key_data'],
                name=data['name'],
                object_type=key_type)

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


class GenerateKeyPair(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                widget=ListTextWidget(
                                    data_list=KEY_PAIR_ALGORITHMS,
                                    name='algorithm-list'))
    length = forms.IntegerField(label=_("Bit Length"))
    name = forms.RegexField(required=False,
                            max_length=255,
                            label=_("Key Name"),
                            regex=NAME_REGEX,
                            error_messages=ERROR_MESSAGES)

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
            self.api_error(_('Unable to generate key pair.'))
            return False
