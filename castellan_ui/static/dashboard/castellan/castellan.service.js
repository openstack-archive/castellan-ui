/**
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.castellan', API);

  API.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext'
  ];

  function API(apiService, toastService, gettext) {
    var service = {
      getManage: getManage,
      getManages: getManages,
      createManage: createManage,
      updateManage: updateManage,
      deleteManage: deleteManage,
    };

    return service;

    ///////////////
    // Manages //
    ///////////////

    function getManage(id) {
      return apiService.get('/api/castellan/manages/' + id)
        .error(function() {
          var msg = gettext('Unable to retrieve the Manage with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    function getManages() {
      return apiService.get('/api/castellan/manages/')
        .error(function() {
          toastService.add('error', gettext('Unable to retrieve the Manages.'));
        });
    }

    function createManage(params) {
      return apiService.put('/api/castellan/manages/', params)
        .error(function() {
          var msg = gettext('Unable to create the Manage with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function updateManage(id, params) {
      return apiService.post('/api/castellan/manages/' + id, params)
        .error(function() {
          var msg = gettext('Unable to update the Manage with id: %(id)s');
          toastService.add('error', interpolate(msg, { id: params.id }, true));
        });
    }

    function deleteManage(id, suppressError) {
      var promise = apiService.delete('/api/castellan/manages/', [id]);
      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the Manage with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: id }, true));
      });
    }
  }
}());