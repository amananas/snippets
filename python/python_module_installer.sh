#!/bin/bash

MODULE_NAME=
CONFIG_DIR=
CONFIG_FILE_DEFAULTS=
CONFIG_FILE_NAME=
EXEC_FILE_LOCATION=/usr/bin
EXEC_FILE_NAME=

function choice {
    if [ -z $2 ]; then
        while true; do
            echo -n "$1 (y/n) "
            read yn
            case $yn in
                [Yy]* ) return 0;;
                [Nn]* ) return 1;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    else
        $2 && indication="(Y/n)" || indication="(y/N)"
        echo -n "$1 $indication "
        read yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) $2 && return 0 || return 1;;
        esac
    fi
}

function checkRemoveConfigFile {
    if not [ -e $2 ]; then return; fi
    if not diff -q $1 $2 > /dev/null; then
        if choice "Do you want to remove your config file $2 ?" ""; then
            rm $2
            rmdir --ignore-fail-on-non-empty $CONFIG_DIR
        fi
    else
        rm $2
        rmdir --ignore-fail-on-non-empty $CONFIG_DIR
    fi
}

function checkInstallConfigFile {
    if [ -e $2 ]; then
        choice "I found an existing config file $2. Do you want to replace it with the default template ?" false || return
        rm $2
    fi
    [ -d $CONFIG_DIR ] || mkdir $CONFIG_DIR
    cp $1 $2
}

case $1 in
    "install")
        sudo -E pip3 install --process-dependency-links "." || exit 1
        location=$(pip3 show $MODULE_NAME | grep Location | sed "s/Location: //")
        checkInstallConfigFile $location/$MODULE_NAME/$CONFIG_FILE_DEFAULTS $CONFIG_DIR/$CONFIG_FILE_NAME
        sudo -E cp launch_script.sh $EXEC_FILE_LOCATION/$EXEC_FILE_NAME
        sudo -E chmod 755 $EXEC_FILE_LOCATION/$EXEC_FILE_NAME
        ;;
    "remove")
        if not pip3 show mmonitor &>/dev/null; then
            echo "mmonitor is not installed. Aborting..."
            exit 1
        fi
        location=$(pip3 show $MODULE_NAME | grep Location | sed "s/Location: //")
        checkRemoveConfigFile $location/$MODULE_NAME/$CONFIG_FILE_DEFAULTS $CONFIG_DIR/$CONFIG_FILE_NAME
        sudo -E pip3 uninstall mmonitor
    	sudo -E rm $EXEC_FILE_LOCATION/$EXEC_FILE_NAME
        ;;
    *)
        echo "Please use '$0 install' or '$0 remove'."
esac

