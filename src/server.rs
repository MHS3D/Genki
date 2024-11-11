use esp_idf_svc::{http::{server::{Configuration, EspHttpServer}, Method}, io::{EspIOError, Write}};

use crate::shared::SharedDataType;

pub fn init_server(shared_data: SharedDataType) {
        // Set the HTTP server
        let mut server = EspHttpServer::new(&Configuration::default()).unwrap();
        // http://<sta ip>/ handler
        server.fn_handler(
            "/",
            Method::Get,
            move |request| -> core::result::Result<(), EspIOError> {
                let body_json = {
                    let data = shared_data.lock().unwrap();
                    serde_json::to_string(&data.clone()).unwrap()
                };
                let mut response = request.into_ok_response()?;
                response.write_all(body_json.as_bytes())?;
                Ok(())
            },
        ).unwrap();
}