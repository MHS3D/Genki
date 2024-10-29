use std::{thread::sleep, time::Duration};

use anyhow::{bail, Result};
use esp_idf_svc::{
    eventloop::EspSystemEventLoop,
    hal::{
        delay::Delay,
        i2c::{I2c, I2cConfig, I2cDriver},
        prelude::Peripherals,
    },
    mqtt::client::*,
    sys::EspError,
};

use max3010x::{Led, Max3010x, SampleAveraging};
use mpu6050::*;

mod server;
mod wifi;

const BAUDRATE: u32 = 100;

/// This configuration is picked up at compile time by `build.rs` from the
/// file `cfg.toml`.
#[toml_cfg::toml_config]
pub struct Config {
    #[default("baguette")]
    wifi_ssid: &'static str,
    #[default("broetchen123")]
    wifi_psk: &'static str,
    #[default("mqtt://hivemq.cloud:8883")]
    mqtt_url: &'static str,
    #[default("baguette")]
    mqtt_client_id: &'static str,
    #[default("")]
    mqtt_topic: &'static str,
    #[default("baguette")]
    mqtt_username: &'static str,
    #[default("broetchen123")]
    mqtt_password: &'static str,
}

fn mqtt_create(
    url: &str,
    client_id: &str,
) -> Result<(EspMqttClient<'static>, EspMqttConnection), EspError> {
    let (mqtt_client, mqtt_conn) = EspMqttClient::new(
        url,
        &MqttClientConfiguration {
            client_id: Some(client_id),
            ..Default::default()
        },
    )?;

    Ok((mqtt_client, mqtt_conn))
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
    let sda = peripherals.pins.gpio22;
    let scl = peripherals.pins.gpio23;
    let rx = peripherals.pins.gpio17;
    let tx = peripherals.pins.gpio16;

    log::info!("Defined peripherals");

    // Init I2C
    let i2c_config = I2cConfig::new().baudrate(esp_idf_svc::hal::prelude::Hertz(BAUDRATE));
    log::info!("I2C Config: {:?}", i2c_config);

    let i2c_driver = I2cDriver::new(i2c, sda, scl, &i2c_config)?;
    log::info!("I2C Driver init");

    // Init MPU6050 Gyro
    // Only one I2C device can be initialized at a time, @TODO: proper mutex handling to have both at the same time
    let mut mpu = Mpu6050::new(i2c_driver);
    let mut delay = Delay::new_default();
    let _ = mpu.init(&mut delay);
    log::info!("MPU6050 init");

    // Init MAX3010 Pulse Oximeter
    // let mut max3010 = Max3010x::new_max30102(i2c_driver);
    // log::info!("MAX3010 init");

    // max3010.set_sample_averaging(SampleAveraging::Sa4).unwrap();
    // max3010.set_pulse_amplitude(Led::All, 15).unwrap();
    // max3010.enable_fifo_rollover().unwrap();
    // log::info!("MAX3010 config");

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

    let (mut client, mut conn) = mqtt_create(&app_config.mqtt_url, &app_config.mqtt_client_id)?;

    log::info!("MQTT Listening for messages");

    while let Ok(event) = conn.next() {
        log::info!("[Queue] Event: {}", event.payload());
    }

    log::info!("Connection closed");

    // Just to give a chance of our connection to get even the first published message
    std::thread::sleep(Duration::from_millis(500));

    let payload = "Hello from esp-mqtt-demo!";

    // server::init_server();

    // Change to heart rate mode

    //let mut heartrate = max3010.into_heart_rate().unwrap();

    // Infinite loop
    loop {
        client.enqueue("baguette", QoS::AtMostOnce, false, payload.as_bytes())?;

        log::info!("Published \"{payload}\" to topic \"baguette\"");

        let sleep_secs = 2;

        log::info!("Now sleeping for {sleep_secs}s...");
        std::thread::sleep(Duration::from_secs(sleep_secs));
        // let temperature = match max3010.read_temperature() {
        //     Ok(temp) => temp,
        //     Err(err) => {
        //         log::error!("Error reading temperature: {:?}", err);
        //         continue;
        //     }
        // };

        log::info!("Reading Accel");

        let accel = match mpu.get_acc() {
            Ok(acc) => {
                log::info!("Received Accel: {:?}", acc);
                acc
            }
            Err(err) => {
                log::error!("Error reading accelerometer: {:?}", err);
                continue;
            }
        };

        let accel_angles = match mpu.get_acc_angles() {
            Ok(angles) => {
                log::info!("Received Accel Angles: {:?}", angles);
                angles
            }
            Err(err) => {
                log::error!("Error reading accelerometer angles: {:?}", err);
                continue;
            }
        };

        let gyrodata = match mpu.get_gyro() {
            Ok(gyro) => {
                log::info!("Received Gyro: {:?}", gyro);
                gyro
            }
            Err(err) => {
                log::error!("Error reading gyroscope: {:?}", err);
                continue;
            }
        };

        //log::info!("Temperature: {}", temperature);
        // log::info!("Reading Heartrate");
        // let mut data: [u32; 4] = [0; 4];
        // let samples_read = heartrate.read_fifo(&mut data).unwrap();
        // log::info!("Temperature: {:?} | Read Samples: {}", data, samples_read);

        // // Change to oximeter mode
        // let mut oximeter = heartrate.into_oximeter().unwrap();
        // let samples_read = oximeter.read_fifo(&mut data).unwrap();
        // log::info!("Oximeter: {:?} | Read Samples: {}", data, samples_read);

        sleep(Duration::from_secs(1))
    }
}
