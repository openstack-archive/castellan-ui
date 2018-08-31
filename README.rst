===============================
Castellan UI
===============================

Generic Key Manager UI Plugin for Horizon

* Free software: Apache license
* Source: http://git.openstack.org/cgit/openstack/castellan-ui
* Bugs: https://storyboard.openstack.org/#!/project/openstack/castellan-ui

Features
--------

--------------------+------------------+---------------------------+---------------+-----------+--------------+
|                    | Import from file | Import using direct input | Download      | Delete    | Generate [1] |
====================+==================+===========================+===============+===========+==============+
| X.509 Certificates | supported [2]    | supported [2]             | supported [2] | supported | N/A          |
--------------------+------------------+---------------------------+---------------+-----------+--------------+
| Private Keys       | supported [2]    | supported [2]             | supported [2] | supported | supported    |
--------------------+------------------+---------------------------+---------------+-----------+--------------+
| Public Keys        | supported [2]    | supported [2]             | supported [2] | supported | supported    |
--------------------+------------------+---------------------------+---------------+-----------+--------------+
| Symmetric Keys     | supported [3]    | supported [4]             | supported [3] | supported | supported    |
--------------------+------------------+---------------------------+---------------+-----------+--------------+
| Opaque Data        | supported [3]    | supported [4]             | supported [3] | supported | N/A          |
--------------------+------------------+---------------------------+---------------+-----------+--------------+
| Passphrases [5]    | X                | supported                 | X             | supported | N/A          |
--------------------+------------------+---------------------------+---------------+-----------+--------------+

1. Key managers typically support generating keys only and do not generate
   other types of objects. Private and public keys will be generated as a key
   pair, and symmetric keys can be generated individually.
2. Supports Privacy-enhanced Electronic Mail (PEM) formatted objects.
3. Raw bytes represent the object.
4. Object bytes are represented using hex characters.
5. Because passphrases are typically not saved to files, passphrases are
   imported through a form on the web page and are not downloadable, only
   viewed through the web page.

Enabling in DevStack
--------------------

Add this repo as an external repository into your ``local.conf`` file::

    [[local|localrc]]
    enable_plugin castellan-ui https://github.com/openstack/castellan-ui

Manual Installation
-------------------

Begin by cloning the Horizon and Castellan UI repositories::

    git clone https://github.com/openstack/horizon
    git clone https://github.com/openstack/castellan-ui

Create a virtual environment and install Horizon dependencies::

    cd horizon
    virtualenv horizon_dev
    . horizon_dev/bin/activate
    pip install -r requirements.txt

Set up your ``local_settings.py`` file::

    cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

Open up the copied ``local_settings.py`` file in your preferred text
editor. You will want to customize several settings:

-  ``OPENSTACK_HOST`` should be configured with the hostname of your
   OpenStack server. Verify that the ``OPENSTACK_KEYSTONE_URL`` and
   ``OPENSTACK_KEYSTONE_DEFAULT_ROLE`` settings are correct for your
   environment. (They should be correct unless you modified your
   OpenStack server to change them.)

Install Castellan UI with all dependencies in your virtual environment::

   . horizon_dev/bin/activate
   pip install -e ../castellan-ui/

And enable it in Horizon (use full paths instead of relative paths)::

    ln -s ../castellan-ui/castellan_ui/enabled/_90_project_key_manager_panelgroup.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_91_project_key_manager_x509_certificates_panel.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_92_project_key_manager_private_key_panel.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_93_project_key_manager_public_key_panel.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_94_project_key_manager_symmetric_key_panel.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_95_project_key_manager_opaque_data_panel.py openstack_dashboard/local/enabled
    ln -s ../castellan-ui/castellan_ui/enabled/_96_project_key_manager_passphrase_panel.py openstack_dashboard/local/enabled

To run horizon with the newly enabled Castellan UI plugin run::

    python manage.py runserver -- 0.0.0.0:8080

to have the application start on port 8080 and the horizon dashboard will be
available in your browser at http://localhost:8080/

Troubleshooting Tips
--------------------

If you are using Barbican plugin for Castellan, be sure to note that Barbican
requires the 'admin' or 'creator' role be assigned to a user before the user
can list or create key manager objects. The error message that appears if this
is not the case is as follows::

    Could not list objects: Key manager error: Forbidden: Secret(s) retrieval attempt not allowed - please review your user/project privileges

To add the appropriate role for a non-admin user, use the following command (as an admin)  ::

    openstack role add --user <username> --project <project name> creator

See Also
--------

* Castellan: https://github.com/openstack/castellan
* Barbican: https://github.com/openstack/barbican
* Vault: https://github.com/hashicorp/vault
* PyKMIP: https://github.com/OpenKMIP/PyKMIP
