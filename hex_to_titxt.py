#!/usr/bin/env python3
"""
Convert Intel HEX format to TI-TXT format.

Intel HEX format uses records like:
:10C0000001234567890ABCDEF...
:00000001FF

TI-TXT format uses:
@C000
01 23 45 67 89 0A BC DE F...
q
"""

import sys
import re

def intel_hex_to_ti_txt(hex_file_path, txt_file_path):
    """Convert Intel HEX file to TI-TXT format."""
    
    # Dictionary to store address -> data mapping
    memory_data = {}
    
    try:
        with open(hex_file_path, 'r') as hex_file:
            for line_num, line in enumerate(hex_file, 1):
                line = line.strip()
                if not line:
                    continue
                    
                # Intel HEX lines start with ':'
                if not line.startswith(':'):
                    print(f"Warning: Line {line_num} doesn't start with ':' - skipping")
                    continue
                
                # Parse Intel HEX record
                # Format: :LLAAAATT[DD...]CC
                # LL = byte count, AAAA = address, TT = type, DD = data, CC = checksum
                if len(line) < 11:  # Minimum length for a valid record
                    print(f"Warning: Line {line_num} too short - skipping")
                    continue
                
                try:
                    byte_count = int(line[1:3], 16)
                    address = int(line[3:7], 16)
                    record_type = int(line[7:9], 16)
                    
                    # Type 00 = Data record, Type 01 = End of file
                    if record_type == 0x00:  # Data record
                        # Extract data bytes
                        data_start = 9
                        data_end = data_start + (byte_count * 2)
                        if data_end > len(line) - 2:  # -2 for checksum
                            print(f"Warning: Line {line_num} data length mismatch - skipping")
                            continue
                            
                        data_hex = line[data_start:data_end]
                        
                        # Convert hex string to bytes and store
                        for i in range(0, len(data_hex), 2):
                            byte_addr = address + (i // 2)
                            byte_val = int(data_hex[i:i+2], 16)
                            memory_data[byte_addr] = byte_val
                            
                    elif record_type == 0x01:  # End of file
                        break
                        
                except ValueError as e:
                    print(f"Warning: Line {line_num} parse error: {e} - skipping")
                    continue
    
    except FileNotFoundError:
        print(f"Error: Input file '{hex_file_path}' not found")
        return False
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False
    
    if not memory_data:
        print("Warning: No valid data found in Intel HEX file")
        return False
    
    # Write TI-TXT format
    try:
        with open(txt_file_path, 'w') as txt_file:
            # Sort addresses to write in order
            sorted_addresses = sorted(memory_data.keys())
            
            if not sorted_addresses:
                print("Warning: No data to write")
                return False
            
            # Group consecutive addresses
            current_addr = sorted_addresses[0]
            current_data = []
            
            for addr in sorted_addresses:
                if addr == current_addr + len(current_data):
                    # Consecutive address, add to current group
                    current_data.append(memory_data[addr])
                else:
                    # Write current group
                    if current_data:
                        txt_file.write(f"@{current_addr:04X}\n")
                        # Write data in lines of 16 bytes max
                        for i in range(0, len(current_data), 16):
                            line_data = current_data[i:i+16]
                            hex_bytes = " ".join(f"{b:02X}" for b in line_data)
                            txt_file.write(f"{hex_bytes}\n")
                    
                    # Start new group
                    current_addr = addr
                    current_data = [memory_data[addr]]
            
            # Write final group
            if current_data:
                txt_file.write(f"@{current_addr:04X}\n")
                for i in range(0, len(current_data), 16):
                    line_data = current_data[i:i+16]
                    hex_bytes = " ".join(f"{b:02X}" for b in line_data)
                    txt_file.write(f"{hex_bytes}\n")
            
            # End with 'q'
            txt_file.write("q\n")
            
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False
    
    print(f"Successfully converted {len(memory_data)} bytes from Intel HEX to TI-TXT format")
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: hex_to_titxt.py <input.hex> <output.txt>")
        print("Convert Intel HEX format to TI-TXT format")
        sys.exit(1)
    
    hex_file = sys.argv[1]
    txt_file = sys.argv[2]
    
    if intel_hex_to_ti_txt(hex_file, txt_file):
        print(f"Conversion successful: {hex_file} -> {txt_file}")
    else:
        print("Conversion failed")
        sys.exit(1)

if __name__ == "__main__":
    main()