#!/usr/bin/env bash

TEMP_INVENTORY_FILE=__temp_inv_file_remove

function log {
    echo "$1"
}

function print_help {
    log "Install Devbox 0.6"
    log "usage: sealdockercihelper [-u username] [-r remote_host] [-t] [-h]"
    log "OPTIONS:"
    log "   -u <username>        remote username"
    log "   -r <remote_host>     the hostname/ip to the remote machine"
    log "   -t                   just test the connection to the remote host"
    log "   -h                   print this help"
    log ""
    log "EXAMPLE:"
    log "   $ install_devbox -u rupert -r 192.168.5.78"
}

function check_arg {
    if [[ -z $2 ]]
    then
        log "$1 is missing"
        print_help
        exit 1
    fi
}

function test_con {
    ansible -v --user=$1 --ask-pass --inventory-file=$TEMP_INVENTORY_FILE all -a "/bin/echo ok"
}

function cleanup {
    rm $TEMP_INVENTORY_FILE
}

while getopts "u:r:th" opt; do
    case $opt in
        h)
            print_help
            exit
            ;;

        u) username=$OPTARG;;
        r) remote_host=$OPTARG;;
        t) test_connection=true;;

        \?)
            log "invalid option: -$OPTARG" >&2
            print_help
            exit 1
            ;;
        :)
            log "option -$OPTARG requires an argument." >&2
            print_help
            exit 1
            ;;
    esac
done

check_arg "username" $username
check_arg "remote_host" $remote_host

log ""
log "using:"
log "     username:    '"$username"'"
log "     remote host: '"$remote_host"'"
log ""

echo "["$remote_host"]" > $TEMP_INVENTORY_FILE
echo $remote_host >> $TEMP_INVENTORY_FILE

if [[ -n $test_connection ]]
then
    log "testing connection: $username@$remote_host"
    test_con $username
    cleanup
    exit 0
fi

log "running playbooks"
ansible-playbook -v -i "$remote_host," \
  --extra-vars="hosts=$remote_host" \
  -u $username --ask-pass --ask-sudo-pass \
  -c ssh playbooks/devbox.yml

cleanup
