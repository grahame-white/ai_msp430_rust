#![no_main]
#![no_std]
#![feature(asm_experimental_arch)]

use msp430fr2355 as pac;
use msp430_rt::entry;
use panic_msp430 as _;

// LED is connected to P1.0 on MSP430FR2355 LaunchPad
const LED_PIN: u8 = 0;

#[entry]
fn main() -> ! {
    // Get peripheral instances
    let peripherals = unsafe { pac::Peripherals::steal() };
    let p1 = peripherals.P1;
    
    // Configure P1.0 as output (LED)
    unsafe {
        p1.p1dir.write(|w| w.bits(1 << LED_PIN));
        p1.p1out.write(|w| w.bits(0)); // Start with LED off
    }
    
    // Main loop - blink LED
    loop {
        // Turn LED on
        unsafe {
            p1.p1out.modify(|r, w| w.bits(r.bits() | (1 << LED_PIN)));
        }
        
        // Simple delay
        delay_cycles(100_000);
        
        // Turn LED off
        unsafe {
            p1.p1out.modify(|r, w| w.bits(r.bits() & !(1 << LED_PIN)));
        }
        
        // Simple delay
        delay_cycles(100_000);
    }
}

fn delay_cycles(cycles: u32) {
    for _ in 0..cycles {
        unsafe {
            core::arch::asm!("nop");
        }
    }
}
