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


from __future__ import absolute_import

import base64
import logging

from oslo_context import context

from castellan.common import exception as castellan_exception
from castellan.common.objects import key as key_type
from castellan.common.objects import opaque_data
from castellan.common.objects import passphrase
from castellan.common.objects import x_509
from castellan import key_manager as key_manager_api

from horizon import exceptions
from horizon.utils.memoized import memoized_with_request


LOG = logging.getLogger(__name__)

GENERATE_ATTRIBUTES = ['algorithm', 'length', 'name']
IMPORT_KEY_ATTRIBUTES = ['algorithm', 'bit_length', 'name',
                         'key']
IMPORT_CERT_ATTRIBUTES = ['name', 'data']
IMPORT_PASSPHRASE_ATTRIBUTES = ['name', 'passphrase']
IMPORT_DATA_ATTRIBUTES = ['name', 'data']


def key_manager():
    return key_manager_api.API()


def get_auth_params_from_request(request):
    return(
        request.user.token.id,
        request.user.tenant_id,
    )


@memoized_with_request(get_auth_params_from_request)
def get_context(request_auth_params):
    token_id, tenant_id = request_auth_params

    return context.RequestContext(auth_token=token_id,
                                  tenant=tenant_id)


def import_object(request, **kwargs):
    args = {}
    try:
        object_type = kwargs.pop('object_type')
    except TypeError:
        raise exceptions.BadRequest("Object type must be included in kwargs")
    for (key, value) in kwargs.items():
        if key in ['data', 'key']:
            # the data was passed in b64 encoded because some of the bytes
            # were changed when the raw bytes were passed from the form
            value = base64.b64decode(value)

        if (issubclass(object_type, key_type.Key) and
                key in IMPORT_KEY_ATTRIBUTES):
            args[str(key)] = value
        elif object_type == x_509.X509 and key in IMPORT_CERT_ATTRIBUTES:
            args[str(key)] = value
        elif (object_type == passphrase.Passphrase and
                key in IMPORT_PASSPHRASE_ATTRIBUTES):
            args[str(key)] = value
        elif (object_type == opaque_data.OpaqueData and
                key in IMPORT_DATA_ATTRIBUTES):
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Attribute must be in %s" % ",".join(IMPORT_KEY_ATTRIBUTES))
    key = object_type(**args)
    created_uuid = key_manager().store(get_context(request), key)

    return created_uuid


def generate_symmetric_key(request, **kwargs):
    args = {}
    for (key, value) in kwargs.items():
        if key in GENERATE_ATTRIBUTES:
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(GENERATE_ATTRIBUTES))
    created_uuid = key_manager().create_key(get_context(request),
                                            **args)

    return created_uuid


def generate_key_pair(request, **kwargs):
    args = {}
    for (key, value) in kwargs.items():
        if key in GENERATE_ATTRIBUTES:
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(GENERATE_ATTRIBUTES))
    private_uuid, public_uuid = key_manager().create_key_pair(
        get_context(request),
        **args)

    return "{priv} + {pub}".format(priv=private_uuid, pub=public_uuid)


def delete(request, id):
    deleted = key_manager().delete(get_context(request), id)

    return deleted


def list(request, object_type=None):
    try:
        list = key_manager().list(
            get_context(request), object_type=object_type, metadata_only=True)
    except castellan_exception.KeyManagerError as e:
        raise exceptions.BadRequest("Could not list objects: %s" % e.message)

    return list


def get(request, id):
    show = key_manager().get(get_context(request), id)
    return show
