#!/usr/bin/env bash

DIR="scrutinizer"

[[ ! -d "$DIR" ]] && mkdir -p "$DIR"

mysql -B scrutinizer < ../sql/measurements.sql > "$DIR/scrutinizer.tsv"
mysql -B scrutinizer < ../sql/variables.sql > "$DIR/variables.tsv"
