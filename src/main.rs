use std::{thread::sleep, time::Duration};

use anyhow::{bail, Result};
use esp_idf_svc::{eventloop::EspSystemEventLoop, hal::prelude::Peripherals};

mod wifi;
mod server;

/// This configuration is picked up at compile time by `build.rs` from the
/// file `cfg.toml`.
#[toml_cfg::toml_config]
pub struct Config {
    #[default("genkiwlan")]
    wifi_ssid: &'static str,
    #[default("genkipassword")]
    wifi_psk: &'static str,
}

fn main() -> Result<()> {
        // It is necessary to call this function once. Otherwise some patches to the runtime
    // implemented by esp-idf-sys might not link properly. See https://github.com/esp-rs/esp-idf-template/issues/71
    esp_idf_svc::sys::link_patches();

    // Bind the log crate to the ESP Logging facilities
    esp_idf_svc::log::EspLogger::initialize_default();

    log::info!("Hello, world!");

    let peripherals = Peripherals::take().unwrap();
    let sysloop = EspSystemEventLoop::take()?;

    let app_config = CONFIG;
    // Connect to the Wi-Fi network
    let _wifi = match wifi::connect_wifi(
        app_config.wifi_ssid,
        app_config.wifi_psk,
        peripherals.modem,
        sysloop,
    ) {
        Ok(inner) => {
            println!("Connected to Wi-Fi network!");
            inner
        }
        Err(err) => {
            // Red!
            bail!("Could not connect to Wi-Fi network: {:?}", err)
        }
    };

    server::init_server();
    
    // Infinite loop
    loop {
        sleep(Duration::from_secs(1))
    }
}