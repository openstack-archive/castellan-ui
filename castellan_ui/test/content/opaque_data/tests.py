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
import binascii
from django.core.handlers import wsgi
from django.core.urlresolvers import reverse
from horizon import messages as horizon_messages
import mock

from castellan.common.objects import opaque_data
from castellan_ui.api import client as api_castellan
from castellan_ui.test import helpers as tests
from castellan_ui.test import test_data

INDEX_URL = reverse('horizon:project:opaque_data:index')


class OpaqueDataViewTest(tests.APITestCase):

    def setUp(self):
        super(OpaqueDataViewTest, self).setUp()
        self.data = test_data.opaque_data
        self.data_b64_bytes = base64.b64encode(self.data.get_encoded())
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.data))
        self.mock_object(api_castellan, "list", mock.Mock(return_value=[]))
        self.mock_object(horizon_messages, "success")
        FAKE_ENVIRON = {'REQUEST_METHOD': 'GET', 'wsgi.input': 'fake_input'}
        self.request = wsgi.WSGIRequest(FAKE_ENVIRON)

    def test_index(self):
        data_list = [test_data.opaque_data, test_data.nameless_opaque_data]

        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=data_list))

        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'opaque_data.html')
        api_castellan.list.assert_called_with(
            mock.ANY, object_type=opaque_data.OpaqueData)

    def test_detail_view(self):
        url = reverse('horizon:project:opaque_data:detail',
                      args=[self.data.id])
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.data]))
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.data))

        res = self.client.get(url)
        self.assertContains(
            res, "<dt>Name</dt>\n    <dd>%s</dd>" % self.data.name, 1, 200)
        api_castellan.get.assert_called_once_with(mock.ANY, self.data.id)

    def test_import_data(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.data]))
        url = reverse('horizon:project:opaque_data:import')
        self.mock_object(
            api_castellan, "import_object", mock.Mock(return_value=self.data))

        data_input = (
            binascii.hexlify(self.data.get_encoded()).decode('utf-8')
        )

        data_form_data = {
            'source_type': 'raw',
            'name': self.data.name,
            'direct_input': data_input,
        }

        self.client.post(url, data_form_data)

        api_castellan.import_object.assert_called_once_with(
            mock.ANY,
            object_type=opaque_data.OpaqueData,
            data=self.data_b64_bytes,
            name=self.data.name,
        )

    def test_delete_data(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.data]))
        self.mock_object(api_castellan, "delete")

        data_form_data = {
            'action': 'opaque_data__delete__%s' % self.data.id
        }

        res = self.client.post(INDEX_URL, data_form_data)

        api_castellan.list.assert_called_with(
            mock.ANY, object_type=opaque_data.OpaqueData)
        api_castellan.delete.assert_called_once_with(
            mock.ANY,
            self.data.id,
        )
        self.assertRedirectsNoFollow(res, INDEX_URL)
