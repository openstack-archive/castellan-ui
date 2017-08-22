from django.utils.translation import ugettext_lazy as _
from horizon import tables

class ImportPassphrase(tables.LinkAction):
    name = "import_passphrase"
    verbose_name = _("Import Passphrase")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "upload"
    policy_rules = ()

class PassphraseTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created_date", verbose_name=_("Created Date"))
    expiration_date = tables.Column("expiration_date", verbose_name=_("Expiration Date"))

    class Meta(object):
        name = "passphrase"
        table_actions = (ImportPassphrase,)
        row_actions = ()

