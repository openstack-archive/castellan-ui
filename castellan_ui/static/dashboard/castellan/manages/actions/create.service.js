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
   * @name horizon.dashboard.castellan.manages.create.service
   * @description Service for the manage create modal
   */
  angular
    .module('horizon.dashboard.castellan.manages')
    .factory('horizon.dashboard.castellan.manages.create.service', createService);

  createService.$inject = [
    '$location',
    'horizon.app.core.openstack-service-api.castellan',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.toast.service',
    'horizon.dashboard.castellan.manages.events',
    'horizon.dashboard.castellan.manages.model',
    'horizon.dashboard.castellan.manages.resourceType',
    'horizon.dashboard.castellan.manages.workflow'
  ];

  function createService(
    $location, api, policy, actionResult, gettext, $qExtensions,
    toast, events, model, resourceType, workflow
  ) {

    var message = {
      success: gettext('Manage %s was successfully created.')
    };

    var service = {
      initAction: initAction,
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    // fixme: include this function in your service
    // if you plan to emit events to the parent controller,
    // otherwise remove it
    function initAction() {
    }

    // fixme: if newScope is unnecessary, remove it
    /* eslint-disable no-unused-vars */
    function perform(selected, newScope) {
      // modal title, buttons
      var title, submitText, submitIcon;
      title = gettext("Create Manage");
      submitText = gettext("Create");
      submitIcon = "fa fa-check";
      model.init();

      var result = workflow.init(title, submitText, submitIcon, model.spec);
      return result.then(submit);
    }

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
      // fixme: if you need to set policy, change as follow
      //return policy.ifAllowed({ rules: [['manage', 'create_manage']] });
    }

    function submit() {
      model.cleanProperties();
      return api.createManage(model.spec).then(success);
    }

    function success(response) {
      response.data.id = response.data.uuid;
      toast.add('success', interpolate(message.success, [response.data.id]));
      var result = actionResult.getActionResult()
                   .created(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.created.length > 0) {
        $location.path('/project/manages');
      } else {
        return result.result;
      }
    }
  }
})();