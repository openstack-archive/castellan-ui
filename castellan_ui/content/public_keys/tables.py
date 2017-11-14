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


class GeneratePublicKey(tables.LinkAction):
    name = "generate_public_key"
    verbose_name = _("Generate Key Pair")
    url = "horizon:project:public_keys:generate"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = ()


class ImportPublicKey(tables.LinkAction):
    name = "import_public_key"
    verbose_name = _("Import Public Key")
    url = "horizon:project:public_keys:import"
    classes = ("ajax-modal",)
    icon = "upload"
    policy_rules = ()


class DownloadKey(tables.LinkAction):
    name = "download"
    verbose_name = _("Download Key")
    url = "horizon:project:public_keys:download"
    classes = ("btn-download",)
    policy_rules = ()

    def get_link_url(self, datum):
        return reverse(self.url,
                       kwargs={'object_id': datum.id})


class DeletePublicKey(tables.DeleteAction):
    policy_rules = ()
    help_text = _("You should not delete a public key unless you are "
                  "certain it is not being used anywhere.  If there was a "
                  "private key generated with this public key, it will not "
                  "be deleted.")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Public Key",
            u"Delete Public Keys",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Public Key",
            u"Deleted Public Keys",
            count
        )

    def delete(self, request, obj_id):
        client.delete(request, obj_id)


class PublicKeyTable(tables.DataTable):
    detail_link = "horizon:project:public_keys:detail"
    uuid = tables.Column("id", verbose_name=_("Key ID"), link=detail_link)
    name = tables.Column("name", verbose_name=_("Name"))
    algorithm = tables.Column("algorithm", verbose_name=_("Algorithm"))
    bit_length = tables.Column("bit_length", verbose_name=_("Bit Length"))
    created_date = tables.Column("created",
                                 verbose_name=_("Created Date"),
                                 filters=(filters.timestamp_to_iso,))

    def get_object_display(self, datum):
        return datum.name if datum.name else datum.id

    class Meta(object):
        name = "public_key"
        table_actions = (GeneratePublicKey,
                         ImportPublicKey,
                         DeletePublicKey,)
        row_actions = (DownloadKey, DeletePublicKey)
