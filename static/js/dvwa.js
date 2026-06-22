/* DVWA Brute Force Lab — Frontend JS */

/* ── Tab Switching ── */
function showTab(tabId, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active-tab'));
  document.getElementById(tabId).classList.add('active');
  btn.classList.add('active-tab');
}

/* ── Live GET URL preview as user types ── */
function updateUrlPreview() {
  const username = document.getElementById('username');
  const password = document.getElementById('password');
  const box      = document.getElementById('request-url-box');
  const display  = document.getElementById('url-display-text');

  if (!username || !password || !box || !display) return;

  const u = encodeURIComponent(username.value);
  const p = encodeURIComponent(password.value);
  const base = window.location.origin + '/vulnerabilities/brute/';

  if (username.value || password.value) {
    display.textContent = `${base}?username=${u}&password=${p}&Login=Login`;
    box.style.display = 'block';
  } else {
    box.style.display = 'none';
  }
}

/* ── Attach live preview listeners on DOM ready ── */
document.addEventListener('DOMContentLoaded', () => {
  const u = document.getElementById('username');
  const p = document.getElementById('password');
  if (u) u.addEventListener('input', updateUrlPreview);
  if (p) p.addEventListener('input', updateUrlPreview);

  /* If the page loaded with values (e.g. after a failed attempt), show preview */
  updateUrlPreview();
});

/* ── Called by form onsubmit to ensure the URL box is visible before redirect ── */
function showGetUrl() {
  updateUrlPreview();
  /* Let the GET request proceed naturally — no preventDefault */
  return true;
}
