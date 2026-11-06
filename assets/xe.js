/* Xtreme Ears: comportamento do site (header, 3D da hero, visualizador do produto, cena do molde,
   quiz, formulário pro WhatsApp). Sem dependências além do THREE e do iem3d.js. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var WHATS = '5511950295494';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var has3d = window.THREE && window.XE3D && XE3D.webglOk();
  var ROOT = (function () { var s = $('script[src*="xe.js"]'); return s ? s.getAttribute('src').replace(/assets\/xe\.js.*$/, '') : ''; })();
  var C = window.XE3D ? XE3D.clamp : function (v, a, b) { return Math.min(Math.max(v, a), b); };
  function zap(msg) { return 'https://wa.me/' + WHATS + '?text=' + encodeURIComponent(msg); }
  function seg(p, a, b) { return C((p - a) / (b - a), 0, 1); }
  if (!has3d) document.documentElement.classList.add('no3d');

  /* ---------------- header ---------------- */
  var hd = $('#hd'), lastY = 0;
  function onScrollHd() {
    var y = scrollY;
    if (hd) {
      hd.classList.toggle('solid', y > 40);
      hd.classList.toggle('hide', y > 400 && y > lastY && !document.body.classList.contains('menu-open'));
    }
    lastY = y;
  }
  addEventListener('scroll', onScrollHd, { passive: true }); onScrollHd();
  var burger = $('#burger'), menu = $('#menu');
  if (burger) burger.addEventListener('click', function () {
    var open = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', open); menu.hidden = !open;
    document.body.classList.toggle('menu-open', open); document.body.style.overflow = open ? 'hidden' : '';
  });
  if (menu) $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { burger.click(); }); });

  /* ---------------- reveal ---------------- */
  var io = new IntersectionObserver(function (en) {
    en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('.rv').forEach(function (el) { io.observe(el); });

  /* ---------------- filtros e cards ---------------- */
  $$('.filtros button').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('.filtros button').forEach(function (x) { x.classList.toggle('on', x === b); });
      var f = b.dataset.f;
      $$('#gridMoldados .card').forEach(function (c) { c.classList.toggle('hide', f !== 'todos' && c.dataset.area !== f); });
    });
  });
  if (matchMedia('(hover:hover)').matches) $$('.card').forEach(function (c) {
    var img = $('.card-stage img', c);
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      img.style.setProperty('--ry', (x * 22) + 'deg'); img.style.setProperty('--rx', (-y * 16) + 'deg');
      img.style.setProperty('--tx', (x * 10) + 'px'); img.style.setProperty('--ty', (y * 8) + 'px');
    });
    c.addEventListener('pointerleave', function () { ['--ry', '--rx', '--tx', '--ty'].forEach(function (p) { img.style.removeProperty(p); }); });
  });

  /* ---------------- 3D: utilidades ---------------- */
  var logoImg = null, logoCbs = [];
  function withLogo(cb) {
    if (logoImg) return cb(logoImg);
    logoCbs.push(cb);
    if (logoCbs.length > 1) return;
    XE3D.loadLogo(ROOT + 'assets/xe-mark.png', function (img) { logoImg = img; logoCbs.forEach(function (f) { f(img); }); });
  }
  function build(cfg, logo, extra) {
    var o = { bands: cfg.bands, ways: cfg.ways, shell: cfg.shell, finish: cfg.finish, face: cfg.face, logoTone: cfg.logoTone, logo: logo };
    for (var k in extra) o[k] = extra[k];
    var m = XE3D.buildIEM(o);
    XE3D.center(m.root);
    return m;
  }


  // rótulos HTML presos às fileiras de drivers na vista explodida
  var BN = { sub: 'Subgrave', bass: 'Grave', nd: 'Não divulgado', mid: 'Médio', high: 'Agudo' };
  function bandLabels(stage, model, host) {
    var els = {}, v = new THREE.Vector3(), box = new THREE.Box3();
    XE3D.ORDER.forEach(function (b) {
      if (!model.drivers[b] || !model.drivers[b].length) return;
      var el = document.createElement('span');
      el.className = 'blab b-' + b;
      el.innerHTML = '<i></i><b>' + model.drivers[b].length + '×</b> ' + BN[b];
      host.appendChild(el); els[b] = el;
    });
    return function (e) {
      var w = host.clientWidth, h = host.clientHeight;
      stage.scene.updateMatrixWorld();
      for (var b in els) {
        box.setFromObject(model.groups[b]);
        var maxX = -1e9, cy = 0, n = 0;
        [box.min, box.max].forEach(function (a) { [box.min, box.max].forEach(function (c) { [box.min, box.max].forEach(function (d) {
          v.set(a.x, c.y, d.z).project(stage.camera);
          maxX = Math.max(maxX, v.x); cy += v.y; n++;
        }); }); });
        var x = (maxX * 0.5 + 0.5) * w + 14, y = (-(cy / n) * 0.5 + 0.5) * h;
        els[b].style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) translateY(-50%)';
        els[b].style.opacity = C((e - 0.75) * 4, 0, 1);
      }
    };
  }

  /* ---------------- hero ---------------- */
  var hero = $('[data-hero3d]');
  if (hero && has3d) {
    var hcfg = JSON.parse(hero.dataset.hero3d);
    var hcan = $('.hero-canvas', hero), steps = $$('.hero-steps li', hero), copy = $('.hero-copy', hero);
    var stH = XE3D.stage(hcan, { dist: 7.8, ry: -0.75, rx: 0.12, auto: false });
    withLogo(function (logo) {
      var m = build(hcfg, logo);
      stH.spin.add(m.root);
      var labH = bandLabels(stH, m, $('.hero-sticky', hero));
      var cur = { e: 0, x: 0, y: 0, r: 0 }, bandsCycle = ['sub', 'bass', 'mid', 'high'], lastPulse = 0;
      stH.onTick(function (dt) {
        var r = hero.getBoundingClientRect(), total = hero.offsetHeight - innerHeight;
        var p = C(-r.top / total, 0, 1);
        var mobile = innerWidth < 860;
        var ex = seg(p, 0.1, 0.45) * (1 - seg(p, 0.86, 1));
        cur.e += (ex - cur.e) * Math.min(1, dt * 6);
        m.setExplode(cur.e);
        var tx = mobile ? 0.45 * cur.e : XE3D.lerp(1.55, 0.4, seg(p, 0.02, 0.3));
        var ty = mobile ? XE3D.lerp(2.1, 0.2, seg(p, 0.02, 0.3)) : 0;
        cur.x += (tx - cur.x) * Math.min(1, dt * 5); cur.y += (ty - cur.y) * Math.min(1, dt * 5);
        stH.pivot.position.set(cur.x, cur.y, 0);
        var rr = -0.3 * cur.e + Math.sin(performance.now() / 2600) * 0.12 * (1 - cur.e) - 0.15 * seg(p, 0.86, 1);
        cur.r += (rr - cur.r) * Math.min(1, dt * 4);
        stH.pivot.rotation.y = cur.r;
        stH.camera.position.z = 7.8 * (stH.camera.aspect < 0.8 ? 1.75 : 1) * (1 + cur.e * 0.32);
        var s = p < 0.12 ? 0 : p < 0.32 ? 1 : p < 0.52 ? 2 : p < 0.74 ? 3 : p < 0.94 ? 4 : 0;
        steps.forEach(function (li) { li.classList.toggle('on', +li.dataset.s === s); });
        hero.classList.toggle('open', p > 0.1 && p < 0.95);
        copy.style.opacity = 1 - seg(p, 0.02, 0.1);
        copy.style.transform = 'translateY(' + (-40 * seg(p, 0.02, 0.1)) + 'px)';
        // passo 3: as faixas acendem uma por vez
        if (s === 3) {
          lastPulse += dt;
          if (lastPulse > 0.55) { lastPulse = 0; m.pulse(bandsCycle[Math.floor(performance.now() / 550) % 4]); }
        }
        m.update(dt);
        labH(cur.e);
      });
      stH.start();
    });
  }

  /* ---------------- visualizador do produto ---------------- */
  var pv = $('[data-viewer]');
  var cta = $('#ctaZap');
  var NOMES = { shell: {}, face: {} };
  if (window.XE3D) {
    for (var k in XE3D.SHELLS) NOMES.shell[k] = XE3D.SHELLS[k].nome;
    NOMES.face = { vermelho: 'Vermelho', preto: 'Preto', azul: 'Azul', verde: 'Verde', rosa: 'Rosa', roxo: 'Roxo', dourado: 'Dourado', prata: 'Prata', branco: 'Branco' };
  }
  var FIN = { glitter: 'glitter', solido: 'sólido', perola: 'perolado', carbono: 'fibra de carbono' };
  if (pv) {
    var cfg = JSON.parse(pv.dataset.viewer);
    var sel = { shell: cfg.shell, face: cfg.face, finish: cfg.finish }, touched = false;
    function syncUI() {
      $$('[data-shell]').forEach(function (b) { b.classList.toggle('on', b.dataset.shell === sel.shell); });
      $$('[data-face]').forEach(function (b) { b.classList.toggle('on', b.dataset.face === sel.face); });
      $$('[data-finish]').forEach(function (b) { b.classList.toggle('on', b.dataset.finish === sel.finish); });
      var ls = $('[data-lb=shell]'), lf = $('[data-lb=face]');
      if (ls) ls.textContent = NOMES.shell[sel.shell] || '';
      if (lf) lf.textContent = (NOMES.face[sel.face] || '') + ', ' + FIN[sel.finish];
      if (cta) {
        var msg = cta.dataset.base + (touched ? ' Montei assim no site: concha ' + (NOMES.shell[sel.shell] || '').toLowerCase() + ', faceplate ' + (NOMES.face[sel.face] || '').toLowerCase() + ' ' + FIN[sel.finish] + '.' : '');
        cta.href = zap(msg);
        $$('[data-sync=ctaZap]').forEach(function (a) { a.href = cta.href; });
      }
    }
    syncUI();
    var model = null, stP = null, exT = 0, exC = 0, focus = null;
    var btnEx = $('.pv-explode', pv);
    function setEx(on) { exT = on ? 1 : 0; btnEx.setAttribute('aria-pressed', on); $('span', btnEx).textContent = on ? 'Fechar o fone' : 'Abrir o fone'; }
    btnEx.addEventListener('click', function () { setEx(exT === 0); if (!exT) setFocus(null); });
    function setFocus(b) {
      focus = focus === b ? null : b;
      $$('[data-focus]').forEach(function (x) { x.classList.toggle('on', x.dataset.focus === focus); });
      if (model) { model.setFocus(focus); if (focus) model.pulse(focus); }
      if (focus) setEx(true);
    }
    $$('[data-focus]').forEach(function (b) {
      b.addEventListener('click', function () {
        setFocus(b.dataset.focus);
        if (b.classList.contains('sig-b') && innerWidth < 900) pv.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      });
    });
    $$('[data-shell],[data-face],[data-finish]').forEach(function (b) {
      b.addEventListener('click', function () {
        touched = true;
        if (b.dataset.shell) { sel.shell = b.dataset.shell; if (model) model.setShell(sel.shell); }
        if (b.dataset.face) { sel.face = b.dataset.face; if (model) model.setFace(sel.finish, sel.face); }
        if (b.dataset.finish) { sel.finish = b.dataset.finish; if (model) model.setFace(sel.finish, sel.face); }
        if (exT && (b.dataset.face || b.dataset.finish)) setEx(false);
        syncUI();
      });
    });
    if (has3d) {
      stP = XE3D.stage($('.pv-canvas', pv), { dist: 8, ry: -0.75, rx: 0.15 });
      withLogo(function (logo) {
        model = build(cfg, logo);
        stP.spin.add(model.root);
        var labP = bandLabels(stP, model, pv);
        stP.onTick(function (dt) {
          exC += (exT - exC) * Math.min(1, dt * 4);
          // aberto, o fone vira de lado pra mostrar as camadas
          var st = stP.state;
          st.auto = !exT;
          if (exT && !st.drag) {
            var tgt = -1.0 + Math.round((st.ry + 1.0) / (Math.PI * 2)) * Math.PI * 2;
            st.ry += (tgt - st.ry) * Math.min(1, dt * 3);
            st.rx += (0.12 - st.rx) * Math.min(1, dt * 3);
          }
          model.setExplode(exC);
          stP.camera.position.z = stP.state.dist * (stP.camera.aspect < 0.8 ? 1.25 : 1) * (1 + exC * 0.3);
          
          model.update(dt);
          labP(exC);
        });
        stP.start();
      });
    }
    // barra fixa aparece quando o botão principal sai da tela
    var bar = $('#bar');
    if (bar && cta) {
      bar.hidden = false;
      new IntersectionObserver(function (en) {
        var past = !en[0].isIntersecting && en[0].boundingClientRect.top < 0;
        bar.classList.toggle('on', past);
      }).observe(cta);
    }
  }

  /* ---------------- molde: loop na home ---------------- */
  var ml = $('[data-molde-loop]');
  if (ml && has3d) {
    var tag = $('[data-molde-tag]');
    var stL = XE3D.stage(ml, { dist: 8.4, ry: -1.1, rx: 0.1, drag: true });
    withLogo(function (logo) {
      var imp = XE3D.buildImpression();
      var iem = XE3D.buildIEM({ bands: { bass: 2, mid: 2, high: 2 }, ways: 3, shell: 'transparente', finish: 'glitter', face: 'verde', logo: logo });
      var off = new THREE.Box3().setFromObject(imp.root).getCenter(new THREE.Vector3());
      imp.root.position.sub(off); iem.root.position.sub(off);
      stL.spin.add(imp.root); stL.spin.add(iem.root);
      var t = 0, label = '';
      stL.onTick(function (dt) {
        t = (t + dt) % 11;
        var a = moldeState(t / 11);
        applyMolde(imp, iem, a);
        if (a.label !== label) { label = a.label; tag.textContent = label; }
        iem.update(dt);
      });
      stL.start();
    });
  }
  // linha do tempo do molde (0..1), usada pelo loop e pela página /molde/
  function moldeState(p) {
    var s = {};
    s.imp = 1 - seg(p, 0.42, 0.55);
    s.wire = seg(p, 0.28, 0.4) * (1 - seg(p, 0.5, 0.58));
    s.shell = seg(p, 0.46, 0.58);
    s.inside = seg(p, 0.62, 0.8);
    s.face = seg(p, 0.74, 0.86);
    s.label = p < 0.3 ? 'Molde de silicone' : p < 0.5 ? 'Molde aprovado' : p < 0.64 ? 'Concha de acrílico' : p < 0.84 ? 'Drivers e crossover' : 'Fone pronto';
    if (p > 0.94) { var b = seg(p, 0.94, 1); s.imp = b; s.shell = 1 - b; s.inside = 1 - b; s.face = 1 - b; }
    return s;
  }
  function applyMolde(imp, iem, s) {
    imp.setOpacity(s.imp); imp.setWire(s.wire * 0.55);
    iem.setExplode(1 - s.inside);
    var g = iem.groups, sh = g.shell.children[0].material;
    g.shell.visible = s.shell > 0.01;
    sh.opacity = 0.16 + (1 - s.inside) * 0.25 * s.shell; sh.opacity *= s.shell > 0 ? 1 : 0;
    g.shell.children.forEach(function (c, i) { if (i) c.visible = s.shell > 0.5; });
    ['sub', 'bass', 'nd', 'mid', 'high', 'pcb', 'tubes', 'wires'].forEach(function (k) { if (g[k]) g[k].visible = s.inside > 0.01; });
    g.shell.position.copy(g.shell.userData.home);
    g.face.visible = s.face > 0.01;
    g.face.position.copy(g.face.userData.home).add(new THREE.Vector3(-0.2, 0.3, 1.4).multiplyScalar(1 - XE3D.ease(s.face)));
  }

  /* ---------------- molde: página com rolagem ---------------- */
  var mh = $('[data-molde-scroll]');
  if (mh && has3d) {
    var mcan = $('.mh-canvas', mh), msteps = $$('.mh-steps li', mh), mbar = $('.mh-bar', mh);
    var stM = XE3D.stage(mcan, { dist: 9.2, ry: -0.9, rx: 0.1, auto: true });
    withLogo(function (logo) {
      var imp = XE3D.buildImpression();
      var iem = XE3D.buildIEM({ bands: { bass: 4, mid: 2, high: 2 }, ways: 3, shell: 'transparente', finish: 'glitter', face: 'vermelho', logo: logo });
      var off = new THREE.Box3().setFromObject(imp.root).getCenter(new THREE.Vector3());
      imp.root.position.sub(off); iem.root.position.sub(off);
      stM.spin.add(imp.root); stM.spin.add(iem.root);
      var cx = 0;
      stM.onTick(function (dt) {
        var r = mh.getBoundingClientRect(), total = mh.offsetHeight - innerHeight;
        var p = C(-r.top / total, 0, 1);
        var mobile = innerWidth < 860;
        mh.classList.toggle('go', p > 0.03);
        var q = seg(p, 0.05, 1);
        var step = p < 0.05 ? -1 : Math.min(4, Math.floor(q * 5));
        msteps.forEach(function (li) { li.classList.toggle('on', +li.dataset.s === step); });
        mbar.style.setProperty('--p', (p * 100) + '%');
        // cada passo percorre o seu trecho da linha do tempo do loop
        var RANGE = [[0.05, 0.2], [0.2, 0.27], [0.3, 0.42], [0.52, 0.62], [0.62, 0.92]];
        var f = q * 5, i = Math.min(4, Math.floor(f)), fr = i === 4 ? Math.min(1, (f - 4) * 1.4) : f - i;
        var tl = XE3D.lerp(RANGE[i][0], RANGE[i][1], XE3D.ease(fr));
        applyMolde(imp, iem, moldeState(Math.min(tl, 0.93)));
        var tx = mobile ? 0 : (p < 0.03 ? 1.6 : 1.3);
        cx += (tx - cx) * Math.min(1, dt * 4);
        stM.pivot.position.set(cx, mobile ? 1.1 : 0, 0);
        stM.camera.position.z = 9.2 * (mobile ? 1.55 : 1);
        stM.pivot.rotation.y = step === 1 ? -0.9 : 0;
        iem.update(dt);
      });
      stM.start();
    });
  }

  /* ---------------- quiz ---------------- */
  var qz = $('[data-quiz]');
  if (qz) {
    var CAT = JSON.parse(qz.dataset.quiz);
    var TRILHA = {
      grave: { a: ['one-plus-pro', 'xe3-pro', 'xe6-pro', 'xe6-pro'], b: ['xtreme-one-plus', 'xe6-pro', 'xe8-pro', 'xe12-pro'] },
      medio: { a: ['one-plus-pro', 'xe4-pro', 'xe8-pro', 'xe12-pro'], b: ['xtreme-onemax', 'xe5-pro', 'xe5-pro', 'xe14-pro'] },
      agudo: { a: ['xtreme-onemax', 'onemax-pro', 'xe12-pro', 'xe14-pro'], b: ['onemax-pro', 'xe4-pro', 'xe8-pro', 'xe12-pro'] }
    };
    var ans = [], qs = $$('.q', qz), back = $('.quiz-back', qz), prog = $('.quiz-prog i', qz);
    function show(i) {
      qs.forEach(function (q) { q.classList.toggle('on', +q.dataset.q === i); });
      back.hidden = i === 0;
      prog.style.setProperty('--p', (i / 3 * 100) + '%');
    }
    qs.forEach(function (q, qi) {
      $$('button', q).forEach(function (b) {
        b.addEventListener('click', function () {
          ans[qi] = { v: b.dataset.v, t: b.dataset.t };
          if (qi < 2) return show(qi + 1);
          result();
        });
      });
    });
    back.addEventListener('click', function () {
      var cur = qs.findIndex(function (q) { return q.classList.contains('on'); });
      show(Math.max(0, cur - 1));
    });
    function result() {
      var tr = TRILHA[ans[0].v], n = +ans[2].v;
      var a = tr.a[n], b = tr.b[n];
      if (b === a) b = tr.b[(n + 1) % 4];
      var A = CAT[a], B = CAT[b];
      var msg = 'Olá! Fiz o teste no site da Xtreme Ears. Sou: ' + ans[0].t + '. Uso mais em: ' + ans[1].t + '. Investimento: ' + ans[2].t +
        '. O site indicou o ' + A.nome + ' (alternativa: ' + B.nome + '). Pode me ajudar a confirmar?';
      var ambient = ans[1].v === '0' || ans[1].v === '1' ? '<p class="tiny">Toca em igreja ou casa de show e quer ouvir a plateia? Pergunte pela opção Ambient.</p>' : '';
      var res = $('.q-res', qz);
      res.innerHTML = '<div class="res"><img src="' + ROOT + A.img + '" alt="" width="300" height="300"><div><span class="res-k">Indicado pra você</span><h3>' + A.nome + '</h3>' +
        '<p>' + A.ass + '. ' + A.n + (A.n === 1 ? ' driver' : ' drivers') + ', a partir de R$ ' + A.preco + '.</p></div></div>' +
        '<div class="res-ctas"><a class="btn btn-zap" target="_blank" rel="noopener" data-cta="quiz" href="' + zap(msg) + '">Confirmar com especialista</a>' +
        '<a class="btn btn-ghost" href="' + ROOT + a + '/">Ver o ' + A.nome + '</a></div>' + ambient +
        '<p class="res-alt">Alternativa: <a href="' + ROOT + b + '/">' + B.nome + '</a>, ' + B.ass.toLowerCase() + ', a partir de R$ ' + B.preco + '.</p>';
      show(3);
      prog.style.setProperty('--p', '100%');
    }
  }

  /* ---------------- formulário -> WhatsApp ---------------- */
  var form = $('#formZap');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = form.elements;
    if (!f.nome.value.trim()) { f.nome.classList.add('err'); f.nome.focus(); return; }
    var msg = 'Olá! Sou ' + f.nome.value.trim() + (f.cidade.value.trim() ? ', de ' + f.cidade.value.trim() : '') + '. ' +
      'Perfil: ' + f.perfil.value + '. Modelo de interesse: ' + f.modelo.value + '.' + (f.ctx.value.trim() ? ' ' + f.ctx.value.trim() : '');
    window.open(zap(msg), '_blank', 'noopener');
  });
  $$('#formZap input').forEach(function (i) { i.addEventListener('input', function () { i.classList.remove('err'); }); });

  /* ---------------- links de outros modelos no formulário ---------------- */
  var url = new URLSearchParams(location.search).get('modelo');
  if (url && form) { var s = form.elements.modelo; [].slice.call(s.options).forEach(function (o) { if (o.text === url) s.value = url; }); }
})();
