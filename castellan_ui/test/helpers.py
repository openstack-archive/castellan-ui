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
import mock
import uuid

from castellan_ui import api
from openstack_dashboard.test import helpers


class CastellanTestsMixin(object):
    def _setup_test_data(self):
        super(CastellanTestsMixin, self)._setup_test_data()

    def mock_object(self, obj, attr_name, new_attr=None, **kwargs):
        """Use python mock to mock an object attribute

        Mocks the specified objects attribute with the given value.
        Automatically performs 'addCleanup' for the mock.
        """

        if not new_attr:
            new_attr = mock.Mock()
        patcher = mock.patch.object(obj, attr_name, new_attr, **kwargs)
        patcher.start()
        return new_attr


class APITestCase(CastellanTestsMixin, helpers.APITestCase):

    def setUp(self):
        super(APITestCase, self).setUp()
        self.mock_uuid1 = str(uuid.uuid4())
        self.mock_uuid2 = str(uuid.uuid4())
        self.mock_managed_object = mock.Mock()
        self._key_manager = self.mock_object(api.client,
                                             "key_manager")
        self.key_manager = self._key_manager.return_value
        self.key_manager.store.return_value = self.mock_uuid1
        self.key_manager.create_key.return_value = self.mock_uuid1
        self.key_manager.create_key_pair.return_value = (
            self.mock_uuid1, self.mock_uuid2)
        self.key_manager.get.return_value = self.mock_object
        self.key_manager.delete.return_value = True
        self.key_manager.list.return_value = [self.mock_object]
