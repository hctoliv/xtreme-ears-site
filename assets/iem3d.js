/* Xtreme Ears: fone moldado em 3D, montado por código a partir da configuração de cada modelo.
   Casco, faceplate, crossover e um driver de armadura balanceada para cada driver do catálogo,
   agrupados por faixa (subgrave, grave, médio, agudo). Também monta o molde de silicone do ouvido
   e um visualizador com arrasto. Usa o THREE global (three@0.160.0/build/three.min.js). */
(function (global) {
  'use strict';

  var BANDS = {
    sub:  { color: 0xb18cff, css: '#b18cff', nome: 'Subgrave', size: [0.27, 0.2, 0.16] },
    bass: { color: 0xff6b3d, css: '#ff6b3d', nome: 'Grave',    size: [0.25, 0.18, 0.15] },
    mid:  { color: 0x3fa2ff, css: '#3fa2ff', nome: 'Médio',    size: [0.21, 0.15, 0.13] },
    high: { color: 0xffcf4a, css: '#ffcf4a', nome: 'Agudo',    size: [0.17, 0.13, 0.11] },
    nd:   { color: 0x8b9099, css: '#8b9099', nome: 'Não divulgado', size: [0.22, 0.16, 0.13] }
  };
  var ORDER = ['sub', 'bass', 'nd', 'mid', 'high'];

  // cores do casco: as mesmas do personalizador da loja
  var SHELLS = {
    'transparente':      { nome: 'Transparente',      color: 0xcfe0f0, opacity: 0.16,  css: 'rgba(233,239,245,.35)' },
    'preto-translucido': { nome: 'Preto translúcido', color: 0x30343b, opacity: 0.62, css: '#3a3e45' },
    'preto':             { nome: 'Preto',             color: 0x111214, opacity: 0.97, css: '#141416' },
    'azul':              { nome: 'Azul',              color: 0x2563eb, opacity: 0.58, css: '#2563eb' },
    'verde':             { nome: 'Verde',             color: 0x16a34a, opacity: 0.58, css: '#16a34a' },
    'vermelho':          { nome: 'Vermelho',          color: 0xd21f2b, opacity: 0.6,  css: '#d21f2b' },
    'rosa':              { nome: 'Rosa',              color: 0xe1408f, opacity: 0.58, css: '#e1408f' },
    'rosa-claro':        { nome: 'Rosa claro',        color: 0xf5b6d2, opacity: 0.5,  css: '#f5b6d2' }
  };
  var FINISHES = { glitter: 'Glitter', solido: 'Sólido', carbono: 'Fibra de carbono', perola: 'Perolado' };
  var FACE_COLORS = {
    'vermelho': '#b3141f', 'preto': '#121212', 'azul': '#1d4ed8', 'verde': '#15803d', 'rosa': '#db2777',
    'dourado': '#b8892f', 'prata': '#9aa3ad', 'branco': '#ececec', 'roxo': '#6d28d9'
  };

  var OUTLINE_PTS = [[0.5, 0.64], [0.18, 0.8], [-0.22, 0.76], [-0.52, 0.5], [-0.62, 0.1], [-0.52, -0.28], [-0.27, -0.54],
                     [0.03, -0.72], [0.3, -0.82], [0.48, -0.7], [0.56, -0.38], [0.58, 0.05], [0.57, 0.42]];
  var olCache = {};
  function outlinePoints(n) {
    if (olCache[n]) return olCache[n];
    var curve = new THREE.CatmullRomCurve3(OUTLINE_PTS.map(function (p) { return new THREE.Vector3(p[0] * 1.2, p[1] * 1.2, 0); }), true, 'centripetal');
    olCache[n] = curve.getSpacedPoints(n).slice(0, n);
    return olCache[n];
  }
  function canvasTex(w, h, draw) {
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    draw(c.getContext('2d'), w, h);
    var tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
    return tex;
  }
  function smooth(e0, e1, x) { var t = Math.min(Math.max((x - e0) / (e1 - e0), 0), 1); return t * t * (3 - 2 * t); }
  function clamp(v, a, b) { return Math.min(Math.max(v, a), b); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { t = clamp(t, 0, 1); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  var TOP = 0.42;
  var CANAL_DIR = new THREE.Vector3(0.55, -0.22, -0.8).normalize();
  var BODY_DEPTH = 1.02;
  var BODY_END = new THREE.Vector3(0.34, -0.36, TOP - BODY_DEPTH);

  /* Corpo moldado: o contorno do faceplate vira um volume cheio que estufa na concha e na hélix
     e afina até a cânula. Com p.canal maior e p.bend, a mesma função desenha o molde de silicone,
     que vai além da segunda curva do canal. */
  function shellGeometry(p) {
    p = p || {};
    var canalLen = p.canal || 0.46, bend = p.bend || 0, swell = p.swell || 0;
    var RINGS = p.rings || 72, SEG = p.seg || 140;
    var ol = outlinePoints(SEG), pos = [], idx = [];
    var bowl = new THREE.Vector2(-0.35, -0.94).normalize();
    var helix = new THREE.Vector2(-0.62, 0.78).normalize();
    var split = 0.74 * 0.46 / (0.46 + (canalLen - 0.46) * 0.75);
    var dir2 = CANAL_DIR.clone().add(new THREE.Vector3(0.45, 0.25, -0.1).multiplyScalar(bend)).normalize();
    for (var i = 0; i <= RINGS; i++) {
      var u = i / RINGS, cx, cy, cz, sc, m, r;
      if (u <= split) {
        var v = u / split, k = smooth(0.35, 1, v);
        cx = BODY_END.x * k; cy = BODY_END.y * k; cz = TOP - BODY_DEPTH * v;
        sc = (1 + (0.1 + swell) * Math.sin(Math.min(v / 0.45, 1) * Math.PI)) * (1 - 0.7 * smooth(0.3, 1, v));
        m = smooth(0.55, 1, v); r = 0.3;
      } else {
        var w = (u - split) / (1 - split), L = canalLen * w;
        var c = BODY_END.clone().addScaledVector(CANAL_DIR, Math.min(L, 0.42));
        if (L > 0.42) c.addScaledVector(dir2, L - 0.42);
        cx = c.x; cy = c.y; cz = c.z; sc = 1; m = 1;
        r = 0.3 - 0.07 * w;
        if (w > 0.9) r *= 0.6 + 0.4 * Math.sqrt(Math.max(1 - Math.pow((w - 0.9) / 0.1, 2), 0.02));
      }
      var vv = Math.min(u / split, 1);
      var bulge = Math.sin(Math.min(vv / 0.7, 1) * Math.PI) * (1 - m);
      for (var j = 0; j < SEG; j++) {
        var a = (j / SEG) * Math.PI * 2;
        var px = ol[j].x, py = ol[j].y;
        var len = Math.hypot(px, py) || 1, dx = px / len, dy = py / len;
        var e = 1 + bulge * ((0.3 + swell) * Math.pow(Math.max(0, dx * bowl.x + dy * bowl.y), 1.4) + (0.26 + swell) * Math.pow(Math.max(0, dx * helix.x + dy * helix.y), 2.5));
        var ox = px * sc * e, oy = py * sc * e;
        var qx = Math.cos(a) * r, qy = Math.sin(a) * r * 0.88;
        pos.push(cx + ox * (1 - m) + qx * m, cy + oy * (1 - m) + qy * m, cz);
      }
    }
    for (i = 0; i < RINGS; i++) for (j = 0; j < SEG; j++) {
      var a0 = i * SEG + j, a1 = i * SEG + (j + 1) % SEG, b0 = a0 + SEG, b1 = a1 + SEG;
      idx.push(a0, b0, a1, a1, b0, b1);
    }
    // tampa do fundo (ponta da cânula)
    var last = RINGS * SEG, cen = pos.length / 3, cxs = 0, cys = 0, czs = 0;
    for (j = 0; j < SEG; j++) { cxs += pos[(last + j) * 3]; cys += pos[(last + j) * 3 + 1]; czs += pos[(last + j) * 3 + 2]; }
    pos.push(cxs / SEG, cys / SEG, czs / SEG);
    for (j = 0; j < SEG; j++) idx.push(last + j, cen, last + (j + 1) % SEG);
    // tampa de cima, só no molde (o fone tem o faceplate ali)
    if (p.capTop) {
      var c2 = pos.length / 3, sx = 0, sy = 0;
      for (j = 0; j < SEG; j++) { sx += pos[j * 3]; sy += pos[j * 3 + 1]; }
      pos.push(sx / SEG, sy / SEG, TOP + 0.04);
      for (j = 0; j < SEG; j++) idx.push(j, (j + 1) % SEG, c2);
    }
    var g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setIndex(idx); g.computeVertexNormals();
    return g;
  }
  function canalTip(len) { return BODY_END.clone().addScaledVector(CANAL_DIR, len || 0.46); }

  function faceplateGeometry() {
    var ol = outlinePoints(120), shape = new THREE.Shape();
    ol.forEach(function (p, k) { if (k === 0) shape.moveTo(p.x, p.y); else shape.lineTo(p.x, p.y); });
    shape.closePath();
    var g = new THREE.ExtrudeGeometry(shape, { depth: 0.09, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.035, bevelSegments: 8, curveSegments: 120 });
    g.computeBoundingBox();
    var bb = g.boundingBox, uv = g.attributes.uv, ps = g.attributes.position;
    for (var i = 0; i < uv.count; i++) uv.setXY(i, (ps.getX(i) - bb.min.x) / (bb.max.x - bb.min.x), (ps.getY(i) - bb.min.y) / (bb.max.y - bb.min.y));
    return g;
  }

  function shade(hex, f) {
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    var t = f < 0 ? 0 : 255, p = Math.abs(f);
    return 'rgb(' + Math.round(r + (t - r) * p) + ',' + Math.round(g + (t - g) * p) + ',' + Math.round(b + (t - b) * p) + ')';
  }

  /* Faceplate: acabamento + cor + o símbolo XE em metal escovado */
  function drawFace(ctx, w, h, finish, color, logo, logoTone) {
    var base = FACE_COLORS[color] || color || '#121212';
    var g = ctx.createRadialGradient(w * 0.42, h * 0.38, 20, w * 0.5, h * 0.5, w * 0.75);
    g.addColorStop(0, shade(base, 0.12)); g.addColorStop(1, shade(base, -0.55));
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    var i, x, y, s;
    if (finish === 'glitter') {
      for (i = 0; i < 5200; i++) {
        x = Math.random() * w; y = Math.random() * h; s = Math.random() * 2.6 + 0.4;
        ctx.fillStyle = Math.random() < 0.18 ? 'rgba(255,255,255,' + (0.4 + Math.random() * 0.6) + ')' : shade(base, 0.25 + Math.random() * 0.45);
        ctx.globalAlpha = 0.35 + Math.random() * 0.65;
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.random() * 3); ctx.fillRect(-s, -s * 0.6, s * 2, s * 1.2); ctx.restore();
      }
      ctx.globalAlpha = 1;
    } else if (finish === 'carbono') {
      ctx.fillStyle = '#0c0d0f'; ctx.fillRect(0, 0, w, h);
      var cell = 26;
      for (y = 0; y < h; y += cell) for (x = 0; x < w; x += cell) {
        var odd = ((x + y) / cell) % 2 === 0;
        var lg = odd ? ctx.createLinearGradient(x, y, x + cell, y) : ctx.createLinearGradient(x, y, x, y + cell);
        lg.addColorStop(0, '#1b1d21'); lg.addColorStop(0.5, '#3a3e45'); lg.addColorStop(1, '#16181b');
        ctx.fillStyle = lg; ctx.fillRect(x + 1, y + 1, cell - 2, cell - 2);
      }
      if (color && color !== 'preto') { ctx.globalCompositeOperation = 'overlay'; ctx.fillStyle = base; ctx.fillRect(0, 0, w, h); ctx.globalCompositeOperation = 'source-over'; }
    } else if (finish === 'perola') {
      for (i = 0; i < 26; i++) {
        var rg = ctx.createRadialGradient(Math.random() * w, Math.random() * h, 0, Math.random() * w, Math.random() * h, 120 + Math.random() * 260);
        rg.addColorStop(0, 'rgba(255,255,255,.22)'); rg.addColorStop(0.4, 'rgba(200,220,255,.08)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = rg; ctx.fillRect(0, 0, w, h);
      }
    }
    if (logo && logo.complete && logo.naturalWidth) {
      var dw = w * 0.36, dh = dw * logo.naturalHeight / logo.naturalWidth;
      var tmp = document.createElement('canvas'); tmp.width = dw; tmp.height = dh;
      var t = tmp.getContext('2d');
      t.drawImage(logo, 0, 0, dw, dh);
      t.globalCompositeOperation = 'source-in';
      var mg = t.createLinearGradient(0, 0, dw, dh);
      if (logoTone === 'ouro') { mg.addColorStop(0, '#f6e3ad'); mg.addColorStop(0.5, '#c39443'); mg.addColorStop(1, '#f0d48f'); }
      else { mg.addColorStop(0, '#f4f6f8'); mg.addColorStop(0.45, '#9da4ac'); mg.addColorStop(0.55, '#c9cfd5'); mg.addColorStop(1, '#eef1f4'); }
      t.fillStyle = mg; t.fillRect(0, 0, dw, dh);
      ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = 10; ctx.shadowOffsetY = 4;
      ctx.drawImage(tmp, (w - dw) / 2 - w * 0.02, (h - dh) / 2 + h * 0.02);
      ctx.shadowColor = 'transparent';
    }
  }

  function roundedBox(w, h, d, r) {
    var s = new THREE.Shape(), x = -w / 2, y = -h / 2;
    s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
    s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
    var g = new THREE.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: 0.008, bevelSize: 0.008, bevelSegments: 2 });
    g.translate(0, 0, -d / 2);
    return g;
  }

  var geoCache = {};
  // Armadura balanceada: caixinha de metal, contatos coloridos pela faixa e o bico de saída
  function baDriver(band) {
    var B = BANDS[band], sz = B.size, key = band;
    if (!geoCache[key]) geoCache[key] = roundedBox(sz[0], sz[1], sz[2], 0.014);
    var g = new THREE.Group();
    var bodyCol = new THREE.Color(0xc8cbd0).lerp(new THREE.Color(B.color), 0.45);
    var body = new THREE.Mesh(geoCache[key], new THREE.MeshPhysicalMaterial({ color: bodyCol, metalness: 0.65, roughness: 0.3, clearcoat: 0.5 }));
    g.add(body);
    var padMat = new THREE.MeshStandardMaterial({ color: B.color, emissive: B.color, emissiveIntensity: 0.35, metalness: 0.3, roughness: 0.35 });
    for (var r = 0; r < 2; r++) for (var c = 0; c < 2; c++) {
      var pad = new THREE.Mesh(new THREE.BoxGeometry(sz[0] * 0.32, sz[1] * 0.13, 0.012), padMat);
      pad.position.set((c - 0.5) * sz[0] * 0.44, (r - 0.5) * sz[1] * 0.46, -sz[2] / 2 - 0.007);
      g.add(pad);
    }
    var stripe = new THREE.Mesh(new THREE.BoxGeometry(sz[0] * 1.002, sz[1] * 0.16, sz[2] * 1.02), padMat);
    g.add(stripe);
    var spout = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.08, 18), new THREE.MeshStandardMaterial({ color: 0x8a8d92, metalness: 1, roughness: 0.25 }));
    spout.rotation.z = Math.PI / 2; spout.position.set(sz[0] / 2 + 0.035, 0, 0);
    g.add(spout);
    g.userData.glow = padMat;
    return g;
  }

  function tube(points, radius, mat) {
    var curve = new THREE.CatmullRomCurve3(points.map(function (p) { return p.isVector3 ? p : new THREE.Vector3(p[0], p[1], p[2]); }));
    return new THREE.Mesh(new THREE.TubeGeometry(curve, 48, radius, 10, false), mat);
  }

  // altura de cada faixa na vista explodida: uma fileira por faixa, do subgrave embaixo ao agudo em cima
  var EXY = { sub: -0.95, bass: -0.4, nd: -0.4, mid: 0.2, high: 0.75 };
  // onde cada faixa mora dentro do casco
  var ZONES = {
    sub:  { at: [-0.3, -0.42, -0.16], out: [-1.05, -1.0, 0.15] },
    bass: { at: [-0.32, -0.08, 0.02],  out: [-1.25, -0.15, 0.4] },
    mid:  { at: [0.02, 0.24, -0.04],  out: [0.15, 1.05, 0.25] },
    high: { at: [0.3, -0.24, -0.22],  out: [1.15, -0.45, 0.4] },
    nd:   { at: [-0.3, -0.22, -0.04], out: [-1.2, -0.55, 0.35] }
  };

  /* Monta um fone.
     opts: bands {sub,bass,mid,high}, ways (vias do crossover), shell (chave de SHELLS),
     finish, face (cor), logo (Image), logoTone, cable (bool), mirror (bool) */
  function buildIEM(opts) {
    opts = opts || {};
    var bands = opts.bands || { bass: 1, mid: 1, high: 1 };
    var root = new THREE.Group();
    var groups = {}, drivers = { sub: [], bass: [], nd: [], mid: [], high: [] };
    var total = ORDER.reduce(function (s, k) { return s + (bands[k] || 0); }, 0);
    var dscale = 1.45 * (total <= 4 ? 1 : total <= 6 ? 0.85 : total <= 8 ? 0.74 : total <= 12 ? 0.62 : 0.56);

    var shellDef = SHELLS[opts.shell] || SHELLS['preto-translucido'];
    var shellMat = new THREE.MeshPhysicalMaterial({
      color: shellDef.color, metalness: 0, roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.04,
      transparent: true, opacity: shellDef.opacity, side: THREE.DoubleSide, depthWrite: false, envMapIntensity: 1.2
    });
    var shell = new THREE.Mesh(shellGeometry(), shellMat);
    shell.renderOrder = 3;
    groups.shell = new THREE.Group(); groups.shell.add(shell);
    // boca da cânula: três saídas de som e o anel de lado (vermelho = direito, azul = esquerdo)
    var tip = canalTip(), nd = CANAL_DIR.clone();
    var q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, -1), nd);
    var ring = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.012, 8, 40), new THREE.MeshStandardMaterial({ color: opts.mirror ? 0x2d6bd6 : 0xd62d2d, roughness: 0.4 }));
    ring.position.copy(tip).addScaledVector(nd, -0.13); ring.quaternion.copy(q); groups.shell.add(ring);
    var boreMat = new THREE.MeshBasicMaterial({ color: 0x050505 });
    [[-0.06, 0.03], [0.06, 0.04], [0, -0.06]].forEach(function (o) {
      var b = new THREE.Mesh(new THREE.CircleGeometry(0.032, 18), boreMat);
      var sx = new THREE.Vector3(1, 0, 0).applyQuaternion(q), up = new THREE.Vector3(0, 1, 0).applyQuaternion(q);
      b.position.copy(tip).addScaledVector(sx, o[0]).addScaledVector(up, o[1]).addScaledVector(nd, -0.01);
      b.quaternion.copy(q); b.rotateY(Math.PI); groups.shell.add(b);
    });
    root.add(groups.shell);

    // faceplate
    var faceCanvas = document.createElement('canvas'); faceCanvas.width = 1024; faceCanvas.height = 1300;
    var faceTex = new THREE.CanvasTexture(faceCanvas); faceTex.colorSpace = THREE.SRGBColorSpace; faceTex.anisotropy = 8;
    if (opts.mirror) { faceTex.wrapS = THREE.RepeatWrapping; faceTex.repeat.x = -1; faceTex.offset.x = 1; }
    var faceMat = new THREE.MeshPhysicalMaterial({ map: faceTex, metalness: 0.25, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.03 });
    var edgeMat = new THREE.MeshPhysicalMaterial({ color: 0x222222, metalness: 0.3, roughness: 0.25, clearcoat: 1 });
    function paintFace(finish, color) {
      opts.finish = finish || opts.finish || 'glitter'; opts.face = color || opts.face || 'vermelho';
      drawFace(faceCanvas.getContext('2d'), 1024, 1300, opts.finish, opts.face, opts.logo, opts.logoTone);
      faceMat.metalness = opts.finish === 'perola' ? 0.45 : opts.finish === 'carbono' ? 0.35 : 0.2;
      faceTex.needsUpdate = true;
      edgeMat.color.set(opts.finish === 'carbono' ? '#15171a' : shade(FACE_COLORS[opts.face] || opts.face, -0.35));
    }
    paintFace();
    var face = new THREE.Mesh(faceplateGeometry(), [faceMat, edgeMat]);
    face.position.z = TOP - 0.035;
    groups.face = new THREE.Group(); groups.face.add(face);
    var sock = new THREE.Mesh(roundedBox(0.18, 0.1, 0.12, 0.03), new THREE.MeshPhysicalMaterial({ color: 0x1a1a1c, roughness: 0.3, metalness: 0.4 }));
    sock.position.set(0.5, 0.74, 0.5); groups.face.add(sock);
    var pinMat = new THREE.MeshStandardMaterial({ color: 0xd9b46a, metalness: 1, roughness: 0.2 });
    for (var pi = 0; pi < 2; pi++) {
      var pin = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.08, 10), pinMat);
      pin.position.set(0.47 + pi * 0.06, 0.8, 0.5); groups.face.add(pin);
    }
    root.add(groups.face);

    // crossover: placa com uma trilha por via
    var ways = opts.ways || 3;
    var pcb = new THREE.Group();
    pcb.add(new THREE.Mesh(roundedBox(0.6, 0.32, 0.025, 0.04), new THREE.MeshStandardMaterial({ color: 0x15201b, roughness: 0.55, metalness: 0.2 })));
    var compMats = [new THREE.MeshStandardMaterial({ color: 0xc9a26a, roughness: 0.4 }), new THREE.MeshStandardMaterial({ color: 0x2b2b2e, roughness: 0.3, metalness: 0.4 })];
    for (var ci = 0; ci < 8; ci++) {
      var cm = new THREE.Mesh(new THREE.BoxGeometry(0.05 + (ci % 3) * 0.015, 0.04, 0.035), compMats[ci % 2]);
      cm.position.set(-0.22 + (ci % 4) * 0.14, ci < 4 ? 0.08 : -0.08, 0.03); pcb.add(cm);
    }
    var traceMats = [];
    var wayBands = ORDER.filter(function (k) { return bands[k]; });
    for (var tr = 0; tr < ways; tr++) {
      var bk = wayBands[Math.min(tr, wayBands.length - 1)] || 'mid';
      var tm = new THREE.MeshStandardMaterial({ color: BANDS[bk].color, emissive: BANDS[bk].color, emissiveIntensity: 0.5, metalness: 0.6, roughness: 0.3 });
      traceMats.push(tm);
      var t1 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.012, 0.005), tm);
      t1.position.set(0, -0.12 + tr * (0.24 / Math.max(ways - 1, 1)), 0.016); pcb.add(t1);
    }
    pcb.position.set(-0.18, 0.12, 0.25); pcb.rotation.set(0.05, -0.08, 0.06);
    groups.pcb = pcb; root.add(pcb);

    // drivers, faixa por faixa
    var tubeMat = new THREE.MeshPhysicalMaterial({ color: 0xeef3f8, roughness: 0.15, transparent: true, opacity: 0.55 });
    groups.tubes = new THREE.Group();
    ORDER.forEach(function (band) {
      var n = bands[band] || 0;
      var grp = new THREE.Group();
      grp.position.fromArray(ZONES[band].at);
      grp.userData.home = grp.position.clone();
      grp.userData.target = new THREE.Vector3(0.05, EXY[band], 0.45);
      var sz = BANDS[band].size;
      var hex = n === 6 && band === 'mid';
      for (var i = 0; i < n; i++) {
        var d = baDriver(band);
        var col = i % 2, row = Math.floor(i / 2), rows = Math.ceil(n / 2);
        var p;
        if (hex) {
          var a = i / 6 * Math.PI * 2;
          p = new THREE.Vector3(Math.cos(a) * sz[0] * 0.95, Math.sin(a) * sz[1] * 1.25, 0);
        } else {
          p = new THREE.Vector3((n === 1 ? 0 : (col - 0.5)) * sz[0] * 0.55, (row - (rows - 1) / 2) * sz[1] * 1.08, (n === 1 ? 0 : (col - 0.5)) * -sz[2] * 1.05);
        }
        d.userData.base = p.clone();
        d.userData.spread = new THREE.Vector3(0, 0, (i - (n - 1) / 2) * sz[0] * dscale * 1.25);
        d.position.copy(p);
        d.rotation.set(0.15, -0.35, band === 'high' ? -0.5 : 0.1);
        d.scale.setScalar(dscale);
        grp.add(d); drivers[band].push(d);
      }
      groups[band] = grp; root.add(grp);
      if (n) {
        var from = grp.position.clone(), mid = BODY_END.clone(), end = tip.clone().addScaledVector(nd, -0.04);
        groups.tubes.add(tube([from, from.clone().lerp(mid, 0.5).add(new THREE.Vector3(0, 0.03, 0)), mid, end], 0.022, tubeMat));
      }
    });
    root.add(groups.tubes);

    var wireMat = new THREE.MeshStandardMaterial({ color: 0xb87333, metalness: 1, roughness: 0.35 });
    groups.wires = new THREE.Group();
    groups.wires.add(tube([[0.48, 0.7, 0.42], [0.3, 0.45, 0.34], [0.02, 0.2, 0.27]], 0.008, wireMat));
    ORDER.forEach(function (band) {
      if (!bands[band]) return;
      var at = ZONES[band].at;
      groups.wires.add(tube([[-0.12, 0.08, 0.25], [(at[0] - 0.12) / 2, (at[1] + 0.08) / 2, 0.2], [at[0], at[1], at[2] + 0.08]], 0.006, wireMat));
    });
    root.add(groups.wires);

    if (opts.cable !== false) {
      var cableMat = new THREE.MeshPhysicalMaterial({ color: 0x1b1c1f, roughness: 0.45, metalness: 0.1, clearcoat: 0.6 });
      var cable = new THREE.Group();
      for (var s = 0; s < 2; s++) {
        var pts = [];
        for (var k = 0; k <= 70; k++) {
          var u = k / 70, ang = u * Math.PI * 1.15;
          var cx = 0.5 - 0.95 * Math.sin(ang) * 0.9 - u * 0.25, cy = 0.84 + 1.1 * Math.sin(ang * 0.5) + u * 0.4, cz = 0.5 - u * 0.7;
          var tw = u * Math.PI * 22 + s * Math.PI;
          pts.push([cx + Math.cos(tw) * 0.02, cy, cz + Math.sin(tw) * 0.02]);
        }
        cable.add(tube(pts, 0.016, cableMat));
      }
      groups.face.add(cable);
    }

    ['shell', 'face', 'pcb', 'tubes', 'wires'].forEach(function (k) { groups[k].userData.home = groups[k].position.clone(); });
    var OUT = { shell: new THREE.Vector3(-0.1, 0.05, -0.85), face: new THREE.Vector3(0.05, -0.05, 1.45), pcb: new THREE.Vector3(0.2, -0.1, 0.85) };

    var state = { explode: 0, focus: null, t: 0, pulse: {} };
    function dimGroup(group, dim) {
      group.traverse(function (o) {
        if (!o.isMesh) return;
        [].concat(o.material).forEach(function (m) {
          if (m.userData.o0 === undefined) { m.userData.o0 = m.opacity; m.userData.t0 = m.transparent; }
          var target = m.userData.o0 * (1 - 0.8 * dim);
          var tr = m.userData.t0 || target < 0.999;
          if (tr !== m.transparent) { m.transparent = tr; m.needsUpdate = true; }
          m.opacity = target;
        });
      });
    }

    var api = {
      root: root, groups: groups, drivers: drivers, bands: bands, total: total,
      setExplode: function (e) {
        state.explode = e;
        var k = ease(e);
        ['shell', 'face', 'pcb'].forEach(function (n) { groups[n].position.copy(groups[n].userData.home).addScaledVector(OUT[n], k); });
        ORDER.forEach(function (b) {
          var g = groups[b];
          g.position.copy(g.userData.home).lerp(g.userData.target, k);
          drivers[b].forEach(function (d) {
            d.position.copy(d.userData.base).lerp(d.userData.spread, k);
            d.rotation.set(lerp(0.15, 0, k), lerp(-0.35, -Math.PI / 2 + 0.35, k), lerp(b === 'high' ? -0.5 : 0.1, 0, k));
          });
        });
        shellMat.opacity = lerp(shellDef.opacity, Math.min(shellDef.opacity, 0.22), k);
        groups.tubes.visible = groups.wires.visible = k < 0.3;
      },
      setFocus: function (band) {
        state.focus = band;
        ORDER.forEach(function (b) { dimGroup(groups[b], band && band !== b ? 1 : 0); });
        dimGroup(groups.pcb, band ? 1 : 0);
        dimGroup(groups.face, band ? 0.9 : 0);
      },
      setShell: function (key) {
        shellDef = SHELLS[key] || shellDef; opts.shell = key;
        shellMat.color.setHex(shellDef.color);
        shellMat.opacity = lerp(shellDef.opacity, Math.min(shellDef.opacity, 0.22), ease(state.explode));
        shellMat.userData.o0 = undefined;
      },
      setFace: function (finish, color) { paintFace(finish, color); },
      // acende os drivers de uma faixa por um instante (usado na assinatura sonora)
      pulse: function (band) { state.pulse[band] = 1; },
      update: function (dt) {
        state.t += dt;
        ORDER.forEach(function (b) {
          var p = state.pulse[b] || 0;
          if (p > 0) state.pulse[b] = Math.max(0, p - dt * 1.4);
          var on = state.focus === b ? 0.9 + 0.3 * Math.sin(state.t * 6) : 0;
          drivers[b].forEach(function (d, i) {
            d.userData.glow.emissiveIntensity = 0.35 + Math.max(on, p * (1.6 + 0.4 * Math.sin(state.t * 30 + i)));
          });
        });
        traceMats.forEach(function (m, i) { m.emissiveIntensity = 0.5 + 0.35 * Math.sin(state.t * 2 + i); });
      },
      anchor: function (band) {
        var g = groups[band]; if (!g || !g.children.length) return null;
        var b = new THREE.Box3().setFromObject(g); return b.getCenter(new THREE.Vector3());
      }
    };
    api.setExplode(0);
    return api;
  }

  /* Molde de silicone do ouvido: concha completa, hélix e o canal até depois da segunda curva,
     com o protetor de espuma (otoblock) e o fio na ponta. */
  function buildImpression(opts) {
    opts = opts || {};
    var root = new THREE.Group();
    var mat = new THREE.MeshPhysicalMaterial({ color: opts.color || 0x36c2a8, roughness: 0.62, metalness: 0, clearcoat: 0.25, clearcoatRoughness: 0.5, transparent: true, opacity: 1, sheen: 0.4, sheenColor: new THREE.Color(0xffffff) });
    var geo = shellGeometry({ canal: 0.86, bend: 1, swell: 0.08, capTop: true });
    var m = new THREE.Mesh(geo, mat);
    root.add(m);
    // otoblock na ponta + fio
    var tipDir = CANAL_DIR.clone().add(new THREE.Vector3(0.45, 0.25, -0.1)).normalize();
    var tip = BODY_END.clone().addScaledVector(CANAL_DIR, 0.42).addScaledVector(tipDir, 0.44);
    var foam = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.13, 32), new THREE.MeshStandardMaterial({ color: 0xf2efe6, roughness: 0.95, transparent: true, opacity: 1 }));
    foam.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tipDir);
    foam.position.copy(tip).addScaledVector(tipDir, 0.03);
    root.add(foam);
    var threadPts = [];
    for (var i = 0; i <= 30; i++) {
      var u = i / 30;
      threadPts.push(new THREE.Vector3(tip.x - u * 0.9, tip.y + Math.sin(u * 3) * 0.25 + u * 0.4, tip.z + u * 0.9));
    }
    var thread = tube(threadPts.map(function (p) { return [p.x, p.y, p.z]; }), 0.008, new THREE.MeshStandardMaterial({ color: 0x2f6fd6, roughness: 0.6, transparent: true, opacity: 1 }));
    root.add(thread);
    // ondulações de silicone na superfície
    var wire = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x7ff5df, wireframe: true, transparent: true, opacity: 0 }));
    root.add(wire);
    return {
      root: root, mats: [mat, foam.material, thread.material], wire: wire, mesh: m,
      setOpacity: function (o) { [mat, foam.material, thread.material].forEach(function (mm) { mm.opacity = o; mm.depthWrite = o > 0.6; }); root.visible = o > 0.01 || wire.material.opacity > 0.01; },
      setWire: function (o) { wire.material.opacity = o; root.visible = o > 0.01 || mat.opacity > 0.01; }
    };
  }

  function studioEnvironment(renderer) {
    var pm = new THREE.PMREMGenerator(renderer);
    var env = new THREE.Scene();
    env.add(new THREE.Mesh(new THREE.BoxGeometry(20, 20, 20), new THREE.MeshBasicMaterial({ color: 0x0c0d10, side: THREE.BackSide })));
    function soft(w, h, x, y, z, c, ry, rx) {
      var m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide }));
      m.position.set(x, y, z); m.rotation.y = ry || 0; m.rotation.x = rx || 0; env.add(m);
    }
    soft(8, 3, 0, 7, 0, 0xffffff, 0, Math.PI / 2);
    soft(3, 6, -8, 1, 2, 0xfff1dc, Math.PI / 2);
    soft(3, 6, 8, 0, -2, 0xc9dbff, -Math.PI / 2);
    soft(6, 2, 0, -1, 9, 0xffffff, 0);
    var rt = pm.fromScene(env, 0.03); pm.dispose();
    return rt.texture;
  }

  function webglOk() {
    try { var c = document.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl'))); } catch (e) { return false; }
  }

  /* Palco: renderer + câmera + luzes + pivô que gira com arrasto (com inércia) e um loop que
     só roda com o canvas visível. */
  function stage(canvas, o) {
    o = o || {};
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, preserveDrawingBuffer: !!o.preserve });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, innerWidth < 768 ? 1.5 : 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = o.exposure || 1.35;
    var scene = new THREE.Scene();
    scene.environment = studioEnvironment(renderer);
    var cam = new THREE.PerspectiveCamera(o.fov || 30, 1, 0.1, 60);
    var key = new THREE.DirectionalLight(0xfff3e0, 2.3); key.position.set(-3, 4, 5); scene.add(key);
    var rim = new THREE.DirectionalLight(0xc9dbff, 1.8); rim.position.set(4, 1, -4); scene.add(rim);
    var fill = new THREE.PointLight(0xffffff, 1.4, 8, 2); fill.position.set(1.4, -0.6, 2); scene.add(fill);
    scene.add(new THREE.HemisphereLight(0x8899aa, 0x111111, 0.55));
    var pivot = new THREE.Group(); scene.add(pivot);
    var spin = new THREE.Group(); pivot.add(spin);

    var st = { rx: o.rx || 0.15, ry: o.ry || -0.6, vx: 0, vy: 0, drag: false, lx: 0, ly: 0, auto: o.auto !== false, idle: 0, visible: true, dist: o.dist || 9 };
    var tickers = [];
    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      cam.aspect = w / h;
      var fit = o.fit || 1.0;
      cam.position.set(0, 0, st.dist * (w / h < 0.8 ? 1.25 : 1) / fit);
      cam.lookAt(0, 0, 0); cam.updateProjectionMatrix();
    }
    if (o.drag !== false) {
      canvas.style.touchAction = 'pan-y';
      canvas.addEventListener('pointerdown', function (e) { st.drag = true; st.lx = e.clientX; st.ly = e.clientY; st.idle = 0; canvas.classList.add('is-drag'); });
      window.addEventListener('pointermove', function (e) {
        if (!st.drag) return;
        var dx = e.clientX - st.lx, dy = e.clientY - st.ly; st.lx = e.clientX; st.ly = e.clientY;
        st.vy = dx * 0.008; st.vx = dy * 0.005; st.ry += st.vy; st.rx = clamp(st.rx + st.vx, -0.9, 0.9);
      });
      window.addEventListener('pointerup', function () { st.drag = false; canvas.classList.remove('is-drag'); });
    }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { st.visible = en[0].isIntersecting; }).observe(canvas);
    window.addEventListener('resize', resize);
    var clock = new THREE.Clock();
    function loop() {
      requestAnimationFrame(loop);
      if (!st.visible) { clock.getDelta(); return; }
      var dt = Math.min(clock.getDelta(), 0.05);
      if (!st.drag) {
        st.idle += dt;
        st.vy *= 0.94; st.vx *= 0.9;
        st.ry += st.vy; st.rx = clamp(st.rx + st.vx, -0.9, 0.9);
        if (st.auto && st.idle > 1.5) st.ry += dt * 0.25;
      }
      spin.rotation.set(st.rx, st.ry, 0);
      tickers.forEach(function (f) { f(dt); });
      renderer.render(scene, cam);
    }
    resize();
    return {
      renderer: renderer, scene: scene, camera: cam, pivot: pivot, spin: spin, state: st, resize: resize,
      onTick: function (f) { tickers.push(f); }, start: function () { resize(); loop(); },
      renderOnce: function () { spin.rotation.set(st.rx, st.ry, 0); tickers.forEach(function (f) { f(0); }); renderer.render(scene, cam); }
    };
  }

  // centraliza o fone no palco
  function center(obj) {
    var b = new THREE.Box3().setFromObject(obj), c = b.getCenter(new THREE.Vector3());
    obj.position.sub(c);
    return b.getSize(new THREE.Vector3());
  }

  function loadLogo(src, cb) {
    var img = new Image();
    img.onload = img.onerror = function () { cb(img); };
    img.src = src;
  }

  global.XE3D = {
    BANDS: BANDS, ORDER: ORDER, SHELLS: SHELLS, FINISHES: FINISHES, FACE_COLORS: FACE_COLORS,
    buildIEM: buildIEM, buildImpression: buildImpression, stage: stage, center: center, loadLogo: loadLogo,
    webglOk: webglOk, ease: ease, clamp: clamp, lerp: lerp
  };
})(window);
