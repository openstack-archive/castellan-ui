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
    .module('horizon.dashboard.castellan.manages')
    .controller('horizon.dashboard.castellan.manages.OverviewController', controller);

  controller.$inject = [
    '$scope',
    'horizon.dashboard.castellan.manages.resourceType',
    'horizon.dashboard.castellan.manages.events',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function controller(
    $scope,
    resourceType,
    events,
    registry
  ) {
    var ctrl = this;
    ctrl.manage = {};

    $scope.context.loadPromise.then(onGetManage);

    function onGetManage(manage) {
      ctrl.manage = manage.data;
    }
  }
})();