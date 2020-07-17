#!/usr/bin/env bash

if [[ $# != 1 ]]; then
    printf "usage: %s DIR\n" $(basename "$0")
    exit 1
fi

DIR=$1
DB="uasrc"

for FILE in $DIR/*.json; do
    BASE=$(basename "$FILE")
    COLL="${BASE%.*}"
    echo "Loading $COLL"
    mongoimport --jsonArray --drop --db "$DB" --collection "$COLL" "$FILE"
done

echo "Done."
