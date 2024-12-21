async function fetchMessage() {
    const response = await fetch('/api');
    const data = await response.json();
    document.getElementById('message').innerText = data.message;
 }