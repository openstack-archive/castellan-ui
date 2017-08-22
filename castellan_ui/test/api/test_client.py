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

from openstack_dashboard.test import helpers

from castellan_ui.api import client as api


class ClientApiTests(helpers.APITestCase):

    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_auth_params_from_request(self):
        token, tenant = api.get_auth_params_from_request(self.request)
        self.assertEqual(self.token.id, token)
        self.assertEqual(self.tenant.id, tenant)

    def test_get_context(self):
        ctxt = api.get_context(self.request)
        self.assertEqual(ctxt.auth_token, self.token.id)
        self.assertEqual(ctxt.tenant, self.tenant.id)

    def import_object(self):
        pass
