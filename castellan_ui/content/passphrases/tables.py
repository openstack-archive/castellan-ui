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
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from castellan_ui.api import client
from horizon import tables


class ImportPassphrase(tables.LinkAction):
    name = "import_passphrase"
    verbose_name = _("Import Passphrase")
    url = "horizon:project:passphrases:import"
    classes = ("ajax-modal",)
    icon = "upload"
    policy_rules = ()


class DeletePassphrase(tables.DeleteAction):
    policy_rules = ()
    help_text = _("You should not delete a passphrase unless you are "
                  "certain it is not being used anywhere.")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Passphrase",
            u"Delete Passphrases",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Passphrase",
            u"Deleted Passphrases",
            count
        )

    def delete(self, request, obj_id):
        client.delete(request, obj_id)


class PassphraseTable(tables.DataTable):
    detail_link = "horizon:project:passphrases:detail"
    uuid = tables.Column("id", verbose_name=_("Passphrase ID"),
                         link=detail_link)
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created",
                                 verbose_name=_("Created Date"),
                                 filters=(filters.timestamp_to_iso,))

    def get_object_display(self, datum):
        return datum.name if datum.name else datum.id

    class Meta(object):
        name = "passphrase"
        table_actions = (ImportPassphrase,
                         DeletePassphrase,)
        row_actions = (DeletePassphrase, )
