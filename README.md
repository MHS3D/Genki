# Genki

ESP32C6 based smartwatch using Rust.

## Building

Follow this guide to setup your environment: https://docs.esp-rs.org/book/installation/rust.html

Remember to switch to rust-src:

```sh
rustup toolchain install nightly --component rust-src
```

don't forget to install the `espflash` tool:

```sh
cargo install espflash
```

and `ldproxy`:

```sh
cargo install ldproxy
```

Then you can build the project:

```sh 
cargo build --release
```

and flash it to your device using:

```sh
cargo run
```