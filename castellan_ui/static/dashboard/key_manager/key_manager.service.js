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
    .factory('horizon.app.core.openstack-service-api.key_manager', API);

  API.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext'
  ];

  function API(apiService, toastService, gettext) {
    var service = {
      getManagedObject: getManagedObject,
      getManagedObjects: getManagedObjects,
      createManagedObject: createManagedObject,
      uploadManagedObject: uploadManagedObject,
      updateManagedObject: updateManagedObject,
      deleteManagedObject: deleteManagedObject,
      getSymmetricKey: getSymmetricKey,
      getSymmetricKeys: getSymmetricKeys,
      createSymmetricKey: createSymmetricKey,
      uploadSymmetricKey: uploadSymmetricKey,
      updateSymmetricKey: updateSymmetricKey,
      deleteSymmetricKey: deleteSymmetricKey,
    };

    return service;

    ///////////////
    // ManagedObjects //
    ///////////////

    function getManagedObject(id) {
      return apiService.get('/api/key_manager/managed_objects/' + id)
        .error(function() {
          var msg = gettext('Unable to retrieve the ManagedObject with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    function getManagedObjects() {
      return apiService.get('/api/key_manager/managed_objects/')
        .error(function() {
          toastService.add('error', gettext('Unable to retrieve the ManagedObjects.'));
        });
    }

    function createManagedObject(params) {
      return apiService.put('/api/key_manager/managed_objects/', params)
        .error(function() {
          var msg = gettext('Unable to create the ManagedObject with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function uploadManagedObject(params) {
      return apiService.put('/api/key_manager/managed_objects/', params)
        .error(function() {
          var msg = gettext('Unable to create the ManagedObject with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function updateManagedObject(id, params) {
      return apiService.post('/api/key_manager/managed_objects/' + id, params)
        .error(function() {
          var msg = gettext('Unable to update the ManagedObject with id: %(id)s');
          toastService.add('error', interpolate(msg, { id: params.id }, true));
        });
    }

    function deleteManagedObject(id, suppressError) {
      var promise = apiService.delete('/api/key_manager/managed_objects/', [id]);
      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the ManagedObject with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: id }, true));
      });
    }
    function getSymmetricKey(id) {
      return apiService.get('/api/key_manager/symmetric_keys/' + id)
        .error(function() {
          var msg = gettext('Unable to retrieve the ManagedObject with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    function getSymmetricKeys() {
      return apiService.get('/api/key_manager/symmetric_keys/')
        .error(function() {
          toastService.add('error', gettext('Unable to retrieve the ManagedObjects.'));
        });
    }

    function createSymmetricKey(params) {
      return apiService.put('/api/key_manager/symmetric_keys/', params)
        .error(function() {
          var msg = gettext('Unable to create the ManagedObject with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function uploadSymmetricKey(params) {
      return apiService.put('/api/key_manager/symmetric_keys/', params)
        .error(function() {
          var msg = gettext('Unable to create the ManagedObject with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function updateSymmetricKey(id, params) {
      return apiService.post('/api/key_manager/symmetric_keys/' + id, params)
        .error(function() {
          var msg = gettext('Unable to update the ManagedObject with id: %(id)s');
          toastService.add('error', interpolate(msg, { id: params.id }, true));
        });
    }

    function deleteSymmetricKey(id, suppressError) {
      var promise = apiService.delete('/api/key_manager/symmetric_keys/', [id]);
      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the ManagedObject with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: id }, true));
      });
    }
  }
}());
