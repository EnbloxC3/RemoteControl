// Server
function connectServer(param_ip, param_port) {
  const url = `http://${param_ip}:${param_port}`;
  return fetch(`${url}/`)
    .then((res) => {
      return res;
    })
    .catch((err) => {
      return err;
    });
}

function disconnectServer() {
  base = ip = port = token = undefined;
  clearSS();
  return true;
}

function requestForServer(endpoint) {
  const server = sessionStorage.getItem("base");
  if (!server) throw new Error("No connected server!");

  const state = {
    method: "GET",
    headers: {},
    body: null,
    query: new URLSearchParams(),
    timeout: 10000,
    useCache: true,
    onSuccessCallback: null,
    onErrorCallback: null,

    setMethod(method) {
      state.method = method.toUpperCase();
      return state;
    },

    addHeader(key, value) {
      state.headers[key] = value;
      return state;
    },

    setBody(data) {
      state.body = typeof data === "string" ? data : JSON.stringify(data);
      if (!state.headers["Content-Type"]) {
        state.headers["Content-Type"] = "application/json";
      }
      return state;
    },

    addQuery(key, value) {
      state.query.append(key, value);
      return state;
    },

    setQuery(obj) {
      Object.entries(obj).forEach(([k, v]) => state.query.set(k, v));
      return state;
    },

    setTimeout(ms) {
      state.timeout = ms;
      return state;
    },

    cache(bool) {
      state.useCache = !!bool;
      return state;
    },

    onSuccess(callback) {
      state.onSuccessCallback = callback;
      return state;
    },

    onError(callback) {
      state.onErrorCallback = callback;
      return state;
    },

    send() {
      const url = `${server}${endpoint}?${state.query.toString()}`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), state.timeout);

      fetch(url, {
        method: state.method,
        headers: state.headers,
        body: ["GET", "HEAD"].includes(state.method) ? null : state.body,
        cache: state.useCache ? "default" : "no-store",
        signal: controller.signal,
      })
        .then(async (res) => {
          clearTimeout(timeoutId);
          state.onSuccessCallback?.(res);
        })
        .catch((err) => {
          clearTimeout(timeoutId);
          state.onErrorCallback?.(err);
        });

      return state;
    },
  };

  return state;
}

function authRequest(endpoint) {
  return requestForServer(endpoint).addHeader(
    "Authorization",
    `Bearer ${token}`
  );
}

function remoteSend(endpoint) {
  return authRequest(endpoint);
}

// Console

function logConsole(message, type = "success") {
  const console = consoleDiv.querySelector(".content");
  const p = document.createElement("p");
  p.textContent = message;
  p.className = type;
  console.appendChild(p);
  console.scrollTop = console.scrollHeight;
  if (console.children.length > 100) {
    console.removeChild(console.children[0]);
  }
}

(function () {
  const consoleContainer = consoleDiv.querySelector(".content");
  if (!consoleContainer) return;

  const original = { ...console };
  const proxy = new Proxy(console, {
    get(_, method) {
      return function (...args) {
        const message = args.join(" ");
        logConsole(
          message,
          method === "error"
            ? "error"
            : method === "warn"
            ? "warning"
            : "success"
        );
        return original[method]?.apply(console, args);
      };
    },
  });
  window.console = proxy;
})();

// UI

function createModal(
  title,
  innerHTML = "",
  id = Math.random().toString(),
  canClose = true
) {
  const modal = document.createElement("div");
  modal.className = "modal hidden";
  modal.id = id;

  const content = document.createElement("div");
  content.className = `modal-content`;
  content.innerHTML = `<h2>${title}</h2>${innerHTML}`;

  const closeBtn = document.createElement("span");
  closeBtn.className = "close";
  closeBtn.textContent = "×";
  closeBtn.onclick = () => {
    removeModal(id);
  };

  if (canClose) content.appendChild(closeBtn);
  modal.appendChild(content);
  document.body.appendChild(modal);
  setTimeout(() => modal.classList.remove("hidden"), 100);
  return modal;
}

function getModal(id) {
  return document.querySelector(`#${id}.modal`);
}

function removeModal(id) {
  const modal = document.getElementById(id);
  modal.classList.add("hidden");
  setTimeout(() => {
    document.body.removeChild(modal);
  }, 100);
}

function showBubble(text, type = "info") {
  const el = document.createElement("div");
  el.className = `rounded bubble ${type}`;
  el.textContent = text;
  el.style.opacity = "0";
  document.body.appendChild(el);
  setTimeout(() => (el.style.opacity = "1"), 100);
  setTimeout(() => document.body.removeChild(el), 3000);
}

// UI - Session

function temporarilyDisableLogin(seconds) {
  tokenInput.disabled = true;
  loginBtn.disabled = true;

  let remaining = seconds;
  loginMsg.textContent = `Too many retries, please wait ${remaining} seconds.`;

  const interval = setInterval(() => {
    remaining--;
    loginMsg.textContent = `Too many retries, please wait ${remaining} seconds.`;
    if (remaining <= 0) {
      clearInterval(interval);
      tokenInput.disabled = false;
      loginBtn.disabled = false;
      loginMsg.textContent = "";
    }
  }, 1000);
}

function login(param_token) {
  let result;
  requestForServer("/check_token")
    .addHeader("Authorization", `Bearer ${param_token}`)
    .onSuccess((data) => {
      result = data;
    })
    .onError((err) => {
      result = { status: -1, error: err.message };
    })
    .send();

  if (result.status === 200) {
    token = param_token;
    updateSS();
    loginMsg.textContent = "";
    loginDiv.style.display = "none";
    dashboard.style.display = "block";
    console.log("Logged in successfully");
  } else if (result.status === 401) {
    loginMsg.textContent = "Invalid token";
  } else if (result.status === 429) {
    loginMsg.textContent = "Too many attempts";
  } else if (result.status === 423) {
    temporarilyDisableLogin(result.headers.get("Retry-After"));
  } else if (result.status === 403) {
    loginMsg.textContent = "Banned!";
    tokenInput.disabled = true;
    loginBtn.disabled = true;
  } else if (result.status === 500) {
    loginMsg.textContent = "Server error";
  } else if (result.status === -1) {
    loginMsg.textContent = "Connection error: " + result.error;
  } else {
    loginMsg.textContent = "Unknown status: " + result.status;
  }
}

// Session

function updateSS() {
  if (base) sessionStorage.setItem("base", base);
  if (ip) sessionStorage.setItem("ip", ip);
  if (port) sessionStorage.setItem("port", port);
  if (token) sessionStorage.setItem("token", token);
}

function clearSS() {
  sessionStorage.clear();
}
