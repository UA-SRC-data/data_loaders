#!/usr/bin/env bash

DB="uasrc"
DIR="mongoexport"
ZIP="uasrc_mongo.zip"

[[ ! -d "$DIR" ]] && mkdir -p "$DIR"
rm $DIR/*

for COLL in scrutinizer variables csm csm_variables; do
    mongoexport -d "$DB" -c "$COLL" -o "${DIR}/${COLL}.json"
done

zip -r "$ZIP" "$DIR"

echo "Done, see \"$ZIP\""
