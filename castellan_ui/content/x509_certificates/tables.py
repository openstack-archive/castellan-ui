from django.utils.translation import ugettext_lazy as _
from horizon import tables

class ImportX509Certificate(tables.LinkAction):
    name = "import_x509_certificate"
    verbose_name = _("Import X.509 Certificate")
    url = "horizon:project:key_pairs:index"
    classes = ("btn-launch",)
    icon = "upload"
    policy_rules = ()

class X509CertificateTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    created_date = tables.Column("created_date", verbose_name=_("Created Date"))
    expiration_date = tables.Column("expiration_date", verbose_name=_("Expiration Date"))

    class Meta(object):
        name = "x509_certificate"
        table_actions = (ImportX509Certificate,)
        row_actions = ()

