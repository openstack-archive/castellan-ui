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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from castellan.common.objects import passphrase
from castellan_ui.api import client
from castellan_ui.content.passphrases import forms as passphrase_forms
from castellan_ui.content.passphrases import tables
from datetime import datetime
from horizon import exceptions
from horizon import forms
from horizon.tables import views as tables_views
from horizon.utils import memoized
from horizon import views


class IndexView(tables_views.MultiTableView):
    table_classes = [
        tables.PassphraseTable
    ]
    template_name = 'passphrases.html'

    def get_passphrase_data(self):
        try:
            return client.list(
                self.request, object_type=passphrase.Passphrase)
        except Exception as e:
            msg = _('Unable to list passphrases: "%s".') % (e.message)
            exceptions.handle(self.request, msg)
            return []


class ImportView(forms.ModalFormView):
    form_class = passphrase_forms.ImportPassphrase
    template_name = 'passphrase_import.html'
    submit_url = reverse_lazy(
        "horizon:project:passphrases:import")
    success_url = reverse_lazy('horizon:project:passphrases:index')
    submit_label = page_title = _("Import Passphrase")

    def get_object_id(self, key_uuid):
        return key_uuid


class DetailView(views.HorizonTemplateView):
    template_name = 'passphrase_detail.html'
    page_title = _("Passphrase Details")

    @memoized.memoized_method
    def _get_data(self):
        try:
            obj = client.get(self.request, self.kwargs['object_id'])
        except Exception:
            redirect = reverse('horizon:project:passphrases:index')
            msg = _('Unable to retrieve details for passphrase "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return obj

    @memoized.memoized_method
    def _get_data_created_date(self, obj):
        try:
            created_date = datetime.utcfromtimestamp(obj.created).isoformat()
        except Exception:
            redirect = reverse('horizon:project:passphrases:index')
            msg = _('Unable to retrieve details for passphrase "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return created_date

    @memoized.memoized_method
    def _get_data_bytes(self, obj):
        return obj.get_encoded()

    def get_context_data(self, **kwargs):
        """Gets the context data for key."""
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self._get_data()
        context['object'] = obj
        context['object_created_date'] = self._get_data_created_date(obj)
        context['object_bytes'] = self._get_data_bytes(obj)
        return context
