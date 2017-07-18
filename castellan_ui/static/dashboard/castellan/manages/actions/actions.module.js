/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngdoc overview
   * @ngname horizon.dashboard.castellan.manages.actions
   *
   * @description
   * Provides all of the actions for Manages.
   */
  angular
    .module('horizon.dashboard.castellan.manages.actions', [
      'horizon.framework',
      'horizon.dashboard.castellan'
    ])
    .run(registerManageActions);

  registerManageActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.dashboard.castellan.manages.create.service',
    'horizon.dashboard.castellan.manages.update.service',
    'horizon.dashboard.castellan.manages.delete.service',
    'horizon.dashboard.castellan.manages.resourceType'
  ];

  function registerManageActions (
    registry,
    gettext,
    createManageService,
    updateManageService,
    deleteManageService,
    resourceType
  ) {
    var managesResourceType = registry.getResourceType(resourceType);
    managesResourceType.globalActions
      .append({
        id: 'createManageAction',
        service: createManageService,
        template: {
          type: 'create',
          text: gettext('Create Manage')
        }
      });

    managesResourceType.batchActions
      .append({
        id: 'batchDeleteManageAction',
        service: deleteManageService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Manages')
        }
      });

    managesResourceType.itemActions
      .append({
        id: 'updateManageAction',
        service: updateManageService,
        template: {
          text: gettext('Update Manage')
        }
      })
      .append({
        id: 'deleteManageAction',
        service: deleteManageService,
        template: {
          type: 'delete',
          text: gettext('Delete Manage')
        }
      });
  }
})();