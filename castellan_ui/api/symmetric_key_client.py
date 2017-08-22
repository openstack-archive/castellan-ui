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

from keystoneauth1 import identity
from keystoneauth1 import session
from oslo_config import cfg
from oslo_context import context

from castellan import key_manager
from castellan.common.objects import symmetric_key

from horizon import exceptions
from horizon.utils.memoized import memoized
from openstack_dashboard.api import base

# for stab, should remove when use CLI API
import copy
from datetime import datetime
import uuid


LOG = logging.getLogger(__name__)

ATTRIBUTES = ['algorithm', 'bit_length', 'key', 'name']


def get_context(request):
    username = 'admin'
    password = 'secretadmin'
    project_name = 'admin'
    auth_url = 'http://localhost/identity/v3'
    user_domain_name = 'Default'
    project_domain_name = 'Default'

    auth = identity.V3Password(auth_url=auth_url,
                               username=username,
                               password=password,
                               project_name=project_name,
                               user_domain_name=user_domain_name,
                               project_domain_name=project_domain_name)
    sess = session.Session(auth=auth)

    return context.RequestContext(auth_token=auth.get_token(sess),
                                  tenant=auth.get_project_id(sess))


def create(request, **kwargs):
    args = {}
    for (key, value) in kwargs.items():
        if key in ATTRIBUTES:
            args[str(key)] = value
        else:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(ATTRIBUTES))
    key = symmetric_key.SymmetricKey(**args)
    created_uuid = key_manager.API().store(get_context(), key)

    return created_uuid


def delete(request, id):
    apiclient(request).delete(id)

    return deleted


def list(
        request, limit=None, marker=None, sort_key=None,
        sort_dir=None, detail=True):

    list = [] # key_manager.API().list(get_context(request), metadata_only=True)
    return list


def show(request, id):
    show = apiclient(request).list(id)
    return show
