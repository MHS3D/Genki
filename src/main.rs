#![feature(duration_millis_float)]

use std::{
    sync::{Arc, Mutex},
    thread::{sleep, spawn},
    time::Duration,
};

use anyhow::{bail, Result};
use esp_idf_svc::{
    eventloop::EspSystemEventLoop,
    hal::{
        delay::Delay,
        i2c::{I2cConfig, I2cDriver},
        prelude::Peripherals,
    },
    mqtt::client::*,
    sys::EspError,
};
use shared::{SharedData, ThreeAxisData, MAX_DATA_POINTS};
use shared_bus::BusManagerSimple;

use max3010x::{Led, Max3010x, SampleAveraging};
use mpu6050::*;

mod server;
mod shared;
mod timer;
mod wifi;

const BAUDRATE: u32 = 115200;

/// This configuration is picked up at compile time by `build.rs` from the
/// file `cfg.toml`.
#[toml_cfg::toml_config]
pub struct Config {
    #[default("baguette")]
    wifi_ssid: &'static str,
    #[default("broetchen123")]
    wifi_psk: &'static str,
}

const IGNORE_WIFI: bool = false;

enum SensorToUse {
    MAX3010,
    MPU6050,
}

fn main() -> Result<()> {
    // It is necessary to call this function once. Otherwise some patches to the runtime
    // implemented by esp-idf-sys might not link properly. See https://github.com/esp-rs/esp-idf-template/issues/71
    esp_idf_svc::sys::link_patches();

    // Bind the log crate to the ESP Logging facilities
    esp_idf_svc::log::EspLogger::initialize_default();

    log::info!("Hello, world!");

    // let rx = peripherals.pins.gpio17;
    // let tx = peripherals.pins.gpio16;

    log::info!("Defined peripherals");

    let shared_data = Arc::new(Mutex::new(SharedData::new()));

    log::info!("Shared Data created");

    let sysloop = EspSystemEventLoop::take()?;

    log::info!("System Event Loop taken");

    let app_config = CONFIG;
    // Connect to the Wi-Fi network
    let peripherals = Peripherals::take().unwrap();
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

    log::info!("Wifi initialized");

    // Just to give a chance of our connection to get even the first published message
    std::thread::sleep(Duration::from_millis(1000));

    log::info!("Starting Server");

    let shared_data_copy = shared_data.clone();
    let server = server::init_server(shared_data_copy);

    // Get the peripherals
    let i2c = peripherals.i2c0;
    let sda = peripherals.pins.gpio22;
    let scl = peripherals.pins.gpio23;

    // Init I2C
    let i2c_config = I2cConfig::new().baudrate(esp_idf_svc::hal::prelude::Hertz(BAUDRATE));
    log::info!("I2C Config: {:?}", i2c_config);
    let i2c_driver = I2cDriver::new(i2c, sda, scl, &i2c_config)?;
    log::info!("I2C Driver init");

    // Create a shared bus manager
    let i2c_bus = BusManagerSimple::new(i2c_driver);
    log::info!("I2C Bus Manager init");

    log::info!("Initializing Sensors");

    // let mut max3010 = Max3010x::new_max30102(i2c_bus.acquire_i2c());
    log::info!("MAX3010 init");
    // max3010.enable_fifo_rollover().unwrap();
    // let mut oximeter = max3010.into_oximeter().unwrap();
    log::info!("MAX3010 config");

    let mut mpu = Mpu6050::new(i2c_bus.acquire_i2c());
    let mut delay = Delay::new_default();
    let _ = mpu.init(&mut delay);
    log::info!("MPU6050 init");

    let mut sensor_to_use = SensorToUse::MPU6050;

    let timer = timer::Timer::new();

    loop {
        match sensor_to_use {
            SensorToUse::MAX3010 => {
                // let temperature = oximeter.read_temperature().unwrap();
                // log::info!("Temperature: {}", temperature);

                // log::info!("Reading Heartrate");
                // let mut heartrate = oximeter.into_heart_rate().unwrap();
                // let mut data: [u32; 4] = [0; 4];
                // let samples_read = heartrate.read_fifo(&mut data).unwrap();
                // log::info!("Temperature: {:?} | Read Samples: {}", data, samples_read);

                // // Change to oximeter mode
                // oximeter = heartrate.into_oximeter().unwrap();
                // let samples_read = oximeter.read_fifo(&mut data).unwrap();
                // log::info!("Oximeter: {:?} | Read Samples: {}", data, samples_read);

                sensor_to_use = SensorToUse::MPU6050;
            }
            SensorToUse::MPU6050 => {
                let accel = match mpu.get_acc() {
                    Ok(acc) => {
                        acc
                    }
                    Err(err) => {
                        log::error!("Error reading accelerometer: {:?}", err);
                        continue;
                    }
                };
                
                // let accel_angles = match mpu.get_acc_angles() {
                //     Ok(angles) => {
                //         log::info!("Received Accel Angles: {:?}", angles);
                //         angles
                //     }
                //     Err(err) => {
                //         log::error!("Error reading accelerometer angles: {:?}", err);
                //         continue;
                //     }
                // };
                // let accel_angles_timestamp = timer.elapsed();

                let gyrodata = match mpu.get_gyro() {
                    Ok(gyro) => {
                        gyro
                    }
                    Err(err) => {
                        log::error!("Error reading gyroscope: {:?}", err);
                        continue;
                    }
                };

                {
                    let mut shared_data = shared_data.lock().unwrap();
                    let timestamp = timer.elapsed();
                    shared_data.add_accel(accel.x, accel.y, accel.z, timestamp);
                    shared_data.add_gyro(gyrodata.x, gyrodata.y, gyrodata.z, timestamp);
                }

                sensor_to_use = SensorToUse::MPU6050;
            }
        }
        sleep(Duration::from_millis(100));
    }
}
