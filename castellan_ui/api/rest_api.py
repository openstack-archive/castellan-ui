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

from django.views import generic

from castellan_ui.api import client

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils


def change_to_id(obj):
    """Change key named 'uuid' to 'id'

    API returns objects with a field called 'uuid' many of Horizons
    directives however expect objects to have a field called 'id'.
    """
    obj['id'] = obj.pop('uuid')
    return obj


@urls.register
class Manage(generic.View):
    """API for retrieving a single Manage"""
    url_regex = r'castellan/manages/(?P<id>[^/]+)$'

    @rest_utils.ajax()
    def get(self, request, id):
        """Get a specific manage"""
        return change_to_id(client.manage_show(request, id).to_dict())

    @rest_utils.ajax(data_required=True)
    def post(self, request, id):
        """Update a Manage.

        Returns the updated Manage object on success.
        """
        manage = client.manage_update(request, id, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/castellan/manage/%s' % manage.uuid,
            manage.to_dict())


@urls.register
class Manages(generic.View):
    """API for Manages"""
    url_regex = r'castellan/manages/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of the Manages for a project.

        The returned result is an object with property 'items' and each
        item under this is a Manage.
        """
        result = client.manage_list(request)
        return {'items': [change_to_id(n.to_dict()) for n in result]}

    @rest_utils.ajax(data_required=True)
    def delete(self, request):
        """Delete one or more Manages by id.

        Returns HTTP 204 (no content) on successful deletion.
        """
        for id in request.DATA:
            client.manage_delete(request, id)

    @rest_utils.ajax(data_required=True)
    def put(self, request):
        """Create a new Manage.

        Returns the new Manage object on success.
        """
        manage = client.manage_create(request, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/castellan/manage/%s' % manage.uuid,
            manage.to_dict())