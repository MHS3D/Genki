use esp_idf_svc::{
    http::{
        server::{Configuration, EspHttpServer},
        Method,
    },
    io::{EspIOError, Write},
};

use crate::shared::SharedDataType;

pub fn init_server(shared_data: SharedDataType) -> EspHttpServer<'static> {
    log::info!("Setting up server...");

    // Set the HTTP server
    let mut server = EspHttpServer::new(&Configuration::default()).unwrap();

    log::info!("Server setup");

    // http://<sta ip>/ handler
    server
        .fn_handler(
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
        )
        .unwrap();

    server.fn_handler(
        "/info",
        Method::Get,
        |request| -> core::result::Result<(), EspIOError> {
            let body = b"Genki server running!";
            let mut response = request.into_ok_response()?;
            response.write_all(body)?;
            Ok(())
        },
    ).unwrap();

    return server;
}
