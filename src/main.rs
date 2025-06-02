#![no_main]
#![no_std]
#![feature(asm_experimental_arch)]

use msp430fr2355 as pac;
use msp430_rt::entry;
use panic_msp430 as _;

// LED is connected to P1.0 on MSP430FR2355 LaunchPad
const LED_PIN: u8 = 0;
const BLINK_DELAY_MS: u16 = 500;

#[entry]
fn main() -> ! {
    // Get peripheral instances
    let peripherals = pac::Peripherals::take().expect("Failed to take peripherals");
    let p1 = peripherals.P1;
    let tb0 = peripherals.TB0;
    
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
        
        // Hardware-based delay
        delay_ms(BLINK_DELAY_MS, &tb0);
        
        // Turn LED off
        unsafe {
            p1.p1out.modify(|r, w| w.bits(r.bits() & !(1 << LED_PIN)));
        }
        
        // Hardware-based delay
        delay_ms(BLINK_DELAY_MS, &tb0);
    }
}

fn delay_ms(ms: u16, timer: &pac::TB0) {
    // Configure Timer_B for up mode with SMCLK source
    // TB0CTL: TBSSEL = 10 (SMCLK), MC = 01 (up mode), TBCLR = 1 (clear timer)
    unsafe {
        timer.tb0ctl.write(|w| w.bits(0x0210)); // Stop timer, clear, SMCLK
        timer.tb0ccr0.write(|w| w.bits(ms)); // Set compare value for delay
        timer.tb0ctl.write(|w| w.bits(0x0214)); // Start timer in up mode
    }
    
    // Wait for timer to reach compare value (CCIFG flag in TB0CCTL0)
    while timer.tb0cctl0.read().bits() & 0x0001 == 0 {}
    
    // Clear interrupt flag and stop timer
    unsafe {
        timer.tb0cctl0.modify(|r, w| w.bits(r.bits() & !0x0001)); // Clear CCIFG
        timer.tb0ctl.write(|w| w.bits(0x0210)); // Stop timer
    }
}
