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

import logging

from oslo_context import context

from castellan.common.objects import symmetric_key
from castellan import key_manager

from horizon import exceptions
from horizon.utils.memoized import memoized_with_request

import codecs


LOG = logging.getLogger(__name__)

GENERATE_ATTRIBUTES = ['algorithm', 'length', 'name']
IMPORT_ATTRIBUTES = ['algorithm', 'bit_length', 'name', 'key']


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


def import_symmetric_key(request, **kwargs):
    args = {}
    for (key, value) in kwargs.items():
        if key in IMPORT_ATTRIBUTES:
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(IMPORT_ATTRIBUTES))
    if args['key']:
        args['key'] = codecs.decode(args['key'], 'hex_codec')
    key = symmetric_key.SymmetricKey(**args)
    created_uuid = key_manager.API().store(get_context(request), key)

    return created_uuid


def generate_symmetric_key(request, **kwargs):
    args = {}
    for (key, value) in kwargs.items():
        if key in GENERATE_ATTRIBUTES:
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(GENERATE_ATTRIBUTES))
    created_uuid = key_manager.API().create_key(get_context(request),
                                                **args)

    return created_uuid


def delete(request, id):
    deleted = key_manager.API().delete(get_context(request), id)

    return deleted


def list(request, object_type=None):
    list = key_manager.API().list(get_context(request),
                                  object_type=object_type,
                                  metadata_only=True)
    return list


def get(request, id):
    show = key_manager.API().get(get_context(request), id)
    return show
