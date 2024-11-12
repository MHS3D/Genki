use std::sync::{Arc, Mutex};

#[derive(Debug, serde::Serialize, Clone)]
pub struct ThreeAxisData {
    x: f32,
    y: f32,
    z: f32,
    timestamp: f64,
}

pub(crate) type SharedDataType = Arc<Mutex<SharedData>>;

pub const MAX_DATA_POINTS: usize = 300;

#[derive(Debug, serde::Serialize, Clone)]
pub struct SharedData {
    accel: Vec<ThreeAxisData>,
    gyro: Vec<ThreeAxisData>,
}

impl SharedData {
    pub fn new() -> Self {
        SharedData {
            accel: Vec::new(),
            gyro: Vec::new(),
        }
    }

    pub fn switch_acc_vec(&mut self, vec: Vec<ThreeAxisData>) {
        self.accel = vec;
    }
}

impl ThreeAxisData {
    pub fn new(x: f32, y: f32, z: f32, timestamp: f64) -> ThreeAxisData {
        ThreeAxisData {
            x,
            y,
            z,
            timestamp
        }
    }
}