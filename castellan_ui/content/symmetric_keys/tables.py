from django.utils.translation import ugettext_lazy as _
from horizon import tables

class GenerateSymmetricKey(tables.LinkAction):
    name = "generate_symmetric_key"
    verbose_name = _("Generate Symmetric Key")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "plus"
    policy_rules = ()

class ImportSymmetricKey(tables.LinkAction):
    name = "import_symmetric_key"
    verbose_name = _("Import Symmetric Key")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "upload"
    policy_rules = ()

class SymmetricKeyTable(tables.DataTable):
    algorithm = tables.Column("algorithm", verbose_name=_("Algorithm"))
    bit_length = tables.Column("bit_length", verbose_name=_("Bit Length"))
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created_date", verbose_name=_("Created Date"))
    expiration_date = tables.Column("expiration_date", verbose_name=_("Expiration Date"))

    class Meta(object):
        name = "symmetric_key"
        table_actions = (GenerateSymmetricKey,
                         ImportSymmetricKey,)
        row_actions = ()

