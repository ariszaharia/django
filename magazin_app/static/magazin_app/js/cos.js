/* Cart helpers shared by the home, products and product detail pages.
   The cart lives in localStorage under "cos_virtual" as
   { "<produs_id>": { name, price, qty, stock_quantity } } — cos.html reads the same shape. */

function citesteCos() {
  try {
    var raw = localStorage.getItem('cos_virtual');
    return (raw && raw !== 'undefined') ? (JSON.parse(raw) || {}) : {};
  } catch (e) { return {}; }
}

function adaugareSimpla(id, name, price, stock_quantity) {
  var cos = citesteCos();

  if (!cos[id]) {
    cos[id] = {
      name: name,
      price: parseFloat(price),
      qty: 1,
      stock_quantity: parseInt(stock_quantity, 10)
    };
  } else if (cos[id].qty < cos[id].stock_quantity) {
    cos[id].qty += 1;
  } else {
    alert('Ai adăugat deja tot stocul disponibil pentru ' + name + '.');
    return;
  }

  localStorage.setItem('cos_virtual', JSON.stringify(cos));
  refreshBife(String(id));
  if (window.actualizeazaNrCos) window.actualizeazaNrCos();
}

function refreshBife(idNou) {
  var cos = citesteCos();
  document.querySelectorAll('.in-cos-badge').forEach(function (el) { el.hidden = true; });

  Object.keys(cos).forEach(function (id) {
    document.querySelectorAll('[data-status="' + id + '"]').forEach(function (el) {
      el.hidden = false;
      el.querySelector('.badge-qty').textContent = cos[id].qty;
      if (id === idNou) {
        el.classList.remove('puls');
        void el.offsetWidth;
        el.classList.add('puls');
      }
    });
  });
}

document.addEventListener('click', function (e) {
  var btn = e.target.closest('.adauga-cos');
  if (!btn) return;
  adaugareSimpla(btn.dataset.id, btn.dataset.name, btn.dataset.price, btn.dataset.stoc);
});

refreshBife();
