from django.utils.translation import ugettext_lazy as _
from horizon import tables

class ImportOpaqueData(tables.LinkAction):
    name = "import_opaque_data"
    verbose_name = _("Import Opaque Data")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "upload"
    policy_rules = ()

class OpaqueDataTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created_date", verbose_name=_("Created Date"))
    expiration_date = tables.Column("expiration_date", verbose_name=_("Expiration Date"))

    class Meta(object):
        name = "opaque_data"
        table_actions = (ImportOpaqueData,)
        row_actions = ()

