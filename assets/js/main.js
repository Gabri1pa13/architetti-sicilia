(function(){
  const byId = (id)=>document.getElementById(id);

  function escapeHtml(s){
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function linkifyStudio4e(s){
    return escapeHtml(String(s)).replace(/\bStudio\s*4\s*[eE]\b/g, `<a class="studio4e-inline-link" href="${STUDIO_URL}">Studio 4e</a>`);
  }

  // Site search (IT + EN)
  const searchBtn = byId('site-search-btn');
  const modal = byId('site-search-modal');
  const input = byId('site-search-input');
  const results = byId('site-search-results');
  const closeBtn = byId('site-search-close');

  const searchState = { loaded:false, items:[] };

  function openSearch(){
    if(!modal) return;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden','false');
    setTimeout(()=>{ if(input) input.focus(); }, 10);
    if(!searchState.loaded) loadSearchIndex();
  }
  function closeSearch(){
    if(!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden','true');
  }

  function normalize(str){ return (str||'').toLowerCase().trim(); }

  function escapeHtml(s){
    return (s||'').replace(/[&<>"]/g, (c)=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c]));
  }

  function renderResults(q){
    if(!results) return;
    const qq = normalize(q);
    if(!qq){
      results.innerHTML = '';
      return;
    }
    const hits = searchState.items.filter(it=>{
      const t = normalize(it.title);
      const e = normalize(it.excerpt);
      const p = normalize(it.province||'');
      const c = normalize(it.categoryLabel||it.category||'');
      return t.includes(qq) || e.includes(qq) || p.includes(qq) || c.includes(qq);
    }).slice(0, 24);

    results.innerHTML = hits.map(it=>{
      const area = it.province ? it.province : (it.lang==='en' ? 'Sicily' : 'Sicilia');
      const topic = it.categoryLabel || it.category || '';
      const badge = it.lang==='en' ? '<span class="site-search-badge">EN</span>' : '<span class="site-search-badge">IT</span>';
      return `
        <a class="site-search-item" href="${it.url}">
          <div class="k">${escapeHtml(area)} • ${escapeHtml(topic)} ${badge}</div>
          <h4>${escapeHtml(it.title)}</h4>
          <p>${escapeHtml(it.excerpt||'')}</p>
        </a>
      `;
    }).join('') || `<div class="notice">Nessun risultato.</div>`;
  }

  function loadJson(url, lang){
    return fetch(url, {cache:'no-cache'})
      .then(r=>r.ok ? r.json() : [])
      .then(arr => (Array.isArray(arr) ? arr.map(x=>({ ...x, lang })) : []))
      .catch(()=>[]);
  }

  function loadSearchIndex(){
    Promise.all([loadJson('/guides_it.json','it'), loadJson('/guides_en.json','en')])
      .then(([it,en])=>{
        searchState.items = [...it, ...en].filter(x=>x && x.title && x.url);
        searchState.loaded = true;
      });
  }

  if(searchBtn) searchBtn.addEventListener('click', openSearch);
  if(closeBtn) closeBtn.addEventListener('click', closeSearch);
  if(modal){
    modal.addEventListener('click', (e)=>{
      const t = e.target;
      if(t && t.dataset && t.dataset.close) closeSearch();
    });
    document.addEventListener('keydown', (e)=>{
      if(e.key==='Escape' && modal.classList.contains('open')) closeSearch();
    });
  }
  if(input){
    input.addEventListener('input', (e)=>renderResults(e.target.value));
  }

  // Guide Explorer
  const mount = byId('guide-explorer');
  if(!mount) return;

  const lang = mount.dataset.lang || 'it';
  const dataUrl = mount.dataset.json || (lang==='en' ? '/guides_en.json' : '/guides_it.json');

  const state = { q:'', province:'', category:'', page:1, perPage:12, items:[] };

  function render(){
    const q = normalize(state.q);
    const prov = normalize(state.province);
    const cat = normalize(state.category);

    let items = state.items.filter(it=>{
      const hitQ = !q || normalize(it.title).includes(q) || normalize(it.excerpt).includes(q);
      const hitP = !prov || normalize(it.province||'') === prov;
      const hitC = !cat || normalize(it.categoryLabel||it.category||'') === cat;
      return hitQ && hitP && hitC;
    });

    const total = items.length;
    const pages = Math.max(1, Math.ceil(total/state.perPage));
    state.page = Math.min(state.page, pages);

    const start = (state.page-1)*state.perPage;
    const slice = items.slice(start, start+state.perPage);

    byId('ge-count').textContent = total.toLocaleString('it-IT') + (lang==='en' ? ' articles' : ' articoli');
    const grid = byId('ge-grid');
    grid.innerHTML = slice.map(it=>{
      return `
        <a class="card" href="${it.url}">
          <div class="kicker">${it.province ? it.province : (lang==='en'?'Sicily':'Sicilia')} • ${it.categoryLabel || it.category}</div>
          <h3>${it.title}</h3>
          <p>${linkifyStudio4e(it.excerpt)}</p>
        </a>
      `;
    }).join('');

    const pager = byId('ge-pager');
    pager.innerHTML = `
      <div class="links">
        <button class="btn secondary" ${state.page<=1?'disabled':''} id="ge-prev">${lang==='en'?'Previous':'Indietro'}</button>
        <span class="pill">${lang==='en'?'Page':'Pagina'} ${state.page} / ${pages}</span>
        <button class="btn secondary" ${state.page>=pages?'disabled':''} id="ge-next">${lang==='en'?'Next':'Avanti'}</button>
      </div>
    `;
    const prev = byId('ge-prev'), next = byId('ge-next');
    if(prev) prev.onclick=()=>{ state.page=Math.max(1,state.page-1); render(); window.scrollTo({top:mount.offsetTop-10,behavior:'smooth'}); };
    if(next) next.onclick=()=>{ state.page=Math.min(pages,state.page+1); render(); window.scrollTo({top:mount.offsetTop-10,behavior:'smooth'}); };
  }

  function fillSelect(id, values, placeholder){
    const sel = byId(id);
    if(!sel) return;
    sel.innerHTML = `<option value="">${placeholder}</option>` + values.map(v=>`<option value="${v}">${v}</option>`).join('');
  }

  fetch(dataUrl).then(r=>r.json()).then(data=>{
    state.items = Array.isArray(data) ? data : [];

    const provinces = Array.from(new Set(state.items.map(x=>x.province).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
    const categories = Array.from(new Set(state.items.map(x=>(x.categoryLabel||x.category)).filter(Boolean))).sort((a,b)=>a.localeCompare(b));

    fillSelect('ge-province', provinces, lang==='en'?'All areas':'Tutte le province');
    fillSelect('ge-category', categories, lang==='en'?'All topics':'Tutti i temi');

    const qEl = byId('ge-q');
    if(qEl) qEl.addEventListener('input', e=>{ state.q=e.target.value; state.page=1; render(); });
    const pEl = byId('ge-province');
    if(pEl) pEl.addEventListener('change', e=>{ state.province=e.target.value; state.page=1; render(); });
    const cEl = byId('ge-category');
    if(cEl) cEl.addEventListener('change', e=>{ state.category=e.target.value; state.page=1; render(); });

    render();
  }).catch(err=>{
    mount.innerHTML = `<div class="notice">Errore nel caricamento. Riprova più tardi.</div>`;
    console.error(err);
  });

  // ------------------------------
  // UI enhancements (nav + motion)
  // ------------------------------
  function setupNavToggle(){
    const navInner = document.querySelector('.nav .nav-inner');
    const menu = document.querySelector('.nav .menu');
    if(!navInner || !menu) return;

    // Inject toggle only once
    if(navInner.querySelector('.nav-toggle')) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'nav-toggle';
    btn.setAttribute('aria-label','Apri menu');
    btn.setAttribute('aria-expanded','false');
    btn.innerHTML = '<span class="bars" aria-hidden="true"><span></span><span></span><span></span></span><span>Menu</span>';

    // Place toggle before menu
    navInner.insertBefore(btn, menu);

    function close(){
      document.body.classList.remove('nav-open');
      btn.setAttribute('aria-expanded','false');
    }
    function toggle(){
      const open = document.body.classList.toggle('nav-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    btn.addEventListener('click', toggle);

    // Close when clicking a link (mobile)
    menu.addEventListener('click', (e)=>{
      const a = e.target && e.target.closest && e.target.closest('a');
      if(a) close();
    });

    // Close on Escape
    document.addEventListener('keydown', (e)=>{
      if(e.key === 'Escape') close();
    });

    // Close when resizing up
    window.addEventListener('resize', ()=>{
      if(window.innerWidth > 900) close();
    }, { passive:true });
  }

  function setupNavScrollState(){
    const nav = document.querySelector('.nav');
    if(!nav) return;
    const onScroll = ()=>{
      if(window.scrollY > 8) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive:true });
  }

  function setupRevealOnScroll(){
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const weights = { hero:4, section:3, list:2, subtle:1 };
    const bucket = new Map();

    function addAll(selector, variant){
      document.querySelectorAll(selector).forEach(el=>{
        if(!el || el.classList.contains('reveal')) return;
        const current = bucket.get(el);
        if(!current || weights[variant] > weights[current]) bucket.set(el, variant);
      });
    }

    // Hero: strongest
    addAll('main .hero', 'hero');
    addAll('main h1', 'hero');
    addAll('main .hero .hero-card', 'hero');
    addAll('main .hero-media', 'hero');

    // Sections: medium
    addAll('main h2', 'section');
    addAll('main section', 'section');
    addAll('main .grid > *', 'section');
    addAll('main .card', 'section');
    addAll('main .panel', 'section');
    addAll('main .tile', 'section');
    addAll('main .kpi', 'section');
    addAll('main .chips a', 'section');
    addAll('main .cta', 'section');
    addAll('main .article img', 'section');
    addAll('main .article figure', 'section');

    // Subtle: long text + footer
    addAll('main .article .breadcrumb', 'subtle');
    addAll('main .article .lede', 'subtle');
    addAll('main .article p', 'subtle');
    addAll('main .article ul', 'subtle');
    addAll('main .article ol', 'subtle');
    addAll('main .article blockquote', 'subtle');
    addAll('main .article .notice', 'subtle');
    addAll('main .article .phone-cta', 'subtle');
    addAll('footer .container', 'subtle');

    // Lists: ultra-soft for scan-heavy areas
    addAll('main .links > *', 'list');
    addAll('main .links a', 'list');

    let i = 0;
    bucket.forEach((variant, el)=>{
      el.classList.add('reveal', `reveal--${variant}`);
      const d = i % 4;
      if(d === 1) el.classList.add('delay-1');
      if(d === 2) el.classList.add('delay-2');
      if(d === 3) el.classList.add('delay-3');
      i++;
    });

    const io = new IntersectionObserver((entries)=>{
      entries.forEach(entry=>{
        if(entry.isIntersecting){
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { root:null, threshold:0.12, rootMargin:'0px 0px -8% 0px' });

    bucket.forEach((_, el)=>io.observe(el));
  }

  function setupMediaParallax(){
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if(!window.matchMedia || !window.matchMedia('(min-width: 920px)').matches) return;

    const path = window.location.pathname || '/';
    const allow = path === '/' || path === '/index.html' || path.startsWith('/servizi');
    if(!allow) return;

    const imgs = Array.from(document.querySelectorAll('.media-strip .media-tile img'));
    if(!imgs.length) return;

    const strengths = imgs.map((_, i)=>{
      const phase = (i % 4) - 1.5;
      return phase * 0.6;
    });

    let ticking = false;
    function update(){
      ticking = false;
      const vh = window.innerHeight || 800;
      imgs.forEach((img, i)=>{
        const rect = img.getBoundingClientRect();
        const mid = rect.top + rect.height * 0.5;
        const offset = (mid - vh * 0.5) / vh;
        const y = Math.max(-8, Math.min(8, offset * strengths[i] * 10));
        img.style.setProperty('--parallax-y', y.toFixed(2) + 'px');
      });
    }
    function onScroll(){
      if(!ticking){
        ticking = true;
        window.requestAnimationFrame(update);
      }
    }

    update();
    window.addEventListener('scroll', onScroll, { passive:true });
    window.addEventListener('resize', onScroll, { passive:true });
  }

  function improveImages(){
    // Lazy-load non-critical images for performance (SEO friendly)
    document.querySelectorAll('img').forEach((img)=>{
      if(!img.getAttribute('loading')) img.setAttribute('loading','lazy');
      if(!img.getAttribute('decoding')) img.setAttribute('decoding','async');
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    if(!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)){
      document.documentElement.classList.add('motion-ready');
    }
    setupNavToggle();
    setupNavScrollState();
    setupRevealOnScroll();
    setupMediaParallax();
    improveImages();
  });


  // Start form: send via Email
  const startForm = byId('start-form');
  if(startForm){
    const emailBtn = startForm.querySelector('.email-submit');
    if(emailBtn){
      emailBtn.addEventListener('click', ()=>{
        const get = (name)=> (startForm.querySelector(`[name="${name}"]`)?.value || '').trim();
        const payload = {
          obiettivo:get('obiettivo'),
          luogo:get('luogo'),
          immobile:get('immobile'),
          tempi:get('tempi'),
          documenti:get('documenti'),
          note:get('note')
        };
        const subject = encodeURIComponent('Richiesta contatto — Architetti Sicilia');
        const lines = [
          'Obiettivo: ' + (payload.obiettivo || '-'),
          'Luogo: ' + (payload.luogo || '-'),
          'Immobile: ' + (payload.immobile || '-'),
          'Tempi: ' + (payload.tempi || '-'),
          'Documenti: ' + (payload.documenti || '-'),
          '',
          'Note:',
          payload.note || '-'
        ];
        const body = encodeURIComponent(lines.join('\n'));
        window.location.href = `mailto:info@studio4e.it?subject=${subject}&body=${body}`;
      });
    }
  }


  // Contact FAB behavior: close on outside click / ESC
  (function(){
    const fab = document.getElementById('contactFab');
    if(!fab) return;
    document.addEventListener('click', (e)=>{
      if(!fab.hasAttribute('open')) return;
      if(fab.contains(e.target)) return;
      fab.removeAttribute('open');
    }, true);
    document.addEventListener('keydown', (e)=>{
      if(e.key === 'Escape' && fab.hasAttribute('open')){
        fab.removeAttribute('open');
      }
    });
  })();
})();



/* Contact form actions: WhatsApp + Email (inizia-da-qui) */
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function safeVal(el) { return el ? String(el.value || '').trim() : ''; }

  function buildContactMessage(form) {
    var fields = [
      ['Nome', safeVal(qs('[name="nome"]', form))],
      ['Telefono', safeVal(qs('[name="telefono"]', form))],
      ['Email', safeVal(qs('[name="email"]', form))],
      ['Città/Provincia', safeVal(qs('[name="citta"]', form))],
      ['Tipologia immobile', safeVal(qs('[name="tipologia"]', form))],
      ['Intervento richiesto', safeVal(qs('[name="intervento"]', form))],
      ['Tempistiche', safeVal(qs('[name="tempistiche"]', form))],
      ['Budget indicativo', safeVal(qs('[name="budget"]', form))],
      ['Documenti disponibili', safeVal(qs('[name="documenti"]', form))],
      ['Note', safeVal(qs('[name="note"]', form))]
    ];

    var lines = ['Richiesta dal sito Architetti Sicilia (Inizia da qui)'];
    for (var i = 0; i < fields.length; i++) {
      if (fields[i][1]) lines.push(fields[i][0] + ': ' + fields[i][1]);
    }
    return lines.join('\n');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var waBtn = document.getElementById('send-whatsapp');
    if (!waBtn) return;

    var form = waBtn.closest('form') || document.querySelector('form');
    var phone = '393299736697'; // Studio 4e WhatsApp (international format, no +)

    waBtn.addEventListener('click', function (e) {
      try {
        var msg = form ? buildContactMessage(form) : 'Richiesta dal sito Architetti Sicilia';
        var url = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(msg);
        // Try new tab first (best UX on desktop); fallback to same tab.
        var win = window.open(url, '_blank', 'noopener,noreferrer');
        if (!win) window.location.href = url;
      } catch (err) {
        // Absolute fallback
        window.location.href = 'https://wa.me/' + phone;
      }
    });

    var emailBtn = document.getElementById('send-email');
    if (emailBtn && form) {
      // Add body prefill (keeps existing href subject if present)
      emailBtn.addEventListener('click', function () {
        try {
          var msg = buildContactMessage(form);
          var base = 'mailto:info@studio4e.it';
          var subject = 'Richiesta dal sito Architetti Sicilia';
          var href = base + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(msg);
          emailBtn.setAttribute('href', href);
        } catch (e) {}
      });
    }
  });
})();


// --- reveal on scroll (no content changes) ---
(() => {
  const els = Array.from(document.querySelectorAll('.reveal'));
  if (!els.length) return;

  const show = (el) => el.classList.add('is-visible');

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          show(e.target);
          io.unobserve(e.target);
        }
      }
    }, { threshold: 0.12, rootMargin: '80px 0px' });

    els.forEach(el => io.observe(el));
  } else {
    // fallback
    els.forEach(show);
  }
})();
