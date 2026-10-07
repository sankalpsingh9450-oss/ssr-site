/* SSR Group Civil inner pages: menu, enquiry form (email via FormSubmit, WhatsApp fallback). */
(function () {
  'use strict';
  var WA = '918796138550';
  var MAIL_ENDPOINT = 'https://formsubmit.co/ajax/info@ssrgroupcivil.in';
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function waHref(text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); }
  window.SSR = { waHref: waHref, sendLead: sendLead };

  /* menu */
  var nav = $('#mobile-nav'), btn = $('#menu-btn');
  if (nav && btn) {
    var set = function (on) { nav.classList.toggle('open', on); btn.setAttribute('aria-expanded', on ? 'true' : 'false'); };
    btn.addEventListener('click', function () { set(true); });
    $('#menu-close').addEventListener('click', function () { set(false); });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }

  /* generic WhatsApp links with a page-specific opening line */
  $$('[data-wa]').forEach(function (a) { a.href = waHref(a.getAttribute('data-wa')); });

  /* lead sending: email through FormSubmit; caller handles the WhatsApp fallback */
  function sendLead(fields, subject) {
    var body = { _subject: subject || 'New enquiry from ssrgroupcivil.in', _template: 'table', _captcha: 'false' };
    Object.keys(fields).forEach(function (k) { body[k] = fields[k]; });
    body['Page'] = location.pathname;
    return fetch(MAIL_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || String(j.success) !== 'true') throw new Error(j.message || 'not sent'); return j; }); });
  }

  /* enquiry forms */
  $$('form.enq').forEach(function (form) {
    var status = $('.status', form), send = $('[data-send]', form), wa = $('[data-wa-form]', form);
    function data() {
      return {
        name: ($('[name=name]', form) || {}).value ? $('[name=name]', form).value.trim() : '',
        phone: ($('[name=phone]', form) || {}).value ? $('[name=phone]', form).value.trim() : '',
        place: ($('[name=place]', form) || {}).value ? $('[name=place]', form).value.trim() : '',
        topic: ($('[name=topic]', form) || {}).value || form.getAttribute('data-topic') || '',
        msg: ($('[name=msg]', form) || {}).value ? $('[name=msg]', form).value.trim() : ''
      };
    }
    function text(d) {
      var L = ['Hi Sankalp, I saw ssrgroupcivil.in.'];
      if (d.topic) L.push('About: ' + d.topic);
      if (d.place) L.push('Location: ' + d.place);
      if (d.msg) L.push('', d.msg);
      if (d.name || d.phone) { L.push(''); if (d.name) L.push('Name: ' + d.name); if (d.phone) L.push('Mobile: ' + d.phone); }
      return L.join('\n');
    }
    function say(msg, err) { status.hidden = false; status.textContent = msg; status.classList.toggle('err', !!err); }
    function refresh() { if (wa) wa.href = waHref(text(data())); }
    $$('input,select,textarea', form).forEach(function (el) { el.addEventListener('input', refresh); el.addEventListener('change', refresh); });
    refresh();
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = data();
      if ($('[name=_honey]', form) && $('[name=_honey]', form).value) return;
      if (!d.name || d.phone.replace(/\D/g, '').length < 10) { say('Please add your name and a 10-digit mobile number.', true); return; }
      send.disabled = true; say('Sending…');
      sendLead({ Name: d.name, Mobile: d.phone, Location: d.place, Topic: d.topic, Message: d.msg }, 'Website enquiry: ' + (d.topic || 'general'))
        .then(function () { say('Thank you, ' + d.name.split(' ')[0] + '. Your enquiry has reached SSR; we will get back to you on ' + d.phone + '.'); form.reset(); refresh(); })
        .catch(function () { say('We could not send this by email just now. Tap “WhatsApp instead” and it goes straight to Sankalp.', true); })
        .then(function () { send.disabled = false; });
    });
  });
})();
