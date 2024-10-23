use esp_idf_svc::{http::{server::{Configuration, EspHttpServer}, Method}, io::{EspIOError, Write}};

pub fn init_server() {
        // Set the HTTP server
        let mut server = EspHttpServer::new(&Configuration::default()).unwrap();
        // http://<sta ip>/ handler
        server.fn_handler(
            "/",
            Method::Get,
            |request| -> core::result::Result<(), EspIOError> {
                let html = "Hello :D";
                let mut response = request.into_ok_response()?;
                response.write_all(html.as_bytes())?;
                Ok(())
            },
        ).unwrap();
}