// Site
let version = "1.0.0";

// Server
let base;
let ip;
let port;
let token;

if (sessionStorage.getItem("base")) {
  base = sessionStorage.getItem("base");
}

if (sessionStorage.getItem("ip")) {
  ip = sessionStorage.getItem("ip");
}

if (sessionStorage.getItem("port")) {
  port = sessionStorage.getItem("port");
}

if (sessionStorage.getItem("token")) {
  token = sessionStorage.getItem("token");
}

// UI

const loginDiv = document.getElementById("login");
const loginMsg = document.getElementById("loginMsg");
const dashboard = document.getElementById("dashboard");
const consoleDiv = document.getElementById("console");
const setAbsolute = document.getElementById("setAbsolute");
const tokenInput = document.getElementById("tokenInput");
const loginBtn = document.querySelector("#login button");
