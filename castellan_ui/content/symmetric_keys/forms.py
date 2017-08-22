import re

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from castellan_ui.api import symmetric_key_client


NEW_LINES = re.compile(r"\r|\n")

KEYPAIR_NAME_REGEX = re.compile(r"^\w+(?:[- ]\w+)*$", re.UNICODE)
KEYPAIR_ERROR_MESSAGES = {
    'invalid': _('Key pair name may only contain letters, '
                 'numbers, underscores, spaces, and hyphens '
                 'and may not be white space.')}


class ImportSymmetricKey(forms.SelfHandlingForm):
    algorithm = forms.CharField(label=_("Algorithm"),
                                 widget=forms.Textarea())
    bit_length = forms.CharField(label=_("Bit Length"),
                                 widget=forms.Textarea())
    name = forms.RegexField(max_length=255,
                            label=_("Key Pair Name"),
                            regex=KEYPAIR_NAME_REGEX,
                            error_messages=KEYPAIR_ERROR_MESSAGES)
    key = forms.CharField(label=_("Symmetric Key"),
                                 widget=forms.Textarea())

    def handle(self, request, data):
        try:
            # Remove any new lines in the public key
            data['symmetric_key'] = NEW_LINES.sub("", data['symmetric_key'])
            
            key_uuid = symmetric_key_client.create(request,
                                                   algorithm=data['algorithm'],
                                                   bit_length=data['bit_length'],
                                                   key=data['key'],
                                                   name=data['name'])

            messages.success(request,
                             _('Successfully imported public key: %s')
                             % data['name'])
            return key_uuid
        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Unable to import key pair.'))
            return False
