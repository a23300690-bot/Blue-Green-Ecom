/* api.js — Kaijudo shared API layer */
const API = '';

/* ── AUTH HELPERS ─────────────────────────────────── */
function getToken()   { return localStorage.getItem('access_token'); }
function getRefresh() { return localStorage.getItem('refresh_token'); }
function getUser()    { return JSON.parse(localStorage.getItem('user') || 'null'); }
function isAdmin()    { const u = getUser(); return u && u.rol === 'admin'; }
function isOperador() { const u = getUser(); return u && (u.rol === 'admin' || u.rol === 'operador'); }
function isLoggedIn() { return !!getToken(); }

/* ── REQUEST ──────────────────────────────────────── */
async function request(method, path, body = null, isForm = false) {
  const headers = { 'Authorization': `Bearer ${getToken()}` };
  if (!isForm) headers['Content-Type'] = 'application/json';
  const opts = { method, headers };
  if (body) opts.body = isForm ? body : JSON.stringify(body);
  let res = await fetch(API + path, opts);
  if (res.status === 401) {
    const renewed = await refreshToken();
    if (!renewed) { logout(); return null; }
    headers['Authorization'] = `Bearer ${getToken()}`;
    res = await fetch(API + path, { ...opts, headers });
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Error ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

async function refreshToken() {
  const rt = getRefresh();
  if (!rt) return false;
  try {
    const res = await fetch(API + '/auth/refresh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: rt }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    localStorage.setItem('access_token', data.access_token);
    return true;
  } catch { return false; }
}

/* ── AUTH CALLS ───────────────────────────────────── */
async function login(email, password) {
  const form = new URLSearchParams({ username: email, password });
  const res = await fetch(API + '/auth/login', {
    method: 'POST', body: form,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Credenciales inválidas');
  const data = await res.json();
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  const user = await request('GET', '/auth/me');
  localStorage.setItem('user', JSON.stringify(user));
  return user;
}

async function registro(nombre, email, password, rol = 'cliente') {
  const res = await fetch(API + '/auth/registro', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre, email, password, rol }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Error al registrar');
  return res.json();
}

function logout() {
  localStorage.clear();
  const enPages = window.location.pathname.includes('/pages/');
  window.location.href = enPages ? 'login.html' : 'pages/login.html';
}

/* ── RESOURCE APIs ────────────────────────────────── */
const Productos = {
  list:   ()       => request('GET',    '/productos/'),
  get:    (id)     => request('GET',    `/productos/${id}`),
  create: (form)   => request('POST',   '/productos/', form, true),
  update: (id, f)  => request('PUT',    `/productos/${id}`, f, true),
  delete: (id)     => request('DELETE', `/productos/${id}`),
};

const Perfiles = {
  list:   ()    => request('GET',    '/perfiles/'),
  get:    (id)  => request('GET',    `/perfiles/${id}`),
  create: (d)   => request('POST',   '/perfiles/', d),
  delete: (id)  => request('DELETE', `/perfiles/${id}`),
};

const Ordenes = {
  list:     ()   => request('GET',   isOperador() ? '/ordenes/' : '/ordenes/mis-ordenes'),
  get:      (id) => request('GET',   `/ordenes/${id}`),
  create:   (d)  => request('POST',  '/ordenes/', d),
  cancelar: (id) => request('PATCH', `/ordenes/${id}/cancelar`),
};

const Chat = {
  iniciarSesion: () => request('POST',  '/chat/sesion/anonima'),
  historial: (id)   => request('GET',   `/chat/sesion/${id}/historial`),
  sesiones:  ()     => request('GET',   '/chat/sesiones'),
  cerrar:    (id)   => request('PATCH', `/chat/sesion/${id}/cerrar`),
};

const Faq = {
  list:   ()   => request('GET',    '/faq/'),
  create: (d)  => request('POST',   '/faq/', d),
  delete: (id) => request('DELETE', `/faq/${id}`),
};

/* ── CARRITO (localStorage) ───────────────────────── */
const Carrito = {
  get()    { return JSON.parse(localStorage.getItem('carrito') || '[]'); },
  save(i)  { localStorage.setItem('carrito', JSON.stringify(i)); },
  add(producto, cantidad = 1) {
    const items = this.get();
    const idx = items.findIndex(i => i.id === producto.id);
    if (idx >= 0) items[idx].cantidad += cantidad;
    else items.push({ ...producto, cantidad });
    this.save(items);
    updateCartBadge();
  },
  remove(id) {
    this.save(this.get().filter(i => i.id !== id));
    updateCartBadge();
  },
  setQty(id, qty) {
    const items = this.get();
    const idx = items.findIndex(i => i.id === id);
    if (idx >= 0) { items[idx].cantidad = qty; this.save(items); }
    updateCartBadge();
  },
  clear()  { localStorage.removeItem('carrito'); updateCartBadge(); },
  total()  { return this.get().reduce((s, i) => s + i.precio * i.cantidad, 0); },
  count()  { return this.get().reduce((s, i) => s + i.cantidad, 0); },
};

function updateCartBadge() {
  document.querySelectorAll('.cart-count').forEach(el => {
    const n = Carrito.count();
    el.textContent = n;
    el.classList.toggle('hidden', n === 0);
  });
}

/* ── TOAST SYSTEM ─────────────────────────────────── */
function ensureToastContainer() {
  if (!document.getElementById('toast-container')) {
    const c = document.createElement('div');
    c.id = 'toast-container';
    document.body.appendChild(c);
  }
  return document.getElementById('toast-container');
}

function showToast(msg, type = 'success', duration = 3000) {
  const container = ensureToastContainer();
  const el = document.createElement('div');
  const icon = type === 'success'
    ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`
    : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
  el.className = `toast toast-${type}`;
  el.innerHTML = `${icon}<span>${msg}</span>`;
  container.appendChild(el);
  setTimeout(() => {
    el.classList.add('out');
    setTimeout(() => el.remove(), 250);
  }, duration);
}

function showAlert(msg, type = 'success', container = document.body) {
  const div = document.createElement('div');
  div.className = `alert alert-${type}`;
  div.textContent = msg;
  container.prepend(div);
  setTimeout(() => div.remove(), 3500);
}

/* ── IMAGE URL HELPER ─────────────────────────────── */
function imgSrc(url) {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return API + url;
}
