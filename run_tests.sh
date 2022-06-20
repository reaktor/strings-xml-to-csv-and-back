#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(dirname "$0")"
TEST_DIR="$SCRIPT_DIR/tests/xml-to-csv"
ACTUAL_CSV="$TEST_DIR/out/actual.csv"
EXPECTED_CSV="$TEST_DIR/expected.csv"
ORIGINAL_XML="$SCRIPT_DIR/tests/xml-to-csv/in"
./strings_to_csv.py "$ACTUAL_CSV" "$ORIGINAL_XML"
diff -us "$EXPECTED_CSV" "$ACTUAL_CSV"

./csv_to_strings.py "$ACTUAL_CSV" "$SCRIPT_DIR/tests/csv-to-xml/out"
ACTUAL_XML="$SCRIPT_DIR/tests/csv-to-xml/out"
diff -us "$ORIGINAL_XML/values/strings.xml" "$ACTUAL_XML/values/strings.xml"
diff -us "$ORIGINAL_XML/values-sv/strings.xml" "$ACTUAL_XML/values-sv/strings.xml"
diff -us "$ORIGINAL_XML/values-fi/strings.xml" "$ACTUAL_XML/values-fi/strings.xml"