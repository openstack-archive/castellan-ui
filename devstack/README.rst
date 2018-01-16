================================
DevStack plugin for castellan-ui
================================

This is setup as a DevStack plugin.
For more information on DevStack plugins,
see the `DevStack Plugins documentation
<https://docs.openstack.org/devstack/latest/plugins.html>`__.

How to enable castellan-ui dashboard
------------------------------------

Add this repo as an external repository into your ``local.conf`` file::

.. code-block:: none

    [[local|localrc]]
    enable_plugin castellan-ui https://github.com/openstack/castellan-ui

