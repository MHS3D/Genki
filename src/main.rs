use std::{thread::sleep, time::Duration};

use anyhow::{bail, Result};
use esp_idf_svc::{eventloop::EspSystemEventLoop, hal::{delay::Delay, i2c::{I2c, I2cConfig, I2cDriver}, prelude::Peripherals}};

use max3010x::{Led, Max3010x, SampleAveraging};
use mpu6050::*;

mod wifi;
mod server;

const BAUDRATE: u32 = 100;

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
    let i2c = peripherals.i2c0;
    let sda = peripherals.pins.gpio0;
    let scl = peripherals.pins.gpio1;
    let rx = peripherals.pins.gpio3;
    let tx = peripherals.pins.gpio4;

    // Init I2C
    let i2c_config = I2cConfig::new().baudrate(esp_idf_svc::hal::prelude::Hertz(BAUDRATE));
    let mut i2c_driver = I2cDriver::new(i2c, sda, scl, &i2c_config)?;

    // Init MPU6050 Gyro
    // Only one I2C device can be initialized at a time, @TODO: proper mutex handling to have both at the same time
    // let mut mpu = Mpu6050::new(i2c_driver);
    // let mut delay = Delay::new_default();
    // let _ = mpu.init(&mut delay);

    // Init MAX3010 Pulse Oximeter
    let mut max3010 = Max3010x::new_max30102(i2c_driver);
    max3010.set_sample_averaging(SampleAveraging::Sa4).unwrap();
    max3010.set_pulse_amplitude(Led::All, 15).unwrap();
    max3010.enable_fifo_rollover().unwrap();

    // Change to heart rate mode
    let mut heartrate = max3010.into_heart_rate().unwrap();
    let mut data: [u32; 4] = [0; 4];
    let samples_read = heartrate.read_fifo(&mut data).unwrap();
    log::info!("Temperature: {:?} | Read Samples: {}", data, samples_read);

    // Change to oximeter mode
    let mut oximeter = heartrate.into_oximeter().unwrap();
    let samples_read = oximeter.read_fifo(&mut data).unwrap();
    log::info!("Oximeter: {:?} | Read Samples: {}", data, samples_read);

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