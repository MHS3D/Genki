## data send by the watch per MQTT message to the broker:
| sensor | data_unit | number_unit |
|--------|-----------|-------------|
| acceleration x | g | f32 |
| acceleration y | g | f32 |
| acceleration z | g | f32 |
| gyro x | rad/s | f32 |
| gyro y | rad/s | f32 |
| gyro z | rad/s | f32 |
| roll | angle | f32 |
| pitch | angle | f32 |
| pulse |  | f32? |

MQTT sends strings -> Daten als JSON versenden z.B.
"[{"sensor":"acceleration x","data":1.0},{"sensor":"acceleration y","data":2.0},{"sensor":"acceleration z","data":3.0},{"sensor":"roll","data":4.0},{"sensor":"pitch","data":5.0},{"sensor":"gyro x","data":6.0},{"sensor":"gyro y","data":7.0},{"sensor":"gyro z","data":8.0}]"


//in Cargo.toml (versionen?)
[dependencies]
serde_json = "1.0.117"
serde = {version = "1.0.203", features = ["derive"]}

//in main:
use serde::Serialize;

#[derive(Serialize)]
pub struct DataEntry {
    sensor: String,
    data: f32
}

        //new data_list to send
        let mut data_list: Vec<DataEntry> = Vec::new();

        //collect sensor data, need to figure out which axis is which entry in vec!!
        data_list.push(DataEntry{sensor: "acceleration x".to_string(),data: accel[0]});
        data_list.push(DataEntry{sensor: "acceleration y".to_string(),data: accel[1]});
        data_list.push(DataEntry{sensor: "acceleration z".to_string(),data: accel[2]});

        data_list.push(DataEntry{sensor: "roll".to_string(),data: accel_angles[0]});
        data_list.push(DataEntry{sensor: "pitch".to_string(),data: accel_angles[1]});

        data_list.push(DataEntry{sensor: "gyro x".to_string(),data: gyrodata[0]});
        data_list.push(DataEntry{sensor: "gyro y".to_string(),data: gyrodata[1]});
        data_list.push(DataEntry{sensor: "gyro z".to_string(),data: gyrodata[2]});

        let payload = serde_json::to_string(&data_list).unwrap();