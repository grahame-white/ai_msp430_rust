# MSP430FR2355 Rust LED Blinky

This project demonstrates a simple LED blink application for the MSP430FR2355 microcontroller written in Rust. The project is designed to work with the MSP430FR2355 LaunchPad development board.

## Features

- LED blink functionality using P1.0 (red LED on LaunchPad)
- No-std embedded Rust implementation
- Uses official MSP430FR2355 peripheral access crate
- Custom delay implementation

## Hardware Requirements

- MSP430FR2355 LaunchPad (or compatible hardware)
- The red LED is connected to P1.0

## Software Requirements

- Rust nightly toolchain (required for MSP430 support)
- rust-src component for building core library

## Building

1. Install Rust nightly and required components:
```bash
rustup install nightly
rustup default nightly
rustup component add rust-src
```

2. Build the project:
```bash
cargo build --release
```

3. Generate TI-TXT format (optional):
```bash
# Generate TI-TXT format for use with TI programming tools
./generate_txt.sh
# or manually:
objcopy -O ihex target/msp430fr2355/release/msp430_blinky target/msp430fr2355/release/msp430_blinky.txt
```

## Project Structure

- `src/main.rs` - Main application code with LED blink logic
- `Cargo.toml` - Project dependencies and configuration
- `memory.x` - Memory layout for MSP430FR2355
- `msp430fr2355.json` - Custom target specification
- `.cargo/config.toml` - Build configuration

## Dependencies

- `msp430fr2355` - Peripheral access crate for MSP430FR2355
- `msp430-rt` - Runtime and startup code for MSP430
- `panic-msp430` - Panic handler for MSP430
- `embedded-hal` - Hardware abstraction layer
- `nb` - Non-blocking APIs

## Programming the Device

The build produces both ELF and TI-TXT formatted files that can be programmed to the device using various tools:

### Using ELF format:
- Code Composer Studio (CCS)
- MSP430 Flasher
- mspdebug (Linux)

### Using TI-TXT format:
- MSP430 programming tools that support Intel HEX format
- TI UniFlash
- Custom programming utilities

The compiled files are located at:
- ELF Binary (Debug): `target/msp430fr2355/debug/msp430_blinky`
- ELF Binary (Release): `target/msp430fr2355/release/msp430_blinky`
- TI-TXT Format: `target/msp430fr2355/release/msp430_blinky.txt`

## License

This project is licensed under the MIT License - see the LICENSE file for details.