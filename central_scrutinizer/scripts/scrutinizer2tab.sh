#!/usr/bin/env bash

DIR="scrutinizer"

mysql -B scrutinizer < sql/measurements.sql > "$DIR/scrutinizer.tsv"
mysql -B scrutinizer < sql/variables.sql > "$DIR/variables.tsv"
