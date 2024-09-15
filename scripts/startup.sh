#!/bin/sh
set -e

# Execute scripts
/app/scripts/drop_tables.sh
/app/scripts/create_tables.sh
/app/scripts/insert_openings.sh

# Run the command provided by CMD
exec "$@"
