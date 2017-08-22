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
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

import binascii
from castellan.common.objects import symmetric_key
from castellan_ui.api import client
from castellan_ui.content.symmetric_keys import forms as symmetric_key_forms
from castellan_ui.content.symmetric_keys import tables
from datetime import datetime
from horizon import exceptions
from horizon import forms
from horizon.tables import views as tables_views
from horizon.utils import memoized
from horizon import views


def download_key(request, object_id):
    try:
        obj = client.get(request, object_id)
        data = obj.get_encoded()
        response = HttpResponse()
        response.write(data)
        response['Content-Disposition'] = ('attachment; '
                                           'filename="%s.key"' % object_id)
        response['Content-Length'] = str(len(response.content))
        return response

    except Exception:
        redirect = reverse('horizon:project:symmetric_keys:index')
        msg = _('Unable to download symmetric_key "%s".')\
            % (object_id)
        exceptions.handle(request, msg, redirect=redirect)


class IndexView(tables_views.MultiTableView):
    table_classes = [
        tables.SymmetricKeyTable
    ]
    template_name = 'symmetric_keys.html'

    def get_symmetric_key_data(self):
        try:
            return client.list(self.request,
                               object_type=symmetric_key.SymmetricKey)
        except Exception as e:
            msg = _('Unable to list symmetric keys: "%s".') % (e.message)
            exceptions.handle(self.request, msg)
            return []


class GenerateView(forms.ModalFormView):
    form_class = symmetric_key_forms.GenerateSymmetricKey
    template_name = 'symmetric_key_generate.html'
    submit_url = reverse_lazy(
        "horizon:project:symmetric_keys:generate")
    success_url = reverse_lazy('horizon:project:symmetric_keys:index')
    submit_label = page_title = _("Generate Symmetric Key")


class ImportView(forms.ModalFormView):
    form_class = symmetric_key_forms.ImportSymmetricKey
    template_name = 'symmetric_key_import.html'
    submit_url = reverse_lazy(
        "horizon:project:symmetric_keys:import")
    success_url = reverse_lazy('horizon:project:symmetric_keys:index')
    submit_label = page_title = _("Import Symmetric Key")

    def get_object_id(self, key_uuid):
        return key_uuid


class DetailView(views.HorizonTemplateView):
    template_name = 'symmetric_key_detail.html'
    page_title = _("Symmetric Key Details")

    @memoized.memoized_method
    def _get_data(self):
        try:
            obj = client.get(self.request, self.kwargs['object_id'])
        except Exception:
            redirect = reverse('horizon:project:symmetric_keys:index')
            msg = _('Unable to retrieve details for symmetric_key "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return obj

    @memoized.memoized_method
    def _get_data_created_date(self, obj):
        try:
            created_date = datetime.utcfromtimestamp(obj.created).isoformat()
        except Exception:
            redirect = reverse('horizon:project:symmetric_keys:index')
            msg = _('Unable to retrieve details for symmetric_key "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return created_date

    @memoized.memoized_method
    def _get_data_bytes(self, obj):
        try:
            data_bytes = binascii.hexlify(obj.get_encoded())
        except Exception:
            redirect = reverse('horizon:project:symmetric_keys:index')
            msg = _('Unable to retrieve details for symmetric_key "%s".')\
                % (self.kwargs['object_id'])
            exceptions.handle(self.request, msg,
                              redirect=redirect)
        return data_bytes

    def get_context_data(self, **kwargs):
        """Gets the context data for key."""
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self._get_data()
        context['object'] = obj
        context['object_created_date'] = self._get_data_created_date(obj)
        context['object_bytes'] = self._get_data_bytes(obj)
        return context
