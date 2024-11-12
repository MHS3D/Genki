use std::sync::{Arc, Mutex};

#[derive(Debug, serde::Serialize, Clone)]
pub struct ThreeAxisData {
    x: f32,
    y: f32,
    z: f32,
    timestamp: f64,
}

pub(crate) type SharedDataType = Arc<Mutex<SharedData>>;

pub const MAX_DATA_POINTS: usize = 600;

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

    pub fn switch_gyro_vec(&mut self, vec: Vec<ThreeAxisData>) {
        self.gyro = vec;
    }

    pub fn add_accel(&mut self, x: f32, y: f32, z: f32, timestamp: f64) {
        if self.accel.len() >= MAX_DATA_POINTS {
            self.accel.remove(0);
        }

        self.accel.push(ThreeAxisData { x, y, z, timestamp });
    }

    pub fn add_gyro(&mut self, x: f32, y: f32, z: f32, timestamp: f64) {
        if self.gyro.len() >= MAX_DATA_POINTS {
            self.gyro.remove(0);
        }

        self.gyro.push(ThreeAxisData { x, y, z, timestamp });
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