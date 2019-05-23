#!/usr/bin/env bash
set -eo pipefail
CURRENT_DIR=`dirname $BASH_SOURCE`
source $CURRENT_DIR/helpers.sh
log() { log_base "migrate" "$1" "$2"; }

APPNAME="joplin-pr-1836-migration-scrip" # for testing!

print_header "Running Database Migration"

# Manually run entrypoint script
log 0 "Migrating data for App: ${APPNAME}";
heroku run -x --app $APPNAME -- /app/docker-entrypoint.sh
