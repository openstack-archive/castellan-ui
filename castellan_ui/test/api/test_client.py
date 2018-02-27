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
import mock
import uuid

from castellan.common.objects import symmetric_key
from castellan_ui.api import client as api
from castellan_ui.test import helpers as base

from horizon import exceptions


class ClientApiTests(base.APITestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.ctxt = api.get_context(self.request)

    def test_get_auth_params_from_request(self):
        token, tenant = api.get_auth_params_from_request(self.request)
        self.assertEqual(self.token.id, token)
        self.assertEqual(self.tenant.id, tenant)

    def test_get_context(self):
        ctxt = api.get_context(self.request)
        self.assertEqual(ctxt.auth_token, self.token.id)
        self.assertEqual(ctxt.tenant, self.tenant.id)
        self.assertEqual(ctxt, self.ctxt)

    def test_import_object(self):
        algorithm = "AES"
        bit_length = 48
        name = None
        key = b'deadbeef'
        key_b64 = base64.b64encode(key)
        actual_uuid = api.import_object(
            self.request,
            algorithm=algorithm,
            bit_length=bit_length,
            name=name,
            key=key_b64,
            object_type=symmetric_key.SymmetricKey)
        self.key_manager.store.assert_called_once()
        args, kwargs = self.key_manager.store.call_args
        actual_ctxt, actual_key = args
        self.assertEqual(actual_uuid, self.mock_uuid1)
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_key.algorithm, algorithm)
        self.assertEqual(actual_key.bit_length, bit_length)
        self.assertEqual(actual_key.name, name)
        self.assertEqual(actual_key.get_encoded(), key)

    def test_import_object_includes_invalid_param(self):
        algorithm = "AES"
        bit_length = 256
        name = None
        key = b'deadbeef'
        other_value = "other_value"
        with self.assertRaises(exceptions.BadRequest):
            api.import_object(
                self.request,
                algorithm=algorithm,
                bit_length=bit_length,
                name=name,
                key=key,
                object_type=symmetric_key.SymmetricKey,
                other_value=other_value)

    def test_generate_symmetric_key(self):
        algorithm = "AES"
        length = 256
        name = None
        actual_uuid = api.generate_symmetric_key(
            self.request,
            algorithm=algorithm,
            length=length,
            name=name)
        self.key_manager.create_key.assert_called_once()
        args, kwargs = self.key_manager.create_key.call_args
        (actual_ctxt,) = args
        actual_algorithm = kwargs.get("algorithm")
        actual_length = kwargs.get("length")
        actual_name = kwargs.get("name")
        self.assertEqual(actual_uuid, self.mock_uuid1)
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_algorithm, algorithm)
        self.assertEqual(actual_length, length)
        self.assertEqual(actual_name, name)

    def test_generate_symmetric_key_includes_invalid_param(self):
        algorithm = "AES"
        length = 256
        name = None
        other_value = "other_value"
        with self.assertRaises(exceptions.BadRequest):
            api.generate_symmetric_key(
                self.request,
                algorithm=algorithm,
                length=length,
                name=name,
                other_value=other_value)

    def test_generate_key_pair(self):
        algorithm = "RSA"
        length = 2048
        name = None
        actual_result = api.generate_key_pair(
            self.request,
            algorithm=algorithm,
            length=length,
            name=name)
        self.key_manager.create_key_pair.assert_called_once()
        args, kwargs = self.key_manager.create_key_pair.call_args
        (actual_ctxt,) = args
        actual_algorithm = kwargs.get("algorithm")
        actual_length = kwargs.get("length")
        actual_name = kwargs.get("name")
        self.assertTrue(self.mock_uuid1 in actual_result)
        self.assertTrue(self.mock_uuid2 in actual_result)
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_algorithm, algorithm)
        self.assertEqual(actual_length, length)
        self.assertEqual(actual_name, name)

    def test_generate_key_pair_invalid_param(self):
        algorithm = "RSA"
        length = 2048
        name = None
        other_value = "other_value"
        with self.assertRaises(exceptions.BadRequest):
            api.generate_key_pair(
                self.request,
                algorithm=algorithm,
                length=length,
                name=name,
                other_value=other_value)

    def test_delete(self):
        object_id = str(uuid.uuid4())
        api.delete(self.request, object_id)
        self.key_manager.delete.assert_called_once()
        args, kwargs = self.key_manager.delete.call_args
        actual_ctxt, actual_id = args
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_id, object_id)

    def test_list(self):
        api.list(self.request)
        self.key_manager.list.assert_called_once()
        args, kwargs = self.key_manager.list.call_args
        (actual_ctxt,) = args
        actual_object_type = kwargs.get("object_type")
        actual_metadata_only = kwargs.get("metadata_only")
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertIsNone(actual_object_type)
        self.assertTrue(actual_metadata_only)

    def test_list_with_type(self):
        object_type = mock.Mock()
        api.list(self.request, object_type=object_type)
        self.key_manager.list.assert_called_once()
        args, kwargs = self.key_manager.list.call_args
        (actual_ctxt,) = args
        actual_object_type = kwargs.get("object_type")
        actual_metadata_only = kwargs.get("metadata_only")
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_object_type, object_type)
        self.assertTrue(actual_metadata_only)

    def test_get(self):
        object_id = str(uuid.uuid4())
        api.get(self.request, object_id)
        self.key_manager.get.assert_called_once()
        args, kwargs = self.key_manager.get.call_args
        actual_ctxt, actual_id = args
        self.assertEqual(actual_ctxt, self.ctxt)
        self.assertEqual(actual_id, object_id)
