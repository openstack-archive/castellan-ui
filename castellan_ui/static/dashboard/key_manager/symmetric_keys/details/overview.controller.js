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
    .module('horizon.dashboard.key_manager.symmetric_keys')
    .controller('horizon.dashboard.key_manager.symmetric_keys.OverviewController', controller);

  controller.$inject = [
    '$scope',
    'horizon.dashboard.key_manager.symmetric_keys.resourceType',
    'horizon.dashboard.key_manager.symmetric_keys.events',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function controller(
    $scope,
    resourceType,
    events,
    registry
  ) {
    var ctrl = this;
    ctrl.symmetric_key = {};

    $scope.context.loadPromise.then(onGetSymmetricKey);

    function onGetSymmetricKey(symmetric_key) {
      ctrl.symmetric_key = symmetric_key.data;
    }
  }
})();
