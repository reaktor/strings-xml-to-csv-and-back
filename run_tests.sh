#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$0")"
TEST_DIR="$SCRIPT_DIR/tests/xml-to-csv"
OUT="$TEST_DIR/out/actual.csv"
EXPECTED="$TEST_DIR/expected.csv"
./strings_to_csv.py "$OUT" "$SCRIPT_DIR/tests/xml-to-csv/in"
diff -s "$EXPECTED" "$OUT" && echo "Success" || echo "Failed, see diff above"