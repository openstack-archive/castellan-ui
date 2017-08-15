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
   * @ngname horizon.dashboard.key_manager.managed_objects.actions
   *
   * @description
   * Provides all of the actions for ManagedObjects.
   */
  angular
    .module('horizon.dashboard.key_manager.managed_objects.actions', [
      'horizon.framework',
      'horizon.dashboard.key_manager'
    ])
    .run(registerManagedObjectActions);

  registerManagedObjectActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.dashboard.key_manager.managed_objects.create.service',
    'horizon.dashboard.key_manager.managed_objects.upload.service',
    'horizon.dashboard.key_manager.managed_objects.update.service',
    'horizon.dashboard.key_manager.managed_objects.delete.service',
    'horizon.dashboard.key_manager.managed_objects.resourceType'
  ];

  function registerManagedObjectActions (
    registry,
    gettext,
    createManagedObjectService,
    uploadManagedObjectService,
    updateManagedObjectService,
    deleteManagedObjectService,
    resourceType
  ) {
    var managed_objectsResourceType = registry.getResourceType(resourceType);
    managed_objectsResourceType.globalActions
      .append({
        id: 'createManagedObjectAction',
        service: createManagedObjectService,
        template: {
          type: 'create',
          text: gettext('Create Managed Object')
        }
      });

    managed_objectsResourceType.globalActions
      .append({
        id: 'uploadManagedObjectAction',
        service: uploadManagedObjectService,
        template: {
          type: 'create',
          text: gettext('Upload Managed Object')
        }
      });

    managed_objectsResourceType.batchActions
      .append({
        id: 'batchDeleteManagedObjectAction',
        service: deleteManagedObjectService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete ManagedObjects')
        }
      });

    managed_objectsResourceType.itemActions
      .append({
        id: 'updateManagedObjectAction',
        service: updateManagedObjectService,
        template: {
          text: gettext('Update ManagedObject')
        }
      })
      .append({
        id: 'deleteManagedObjectAction',
        service: deleteManagedObjectService,
        template: {
          type: 'delete',
          text: gettext('Delete ManagedObject')
        }
      });
  }
})();
