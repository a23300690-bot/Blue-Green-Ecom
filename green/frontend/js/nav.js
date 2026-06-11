/* nav.js — shared navigation renderer */
function renderNav() {
  const user    = getUser();
  const navAuth = document.getElementById('nav-auth');
  const navUser = document.getElementById('nav-user');
  const navAdmin = document.getElementById('nav-admin');
  const navUsername = document.getElementById('nav-username');

  if (user) {
    navAuth?.classList.add('hidden');
    if (navUser) {
      navUser.classList.remove('hidden');
      if (navUsername) navUsername.textContent = user.nombre;
    }
    if (navAdmin && isOperador()) navAdmin.classList.remove('hidden');
  } else {
    navAuth?.classList.remove('hidden');
    navUser?.classList.add('hidden');
  }
  updateCartBadge();
}

document.addEventListener('DOMContentLoaded', renderNav);
