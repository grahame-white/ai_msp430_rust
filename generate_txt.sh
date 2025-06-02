#!/bin/bash

# Script to generate TI-TXT format from ELF binary
# TI-TXT is essentially Intel HEX format that TI tools can read

set -e

BINARY_PATH="${1:-target/msp430fr2355/release/msp430_blinky}"
OUTPUT_PATH="${2:-target/msp430fr2355/release/msp430_blinky.txt}"

if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary file $BINARY_PATH not found!"
    exit 1
fi

echo "Converting $BINARY_PATH to TI-TXT format..."
echo "Output: $OUTPUT_PATH"

# Convert ELF to Intel HEX format (TI-TXT format)
objcopy -O ihex "$BINARY_PATH" "$OUTPUT_PATH"

if [ -f "$OUTPUT_PATH" ]; then
    echo "TI-TXT file generated successfully!"
    echo "File size: $(wc -c < "$OUTPUT_PATH") bytes"
    echo "Lines: $(wc -l < "$OUTPUT_PATH")"
else
    echo "Error: Failed to generate TI-TXT file!"
    exit 1
fi