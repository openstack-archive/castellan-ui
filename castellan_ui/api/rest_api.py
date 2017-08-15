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
class ManagedObject(generic.View):
    """API for retrieving a single ManagedObject"""
    url_regex = r'key_manager/managed_objects/(?P<id>[^/]+)$'

    @rest_utils.ajax()
    def get(self, request, id):
        """Get a specific managed_object"""
        return change_to_id(client.managed_object_show(request, id).to_dict())

    @rest_utils.ajax(data_required=True)
    def post(self, request, id):
        """Update a ManagedObject.

        Returns the updated ManagedObject object on success.
        """
        managed_object = client.managed_object_update(request, id, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/key_manager/managed_object/%s' % managed_object.uuid,
            managed_object.to_dict())


@urls.register
class ManagedObjects(generic.View):
    """API for ManagedObjects"""
    url_regex = r'key_manager/managed_objects/$'

    @rest_utils.ajax()
    def get(self, request):
        """Get a list of the ManagedObjects for a project.

        The returned result is an object with property 'items' and each
        item under this is a ManagedObject.
        """
        result = client.managed_object_list(request)
        return {'items': [change_to_id(n.to_dict()) for n in result]}

    @rest_utils.ajax(data_required=True)
    def delete(self, request):
        """Delete one or more ManagedObjects by id.

        Returns HTTP 204 (no content) on successful deletion.
        """
        for id in request.DATA:
            client.managed_object_delete(request, id)

    @rest_utils.ajax(data_required=True)
    def put(self, request):
        """Create a new ManagedObject.

        Returns the new ManagedObject object on success.
        """
        managed_object = client.managed_object_create(request, **request.DATA)
        return rest_utils.CreatedResponse(
            '/api/key_manager/managed_object/%s' % managed_object.uuid,
            managed_object.to_dict())
