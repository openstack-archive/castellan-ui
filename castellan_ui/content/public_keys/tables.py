from django.utils.translation import ugettext_lazy as _
from horizon import tables

class GenerateKeyPair(tables.LinkAction):
    name = "generate_key_pair"
    verbose_name = _("Generate Key Pair")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "plus"
    policy_rules = ()

class ImportPublicKey(tables.LinkAction):
    name = "import_public_key"
    verbose_name = _("Import Public Key")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "upload"
    policy_rules = ()

class PublicKeyTable(tables.DataTable):
    algorithm = tables.Column("algorithm", verbose_name=_("Algorithm"))
    bit_length = tables.Column("bit_length", verbose_name=_("Bit Length"))
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created_date", verbose_name=_("Created Date"))
    expiration_date = tables.Column("expiration_date", verbose_name=_("Expiration Date"))

    class Meta(object):
        name = "public_key"
        table_actions = (GenerateKeyPair,
                         ImportPublicKey,)
        row_actions = ()

