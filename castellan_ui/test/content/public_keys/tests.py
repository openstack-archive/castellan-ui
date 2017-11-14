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

from castellan.common.objects import public_key
from castellan_ui.api import client as api_castellan
from castellan_ui.test import helpers as tests
from castellan_ui.test import test_data

INDEX_URL = reverse('horizon:project:public_keys:index')


class PublicKeysViewTest(tests.APITestCase):

    def setUp(self):
        super(PublicKeysViewTest, self).setUp()
        self.key = test_data.public_key
        self.key_b64_bytes = base64.b64encode(self.key.get_encoded())
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.key))
        self.mock_object(api_castellan, "list", mock.Mock(return_value=[]))
        self.mock_object(horizon_messages, "success")
        FAKE_ENVIRON = {'REQUEST_METHOD': 'GET', 'wsgi.input': 'fake_input'}
        self.request = wsgi.WSGIRequest(FAKE_ENVIRON)

    def test_index(self):
        key_list = [test_data.public_key, test_data.nameless_public_key]

        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=key_list))

        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'public_keys.html')
        api_castellan.list.assert_called_with(
            mock.ANY, object_type=public_key.PublicKey)

    def test_detail_view(self):
        url = reverse('horizon:project:public_keys:detail',
                      args=[self.key.id])
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.key]))
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.key))

        res = self.client.get(url)
        self.assertContains(
            res, "<dt>Name</dt>\n    <dd>%s</dd>" % self.key.name, 1, 200)
        api_castellan.get.assert_called_once_with(mock.ANY, self.key.id)

    def test_generate_key_pair(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.key]))
        url = reverse('horizon:project:public_keys:generate')
        self.mock_object(
            api_castellan, "generate_key_pair",
            mock.Mock(return_value=(self.key, self.key)))

        key_form_data = {
            'name': self.key.name,
            'length': 2048,
            'algorithm': 'RSA'
        }

        self.client.post(url, key_form_data)

        api_castellan.generate_key_pair.assert_called_once_with(
            mock.ANY,
            name=self.key.name,
            algorithm=u'RSA',
            length=2048
        )

    def test_import_key(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.key]))
        url = reverse('horizon:project:public_keys:import')
        self.mock_object(
            api_castellan, "import_object", mock.Mock(return_value=self.key))

        key_input = (
            u"-----BEGIN PUBLIC KEY-----\n" +
            self.key_b64_bytes.decode("utf-8") +
            u"\n-----END PUBLIC KEY-----"
        )

        key_form_data = {
            'source_type': 'raw',
            'name': self.key.name,
            'direct_input': key_input,
            'bit_length': 2048,
            'algorithm': 'RSA'
        }

        self.client.post(url, key_form_data)

        api_castellan.import_object.assert_called_once_with(
            mock.ANY,
            object_type=public_key.PublicKey,
            key=self.key_b64_bytes,
            name=self.key.name,
            algorithm=u'RSA',
            bit_length=2048
        )

    def test_delete_key(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.key]))
        self.mock_object(api_castellan, "delete")

        key_form_data = {
            'action': 'public_key__delete__%s' % self.key.id
        }

        res = self.client.post(INDEX_URL, key_form_data)

        api_castellan.list.assert_called_with(
            mock.ANY, object_type=public_key.PublicKey)
        api_castellan.delete.assert_called_once_with(
            mock.ANY,
            self.key.id,
        )
        self.assertRedirectsNoFollow(res, INDEX_URL)
