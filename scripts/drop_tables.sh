#!/bin/bash
# Execute the SQL file
psql $DATABASE_URL -c \
"
DROP TABLE users CASCADE;
DROP TABLE openings CASCADE;
DROP TABLE anime CASCADE;
DROP TABLE access_tokens CASCADE;
"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Table dropped successfully."
else
    echo "Failed to insert data."
fi
