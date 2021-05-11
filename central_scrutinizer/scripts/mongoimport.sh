#!/usr/bin/env bash

if [[ $# != 1 ]]; then
    printf "usage: %s DIR\n" $(basename "$0")
    exit 1
fi

DIR=$1
DB="uasrc"

# Variables
VARS="$DIR/variables.json"
if [[ -f "$VARS" ]]; then
    mongoimport --jsonArray --drop --db "$DB" --collection variables "$VARS"
fi

# Measurements
# JOBS=$(mktemp)
JOBS="jobs.txt"
cat /dev/null > "$JOBS"

for FILE in $DIR/m-*.json; do
    echo "mongoimport --db $DB --collection scrutinizer $FILE" >> "$JOBS"
done

NUM=$(wc -l "$JOBS" | awk '{print $1}')

if [[ $NUM -gt 0 ]]; then
    echo "Importing $NUM measurements"
    parallel --tmpdir /data/tmp -j 8 --halt soon,fail=1 < "$JOBS"
else
    echo "No measurements?"
fi

rm "$JOBS"

echo "Done."
