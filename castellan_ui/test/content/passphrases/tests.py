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

from django.core.handlers import wsgi
from django.core.urlresolvers import reverse
from horizon import messages as horizon_messages
import mock

from castellan.common.objects import passphrase
from castellan_ui.api import client as api_castellan
from castellan_ui.test import helpers as tests
from castellan_ui.test import test_data

INDEX_URL = reverse('horizon:project:passphrases:index')


class PassphrasesViewTest(tests.APITestCase):

    class FakeCert(object):
        def __init__(self):
            pass

    def setUp(self):
        super(PassphrasesViewTest, self).setUp()
        self.passphrase = test_data.passphrase
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.passphrase))
        self.mock_object(api_castellan, "list", mock.Mock(return_value=[]))
        self.mock_object(horizon_messages, "success")
        FAKE_ENVIRON = {'REQUEST_METHOD': 'GET', 'wsgi.input': 'fake_input'}
        self.request = wsgi.WSGIRequest(FAKE_ENVIRON)

    def test_index(self):
        passphrase_list = [test_data.passphrase, test_data.nameless_passphrase]

        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=passphrase_list))

        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'passphrases.html')
        api_castellan.list.assert_called_with(
            mock.ANY, object_type=passphrase.Passphrase)

    def test_detail_view(self):
        url = reverse('horizon:project:passphrases:detail',
                      args=[self.passphrase.id])
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.passphrase]))
        self.mock_object(
            api_castellan, "get", mock.Mock(return_value=self.passphrase))

        res = self.client.get(url)
        self.assertContains(
            res, "<dt>Name</dt>\n    <dd>%s</dd>" % self.passphrase.name,
            1, 200)
        api_castellan.get.assert_called_once_with(mock.ANY, self.passphrase.id)

    def test_import_cert(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.passphrase]))
        url = reverse('horizon:project:passphrases:import')
        self.mock_object(
            api_castellan, "import_object", mock.Mock(
                return_value=self.passphrase))

        passphrase_input = (
            self.passphrase.get_encoded()
        )

        passphrase_form_data = {
            'source_type': 'raw',
            'name': self.passphrase.name,
            'direct_input': passphrase_input
        }

        self.client.post(url, passphrase_form_data)

        api_castellan.import_object.assert_called_once_with(
            mock.ANY,
            object_type=passphrase.Passphrase,
            passphrase=self.passphrase.get_encoded(),
            name=self.passphrase.name
        )

    def test_delete_cert(self):
        self.mock_object(
            api_castellan, "list", mock.Mock(return_value=[self.passphrase]))
        self.mock_object(api_castellan, "delete")

        passphrase_form_data = {
            'action': 'passphrase__delete__%s' % self.passphrase.id
        }

        res = self.client.post(INDEX_URL, passphrase_form_data)

        api_castellan.list.assert_called_with(
            mock.ANY, object_type=passphrase.Passphrase)
        api_castellan.delete.assert_called_once_with(
            mock.ANY,
            self.passphrase.id,
        )
        self.assertRedirectsNoFollow(res, INDEX_URL)
