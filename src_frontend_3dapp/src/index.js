const express = require('express');
const app = express();
const PORT = 3000;

// Den "public"-Ordner als statisches Verzeichnis festlegen, damit HTML, CSS und JS-Dateien hier aufgerufen werden können
app.use(express.static('public'));

// GET-Anfrage für die Route "/api" definieren, die JSON-Daten zurückgibt
app.get('/api', (req, res) => {
   res.json({ message: "Hello, World!" });
});

// Server starten und in der Konsole anzeigen, dass der Server läuft
app.listen(PORT, () => {
   console.log(`Server is running at http://localhost:${PORT}`);
});
