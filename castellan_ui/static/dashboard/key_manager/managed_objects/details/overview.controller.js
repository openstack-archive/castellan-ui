/*
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  "use strict";

  angular
    .module('horizon.dashboard.key_manager.managed_objects')
    .controller('horizon.dashboard.key_manager.managed_objects.OverviewController', controller);

  controller.$inject = [
    '$scope',
    'horizon.dashboard.key_manager.managed_objects.resourceType',
    'horizon.dashboard.key_manager.managed_objects.events',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function controller(
    $scope,
    resourceType,
    events,
    registry
  ) {
    var ctrl = this;
    ctrl.managed_object = {};

    $scope.context.loadPromise.then(onGetManagedObject);

    function onGetManagedObject(managed_object) {
      ctrl.managed_object = managed_object.data;
    }
  }
})();
