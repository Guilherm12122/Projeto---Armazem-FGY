var XMLHttpRequest = require('xhr2');
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://127.0.0.1:5000/produtos");
xhr.setRequestHeader("Content-type", "application/json");
xhr.send();
xhr.responseType = 'json';
console.log(xhr);
  
/*
var XMLHttpRequest = require('xhr2')
const Http = new XMLHttpRequest();
const url='http://127.0.0.1:5000/produtos';
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
  console.log(Http.responseText)
}
*/