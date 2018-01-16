# plugin.sh - DevStack plugin.sh dispatch script castellan-ui

CASTELLAN_UI_DIR=$(cd $(dirname $BASH_SOURCE)/.. && pwd)
CASTELLAN_UI_ENABLED_DIR=$CASTELLAN_UI_DIR/castellan_ui/enabled
HORIZON_ENABLED_DIR=$DEST/horizon/openstack_dashboard/local/enabled

function install_castellan_ui {
    setup_develop $CASTELLAN_UI_DIR
}

function configure_castellan_ui {
    cp -a $CASTELLAN_UI_ENABLED_DIR/_[0-9]*.py $HORIZON_ENABLED_DIR
    # NOTE: If locale directory does not exist, compilemessages will fail,
    # so check for an existence of locale directory is required.
    if [ -d $CASTELLAN_UI_DIR/castellan_ui/locale ]; then
        (cd $CASTELLAN_UI_DIR/castellan_ui; \
         DJANGO_SETTINGS_MODULE=openstack_dashboard.settings ../manage.py compilemessages)
    fi
}

# check for service enabled
if is_service_enabled castellan-ui; then

    if [[ "$1" == "stack" && "$2" == "pre-install"  ]]; then
        # Set up system services
        echo_summary "Configuring Castellan UI"
        # no-op
        :

    elif [[ "$1" == "stack" && "$2" == "install"  ]]; then
        # Perform installation of service source
        echo_summary "Installing Castellan UI"
        install_castellan_ui

    elif [[ "$1" == "stack" && "$2" == "post-config"  ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configurng Castellan UI"
        configure_castellan_ui

    elif [[ "$1" == "stack" && "$2" == "extra"  ]]; then
        # no-op
        :
    fi

    if [[ "$1" == "unstack"  ]]; then
        # Remove enabled file(s)
        for _enabled_file in $CASTELLAN_UI_ENABLED_DIR/_[0-9]*.py; do
            _enabled_basename=$(basename $_enabled_file .py)
            rm -f $HORIZON_ENABLED_DIR/${_enabled_basename}.py*
            rm -f $HORIZON_ENABLED_DIR/__pycache__/${_enabled_basename}.*pyc
        done
    fi

    if [[ "$1" == "clean"  ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi

