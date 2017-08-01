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
   * @ngdoc workflow
   * @name horizon.dashboard.castellan.manages.workflow
   * @description Service for the create/update workflow
   */
  angular
    .module('horizon.dashboard.castellan.manages')
    .factory('horizon.dashboard.castellan.manages.workflow', workflow);

  workflow.$inject = [
    'horizon.dashboard.castellan.basePath',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.widgets.form.ModalFormService'
  ];

  function workflow(basePath, gettext, modal) {
    var workflow = {
      init: init
    };

    function init(title, submitText, submitIcon, model) {
      var schema, form;

      // schema
      schema = {
        "type": "object",
        "properties": {
          "name": {
            "title": gettext("Name"),
            "type": "string"
          },
          "description": {
            "title": gettext("Description"),
            "type": "string"
          },
          "enabled": {
            "title": gettext("Enabled"),
            "type": "boolean",
            "default": true
          },
          "size": {
            "title": gettext("Size"),
            "type": "string",
            "default": "M"
          },
          "temperature": {
            "title": gettext("Temperature"),
            "type": "string",
            "default": "H"
          },
          "base": {
            "title": gettext("Base"),
            "type": "string",
            "default": ""
          },
          "flavor": {
            "title": gettext("Flavor"),
            "type": "string",
            "default": ""
          },
          "topping": {
            "title": gettext("Topping")
          }
        }
      };

      // form
      form = [
        {
          "type": "tabs",
          "tabs": [
            {
              "title": gettext("Info"),
              "help": basePath + "manages/workflow/info.help.html",
              "items": [
                {
                  "key": "name",
                  "placeholder": gettext("Name of the manage."),
                  "required": true
                },
                {
                  "key": "description",
                  "type": "textarea"
                },
                {
                  "key": "enabled",
                  "type": "checkbox"
                }
              ]
            },
            {
              "title": gettext("Recipe"),
              "help": basePath + "manages/workflow/recipe.help.html",
              "items": [
                {
                  "key": "size",
                  "type": "radiobuttons",
                  "titleMap": [
                    {"value": "S", "name": gettext("Small")},
                    {"value": "M", "name": gettext("Medium")},
                    {"value": "L", "name": gettext("Large")},
                    {"value": "XL", "name": gettext("Extra Large")}
                  ]
                },
                {
                  "key": "temperature",
                  "type": "radiobuttons",
                  "titleMap": [
                    {"value": "H", "name": gettext("Hot")},
                    {"value": "I", "name": gettext("Ice")}
                  ]
                },
                {
                  "key": "base",
                  "type": "select",
                  "titleMap": [
                    {"value": "", "name": gettext("Choose base.")},
                    {
                      "value": "blend",
                      "name": gettext("House Blend"),
                      "group": gettext("Coffee")
                    },
                    {
                      "value": "mandheling",
                      "name": gettext("Mandheling"),
                      "group": gettext("Coffee")},
                    {
                      "value": "colombia",
                      "name": gettext("Colombia"),
                      "group": gettext("Coffee")
                    },
                    {
                      "value": "espresso",
                      "name": gettext("Espresso"),
                      "group": gettext("Coffee")
                    },
                    {
                      "value": "earl_gray",
                      "name": gettext("Earl Gray"),
                      "group": gettext("Tea")
                    },
                    {
                      "value": "darjeeling",
                      "name": gettext("Darjeeling"),
                      "group": gettext("Tea")},
                    {
                      "value": "orange_pekoe",
                      "name": gettext("Orange Pekoe"),
                      "group": gettext("Tea")
                    }
                  ]
                },
                {
                  "key": "flavor",
                  "type": "select",
                  "titleMap": [
                    {"value": "", "name": gettext("Choose flavor.")},
                    {"value": "chocolate", "name": gettext("Chocolate")},
                    {"value": "mocha", "name": gettext("Mocha")},
                    {"value": "strawberry", "name": gettext("Strawberry")},
                    {"value": "blueberry", "name": gettext("Blueberry")},
                    {"value": "raspberry", "name": gettext("Raspberry")}
                  ]
                },
                {
                  "key": "topping",
                  "type": "checkboxes",
                  "titleMap": [
                    {"value": "clushed_nuts", "name": gettext("Clushed Nuts")},
                    {"value": "whip_cream", "name": gettext("Whip Cream")},
                    {"value": "mixed_serial", "name": gettext("Mixed Serial")}
                  ]
                }
              ] // items
            } // tab
          ] // tabs
        }
      ]; // form

      var config = {
        "title": title,
        "submitText": submitText,
        "schema": schema,
        "form": form,
        "model": model
      };

      return modal.open(config);
    }

    return workflow;
  }
})();
