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


from castellan_ui.content import filters
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from castellan_ui.api import client
from horizon import tables


class ImportOpaqueData(tables.LinkAction):
    name = "import_opaque_data"
    verbose_name = _("Import Opaque Data")
    url = "horizon:project:opaque_data:import"
    classes = ("ajax-modal",)
    icon = "upload"
    policy_rules = ()


class DownloadOpaqueData(tables.LinkAction):
    name = "download"
    verbose_name = _("Download Opaque Data")
    url = "horizon:project:opaque_data:download"
    classes = ("btn-download",)
    policy_rules = ()

    def get_link_url(self, datum):
        return reverse(self.url,
                       kwargs={'object_id': datum.id})


class DeleteOpaqueData(tables.DeleteAction):
    policy_rules = ()
    help_text = _("You should not delete an object unless you are "
                  "certain it is not being used anywhere.")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Opaque Data",
            u"Delete Opaque Data",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Opaque Data",
            u"Deleted Opaque Data",
            count
        )

    def delete(self, request, obj_id):
        client.delete(request, obj_id)


class OpaqueDataTable(tables.DataTable):
    detail_link = "horizon:project:opaque_data:detail"
    uuid = tables.Column("id", verbose_name=_("Object ID"), link=detail_link)
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created",
                                 verbose_name=_("Created Date"),
                                 filters=(filters.timestamp_to_iso,))

    def get_object_display(self, datum):
        return datum.name if datum.name else datum.id

    class Meta(object):
        name = "opaque_data"
        table_actions = (ImportOpaqueData,
                         DeleteOpaqueData,)
        row_actions = (DownloadOpaqueData, DeleteOpaqueData)
