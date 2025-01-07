fetch('http://10.192.73.165:80')
.then(response => response.json())
.then(data => console.log(data))
.catch(err => console.log(err))