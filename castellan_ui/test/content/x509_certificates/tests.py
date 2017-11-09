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

import base64
from django.core.handlers import wsgi
from django.core.urlresolvers import reverse
from horizon import messages as horizon_messages
import mock

from castellan.common.objects import x_509
from castellan_ui.api import client as api_castellan
from castellan_ui.test import helpers as tests
from castellan_ui.test import test_data

INDEX_URL = reverse('horizon:project:x509_certificates:index')


class X509CertificatesViewTest(tests.APITestCase):

    def setUp(self):
        super(X509CertificatesViewTest, self).setUp()
        self.cert = test_data.x509_cert
        self.cert_b64_bytes = base64.b64encode(self.cert.get_encoded())
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.cert))
        self.mock_object(api_castellan, "list", mock.Mock(return_value=[]))
        self.mock_object(horizon_messages, "success")
        FAKE_ENVIRON = {'REQUEST_METHOD': 'GET', 'wsgi.input': 'fake_input'}
        self.request = wsgi.WSGIRequest(FAKE_ENVIRON)

    def test_index(self):
        cert_list = [test_data.x509_cert, test_data.nameless_x509_cert]

        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=cert_list))

        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'x509_certificates.html')
        api_castellan.list.assert_called_with(mock.ANY, object_type=x_509.X509)

    def test_detail_view(self):
        url = reverse('horizon:project:x509_certificates:detail',
                      args=[self.cert.id])
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.cert]))
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.cert))

        res = self.client.get(url)
        self.assertContains(
            res, "<dt>Name</dt>\n    <dd>%s</dd>" % self.cert.name, 1, 200)
        api_castellan.get.assert_called_once_with(mock.ANY, self.cert.id)

    def test_import_cert(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.cert]))
        url = reverse('horizon:project:x509_certificates:import')
        self.mock_object(
            api_castellan, "import_object", mock.Mock(return_value=self.cert))

        cert_input = (
            u"-----BEGIN CERTIFICATE-----\n" +
            self.cert_b64_bytes.decode("utf-8") +
            u"\n-----END CERTIFICATE-----"
        )

        cert_form_data = {
            'source_type': 'raw',
            'name': self.cert.name,
            'direct_input': cert_input
        }

        self.client.post(url, cert_form_data)

        api_castellan.import_object.assert_called_once_with(
            mock.ANY,
            object_type=x_509.X509,
            data=self.cert_b64_bytes.decode('utf-8'),
            name=self.cert.name
        )

    def test_delete_cert(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.cert]))
        self.mock_object(api_castellan, "delete")

        cert_form_data = {
            'action': 'x509_certificate__delete__%s' % self.cert.id
        }

        res = self.client.post(INDEX_URL, cert_form_data)

        api_castellan.list.assert_called_with(mock.ANY, object_type=x_509.X509)
        api_castellan.delete.assert_called_once_with(
            mock.ANY,
            self.cert.id,
        )
        self.assertRedirectsNoFollow(res, INDEX_URL)
