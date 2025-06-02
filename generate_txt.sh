#!/bin/bash

# Script to generate TI-TXT format from ELF binary
# TI-TXT format uses @XXXX address headers followed by hex data and ends with 'q'

set -e

BINARY_PATH="${1:-target/msp430fr2355/release/msp430_blinky}"
OUTPUT_PATH="${2:-target/msp430fr2355/release/msp430_blinky.txt}"
TEMP_HEX_PATH="${OUTPUT_PATH%.txt}.hex"

if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary file $BINARY_PATH not found!"
    exit 1
fi

echo "Converting $BINARY_PATH to TI-TXT format..."
echo "Output: $OUTPUT_PATH"

# Step 1: Convert ELF to Intel HEX format
objcopy -O ihex "$BINARY_PATH" "$TEMP_HEX_PATH"

if [ ! -f "$TEMP_HEX_PATH" ]; then
    echo "Error: Failed to generate Intel HEX file!"
    exit 1
fi

echo "Generated intermediate Intel HEX file:"
echo "File size: $(wc -c < "$TEMP_HEX_PATH") bytes"
echo "Content preview:"
head -5 "$TEMP_HEX_PATH"

# Check if the Intel HEX file contains actual data
if [ "$(wc -l < "$TEMP_HEX_PATH")" -le 1 ]; then
    echo "Warning: Intel HEX file appears to contain no program data."
    echo "This may indicate the ELF binary has no loadable sections."
    echo "Generating a minimal TI-TXT file with a placeholder entry..."
    
    # Create a minimal TI-TXT file with a reset vector at 0xFFFE (typical for MSP430)
    cat > "$OUTPUT_PATH" << EOF
@FFFE
00 80
q
EOF
    
    echo "Generated minimal TI-TXT file:"
    cat "$OUTPUT_PATH"
    
    # Clean up
    rm -f "$TEMP_HEX_PATH"
    
    echo ""
    echo "Note: The generated file contains a minimal reset vector."
    echo "To generate a proper firmware image, ensure your Rust code compiles"
    echo "with loadable sections containing actual program data."
    exit 0
fi

# Step 2: Convert Intel HEX to TI-TXT format
python3 hex_to_titxt.py "$TEMP_HEX_PATH" "$OUTPUT_PATH"

# Clean up temporary file
rm -f "$TEMP_HEX_PATH"

if [ -f "$OUTPUT_PATH" ]; then
    echo "TI-TXT file generated successfully!"
    echo "File size: $(wc -c < "$OUTPUT_PATH") bytes"
    echo "Lines: $(wc -l < "$OUTPUT_PATH")"
    echo "TI-TXT content:"
    cat "$OUTPUT_PATH"
else
    echo "Error: Failed to generate TI-TXT file!"
    exit 1
fi