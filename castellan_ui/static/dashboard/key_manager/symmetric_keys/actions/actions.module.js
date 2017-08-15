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
   * @ngname horizon.dashboard.key_manager.symmetric_keys.actions
   *
   * @description
   * Provides all of the actions for SymmetricKeys.
   */
  angular
    .module('horizon.dashboard.key_manager.symmetric_keys.actions', [
      'horizon.framework',
      'horizon.dashboard.key_manager'
    ])
    .run(registerSymmetricKeyActions);

  registerSymmetricKeyActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.dashboard.key_manager.symmetric_keys.create.service',
    'horizon.dashboard.key_manager.symmetric_keys.upload.service',
    'horizon.dashboard.key_manager.symmetric_keys.update.service',
    'horizon.dashboard.key_manager.symmetric_keys.delete.service',
    'horizon.dashboard.key_manager.symmetric_keys.resourceType'
  ];

  function registerSymmetricKeyActions (
    registry,
    gettext,
    createSymmetricKeyService,
    uploadSymmetricKeyService,
    updateSymmetricKeyService,
    deleteSymmetricKeyService,
    resourceType
  ) {
    var symmetric_keysResourceType = registry.getResourceType(resourceType);
    symmetric_keysResourceType.globalActions
      .append({
        id: 'createSymmetricKeyAction',
        service: createSymmetricKeyService,
        template: {
          type: 'create',
          text: gettext('Create Symmetric Key')
        }
      });

    symmetric_keysResourceType.globalActions
      .append({
        id: 'uploadSymmetricKeyAction',
        service: uploadSymmetricKeyService,
        template: {
          type: 'create',
          text: gettext('Upload Symmetric Key')
        }
      });

    symmetric_keysResourceType.batchActions
      .append({
        id: 'batchDeleteSymmetricKeyAction',
        service: deleteSymmetricKeyService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete SymmetricKeys')
        }
      });

    symmetric_keysResourceType.itemActions
      .append({
        id: 'updateSymmetricKeyAction',
        service: updateSymmetricKeyService,
        template: {
          text: gettext('Update SymmetricKey')
        }
      })
      .append({
        id: 'deleteSymmetricKeyAction',
        service: deleteSymmetricKeyService,
        template: {
          type: 'delete',
          text: gettext('Delete SymmetricKey')
        }
      });
  }
})();
