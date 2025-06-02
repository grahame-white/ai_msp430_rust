// This build script ensures the TI-TXT generation infrastructure is available
fn main() {
    // Just ensure the script is rebuilt if this file changes
    println!("cargo:rerun-if-changed=build.rs");
}