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

from django.views import generic
from django.utils.translation import ugettext_lazy as _

from horizon import forms
from horizon import tables
from horizon.tables import views
from horizon.utils import memoized
from castellan_ui.content.symmetric_keys import forms as symmetric_key_forms
from castellan_ui.content.symmetric_keys import tables
from castellan_ui.api import symmetric_key_client


class IndexView(views.MultiTableView):
    table_classes = [
        tables.SymmetricKeyTable
    ]
    template_name = 'symmetric_keys.html'

    def get_symmetric_key_data(self):
        return symmetric_key_client.list(self.request)

class ImportView(forms.ModalFormView):
    form_class = symmetric_key_forms.ImportSymmetricKey
    template_name = 'symmetric_key_import.html'
    #submit_url = reverse_lazy(
    #    "horizon:project:key_pairs:import")
    #success_url = reverse_lazy('horizon:project:key_pairs:index')
    submit_label = page_title = _("Import Symmetric Key")

    def get_object_id(self, key_uuid):
        return key_uuid
