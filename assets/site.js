(function(){
  "use strict";

  var WHATS = "5511950295494";

  var $ = function(id){ return document.getElementById(id); };

  /* ---------- menu mobile ---------- */
  var burger = $('burger');
  var drawer = $('drawer');
  if(burger && drawer){
  function closeDrawer(){
    burger.setAttribute('aria-expanded','false');
    drawer.classList.remove('open');
    document.body.classList.remove('is-locked');
  }
  burger.addEventListener('click', function(){
    var open = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!open));
    drawer.classList.toggle('open', !open);
    document.body.classList.toggle('is-locked', !open);
  });
  drawer.addEventListener('click', function(e){ if(e.target.tagName === 'A') closeDrawer(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeDrawer(); });
  }

  /* ---------- reveal ---------- */
  var rvs = document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, {rootMargin:'240px 0px 240px 0px', threshold:0});
    rvs.forEach(function(el, i){ el.style.transitionDelay = (Math.min(i % 4, 3) * 50) + 'ms'; io.observe(el); });
  } else {
    rvs.forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- faq ---------- */
  document.querySelectorAll('.fq').forEach(function(btn){
    var panel = btn.nextElementSibling;
    btn.addEventListener('click', function(){
      var open = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.fq').forEach(function(other){
        if(other !== btn){ other.setAttribute('aria-expanded','false'); other.nextElementSibling.style.maxHeight = null; }
      });
      btn.setAttribute('aria-expanded', String(!open));
      panel.style.maxHeight = open ? null : (panel.scrollHeight + 'px');
    });
  });

  /* ---------- quiz (só na home) ---------- */
  if($('quiz')){
  var CAT = {
    'one':    {nome:'XE ONE+/PRO',    preco:'A partir de R$ 2.690',  area:'Grave',
               txt:'Cada faixa no seu driver: o bumbo para de embolar com o baixo. A saída do universal, pra baterista, baixista e guitarrista.'},
    'onemax': {nome:'XE ONEMAX/PRO',  preco:'A partir de R$ 3.990',  area:'Agudo e detalhe',
               txt:'Agudo cristalino sem o brilho que cansa, grave aveludado por baixo. Técnico de som, vocalista e tecladista.'},
    'xe3':    {nome:'XE3/PRO',        preco:'A partir de R$ 4.280',  area:'Grave',
               txt:'O rei do punch. Bate no peito e sobra fôlego quando a banda sobe no refrão. Baterista e baixista.'},
    'xe4':    {nome:'XE4/PRO',        preco:'A partir de R$ 4.680',  area:'Médio',
               txt:'Flat de verdade: sua voz sai do retorno como entrou no microfone. Vocalista, técnico de som e guitarrista.'},
    'xe5':    {nome:'XE5/PRO',        preco:'A partir de R$ 5.290',  area:'Médio',
               txt:'Guitarra com corpo sem comer o vocal. Serve o palco à noite e a referência no estúdio no dia seguinte.'},
    'xe6':    {nome:'XE6/PRO',        preco:'A partir de R$ 5.890',  area:'Grave',
               txt:'O peso do XE3 com leitura fina do kit: dá pra ouvir a diferença entre a mão e a baqueta.'},
    'xe8':    {nome:'XE8/PRO',        preco:'A partir de R$ 7.890',  area:'Médio',
               txt:'Quatro drivers só pro grave e o médio ainda na frente. Show grande, naipe de sopro, teclado em camadas.'},
    'xe12':   {nome:'XE12/PRO',       preco:'A partir de R$ 11.890', area:'Agudo e detalhe',
               txt:'Quatro vias de verdade: cada instrumento com lugar próprio no palco sonoro. O problema aparece na hora.'},
    'xe14':   {nome:'XE14/PRO',       preco:'A partir de R$ 18.990', area:'Agudo e detalhe',
               txt:'Seis drivers só pros médios e extensão até 50 kHz. O que você escuta é o que está na gravação.'}
  };
  var Q2 = {
    palco: {
      titulo:'Qual sonoridade você precisa no seu retorno?',
      opcoes:[
        {v:'punch',    b:'Graves com punch',           s:'Bateristas, baixistas, DJs'},
        {v:'clareza',  b:'Clareza nos médios e agudos', s:'Vocais e guitarras'},
        {v:'equilibrio', b:'Equilíbrio total',          s:'Tecladistas e técnicos de som'}
      ]
    },
    estudio: {
      titulo:'Qual característica é mais importante na sua produção?',
      opcoes:[
        {v:'flat',     b:'Resposta plana (flat)',  s:'Análise crítica e mixagem precisa'},
        {v:'detalhe',  b:'Riqueza de detalhes',    s:'Ouvir todas as nuances e texturas'},
        {v:'extremos', b:'Extensão nos extremos',  s:'Graves profundos e agudos cristalinos'}
      ]
    },
    hifi: {
      titulo:'O que você mais valoriza em uma experiência sonora?',
      opcoes:[
        {v:'musical',  b:'Musicalidade e emoção',  s:'Um som rico, texturizado e envolvente'},
        {v:'precisao', b:'Precisão analítica',     s:'Ouvir a gravação como ela foi feita'},
        {v:'palco',    b:'Palco sonoro e imersão', s:'Sentir a música ao seu redor'}
      ]
    }
  };

  /* perfil + característica -> trilha de modelos por nível */
  /* perfil + caracteristica -> trilha de 3 modelos (essencial, alta, referencia).
     Cada trilha fica dentro da area que a resposta indica, pra nao contradizer
     a secao de modelos: grave = one/xe3/xe6, medio = xe4/xe5/xe8,
     agudo = onemax/xe12/xe14. */
  var TRILHAS = {
    'palco|punch':        ['one','xe3','xe6'],      // grave
    'palco|clareza':      ['xe4','xe5','xe8'],      // medio
    'palco|equilibrio':   ['xe4','xe8','xe12'],     // medio -> agudo
    'estudio|flat':       ['xe4','xe5','xe8'],      // medio
    'estudio|detalhe':    ['onemax','xe12','xe14'], // agudo
    'estudio|extremos':   ['xe8','xe12','xe14'],    // grave articulado -> agudo
    'hifi|musical':       ['onemax','xe8','xe12'],
    'hifi|precisao':      ['xe4','xe12','xe14'],
    'hifi|palco':         ['xe6','xe12','xe14']
  };  var NIVEL = {essencial:0, alta:1, referencia:2};
  var LABEL_PERFIL = {palco:'monitoramento de palco', estudio:'produção em estúdio', hifi:'audição de alta fidelidade'};

  var resp = {};
  var steps = document.querySelectorAll('.quiz-step');
  var result = $('quizResult');
  var bar = $('quizBar');
  var label = $('quizLabel');

  function showStep(n){
    steps.forEach(function(s){ s.classList.toggle('active', Number(s.dataset.step) === n); });
    result.classList.remove('active');
    bar.style.width = (n / 3 * 100) + '%';
    label.textContent = 'Passo ' + n + ' de 3';
  }

  function buildQ2(){
    var cfg = Q2[resp[1]];
    $('q2Title').textContent = cfg.titulo;
    var box = $('q2Opts');
    box.innerHTML = '';
    cfg.opcoes.forEach(function(o){
      var el = document.createElement('button');
      el.className = 'opt';
      el.type = 'button';
      el.dataset.q = '2';
      el.dataset.v = o.v;
      el.innerHTML = '<b>' + o.b + '</b><small>' + o.s + '</small>';
      box.appendChild(el);
    });
  }

  function render(){
    var trilha = TRILHAS[resp[1] + '|' + resp[2]] || ['xe4','xe5','xe12'];
    var idx = NIVEL[resp[3]] || 0;
    var principal = CAT[trilha[idx]];
    var alt = CAT[trilha[idx === 2 ? 1 : idx + 1]];

    var grid = $('resultGrid');
    grid.innerHTML =
      '<article class="result-card lead"><span class="result-badge">Recomendado para você · área ' + principal.area + '</span>' +
        '<h4>' + principal.nome + '</h4><p class="result-price">' + principal.preco + '</p><p>' + principal.txt + '</p></article>' +
      '<article class="result-card"><span class="result-badge">Também vale ouvir · área ' + alt.area + '</span>' +
        '<h4>' + alt.nome + '</h4><p class="result-price">' + alt.preco + '</p><p>' + alt.txt + '</p></article>';

    var msg = 'Olá! Fiz o teste no site da Xtreme Ears.\n\n' +
              '• Objetivo: ' + LABEL_PERFIL[resp[1]] + '\n' +
              '• Modelos sugeridos: ' + principal.nome + ' e ' + alt.nome + '\n\n' +
              'Queria entender melhor qual faz mais sentido pra mim e como funciona o processo do pré-molde.';
    $('quizWhats').href = 'https://wa.me/' + WHATS + '?text=' + encodeURIComponent(msg);

    steps.forEach(function(s){ s.classList.remove('active'); });
    result.classList.add('active');
    bar.style.width = '100%';
    label.textContent = 'Resultado';
  }

  $('quiz').addEventListener('click', function(e){
    var opt = e.target.closest('.opt');
    if(opt){
      var q = Number(opt.dataset.q);
      resp[q] = opt.dataset.v;
      if(q === 1){ buildQ2(); showStep(2); }
      else if(q === 2){ showStep(3); }
      else { render(); }
      return;
    }
    var back = e.target.closest('.quiz-back');
    if(back) showStep(Number(back.dataset.back));
  });

  $('quizRestart').addEventListener('click', function(){
    resp = {};
    showStep(1);
  });

  showStep(1);
  }

  /* ---------- cards -> pré-seleciona o modelo no formulário ---------- */
  if($('f-modelo')){
  document.querySelectorAll('[data-model]').forEach(function(a){
    a.addEventListener('click', function(){
      var sel = document.getElementById('f-modelo');
      var alvo = a.dataset.model;
      var achou = Array.prototype.some.call(sel.options, function(o){
        if(o.text === alvo){ sel.value = o.value; return true; }
        return false;
      });
      if(!achou && /universal/i.test(alvo)) sel.value = 'Linha universal';
      sel.dataset.detalhe = alvo;
    });
  });
  }

  /* ---------- formulário -> WhatsApp com a mensagem pronta ---------- */
  if($('leadForm')) $('leadForm').addEventListener('submit', function(e){
    e.preventDefault();
    var f = e.target;
    var nome = f.nome.value.trim();
    if(!nome){ f.nome.focus(); return; }

    var sel = f.modelo;
    var modelo = sel.dataset.detalhe || sel.value;

    var linhas = ['Olá! Vim pelo site da Xtreme Ears e queria falar com um especialista.', ''];
    linhas.push('• Nome: ' + nome);
    if(f.cidade.value.trim()) linhas.push('• Cidade: ' + f.cidade.value.trim());
    if(f.perfil.value)        linhas.push('• Perfil: ' + f.perfil.value);
    linhas.push('• Modelo de interesse: ' + (modelo || 'ainda não sei, quero orientação'));
    if(f.uso.value.trim())    linhas.push('• Uso: ' + f.uso.value.trim());

    window.open('https://wa.me/' + WHATS + '?text=' + encodeURIComponent(linhas.join('\n')), '_blank', 'noopener');
  });

  /* ---------- CTAs levam ao formulário com o campo pronto ---------- */
  document.querySelectorAll('[data-cta]').forEach(function(el){
    if(el.dataset.cta === 'quiz') return;
    el.addEventListener('click', function(){
      var campo = document.getElementById('f-nome');
      if(campo) setTimeout(function(){ campo.focus({preventScroll:true}); }, 700);
    });
  });

  /* ---------- botão flutuante ---------- */
  var float = $('float');
  var leadSec = $('falar');
  if(float && leadSec) window.addEventListener('scroll', function(){
    var passouHero = window.scrollY > window.innerHeight * .7;
    var noForm = leadSec.getBoundingClientRect().top < window.innerHeight * .8 &&
                 leadSec.getBoundingClientRect().bottom > 0;
    float.classList.toggle('show', passouHero && !noForm);
  }, {passive:true});


  /* ==================================================================
     HERO EM VIDEO
     Ordem de preferencia:
       1. assets/hero.mp4 — arquivo proprio, sem marca de terceiro
       2. YouTube do canal oficial, mudo e em loop, como fundo
       3. a foto (poster), que fica sempre atras dos dois
     O video so aparece quando REALMENTE comeca a tocar; se o navegador
     bloquear o autoplay, a foto continua no lugar e ninguem ve buraco.
     ================================================================== */
  /* Rodizio de artistas no fundo da hero.
     Duas regras pra entrar aqui:
       1. SO 16:9. O player do YouTube encaixota o que nao for widescreen,
          e no fundo da hero essa tarja preta aparece nas laterais. O video
          do Fabiano Manhas em 4:3 (G6BkVSKdvz8) saiu por isso; entrou a
          versao 16:9 do mesmo artista. Confira antes de adicionar:
          curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=ID&format=json"
          e veja se width/height da ~1.77.
       2. Footage de palco. Card de titulo e entrevista sentada viram tela
          parada como fundo (Lexa, Kiko Freitas, Hananiel, PJ, Junior
          Carelli, Johnny Essi, Guilherme Fahl ficaram de fora por isso).
     `t` = segundo onde comecar, pra pular vinheta de abertura.
     Capital Inicial nao existe no canal: o Dinho so tem reel no Instagram. */
  var HERO_VIDEOS = [
    // zoom: medido do proprio quadro do video (ver README). Valor minimo pra
    // tarja sair do enquadramento, com uma folga pequena.
    {id:'PI09H57rC9k', quem:'Lauana Prado',     t:5, zoom:1.24},
    {id:'cwc_h8WMzkw', quem:'Aquiles Priester', t:8, zoom:1.05},
    {id:'DpMVZTAPBz4', quem:'Bruno Graveto',    t:8, zoom:1.36},
    {id:'QbDrR2BFitE', quem:'Fabiano Manhas',   t:6, zoom:1.40},
    {id:'tIrMgNO4Ljk', quem:'Marcelo Falcão',   t:5, zoom:1.47},
    {id:'0LAQgR3c9YU', quem:'Wesley Safadão',   t:5, zoom:1.48}
  ];

  var SEGUNDOS = 13;          // quanto cada artista fica no ar
  var atual = Math.floor(Math.random() * HERO_VIDEOS.length);   // nao comeca sempre igual
  var playerHero = null, troca = null;

  var elVideo = document.querySelector('.hero-video');
  var elYt    = $('heroYt');

  var economiza = (navigator.connection && (navigator.connection.saveData ||
                   /2g/.test(navigator.connection.effectiveType || ''))) ||
                  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function creditar(){
    var c = $('heroCredito');
    if(c) c.textContent = HERO_VIDEOS[atual].quem;
    elYt.style.setProperty('--zoom', HERO_VIDEOS[atual].zoom);
  }

  function proximo(){
    if(!playerHero || !playerHero.loadVideoById) return;
    atual = (atual + 1) % HERO_VIDEOS.length;
    try {
      playerHero.loadVideoById({videoId: HERO_VIDEOS[atual].id,
                                startSeconds: HERO_VIDEOS[atual].t});
      playerHero.mute();
    } catch(e){}
  }

  function fundoYoutube(){
    if(!elYt || economiza || elYt.firstChild) return;
    elYt.appendChild(document.createElement('div'));   // marca que ja comecou

    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);

    elYt.style.setProperty('--zoom', HERO_VIDEOS[atual].zoom);

    window.onYouTubeIframeAPIReady = function(){
      playerHero = new YT.Player(elYt.firstChild, {
        videoId: HERO_VIDEOS[atual].id,
        playerVars: {
          autoplay:1, mute:1, controls:0, start:HERO_VIDEOS[atual].t,
          modestbranding:1, playsinline:1, rel:0, disablekb:1,
          iv_load_policy:3, fs:0
        },
        events: {
          onReady: function(ev){ tocar(ev.target); },
          onStateChange: function(ev){
            if(ev.data === YT.PlayerState.PLAYING){
              elYt.classList.add('ok');
              creditar();
              clearTimeout(troca);
              troca = setTimeout(proximo, SEGUNDOS * 1000);
            }
            if(ev.data === YT.PlayerState.ENDED) proximo();
          },
          // video removido ou com embed bloqueado: pula pro proximo artista
          onError: function(){ proximo(); }
        }
      });
    };
  }

  function tocar(player){
    player.mute();
    var tentativas = 0;
    var t = setInterval(function(){
      if(elYt.classList.contains('ok') || ++tentativas > 6) return clearInterval(t);
      try { player.playVideo(); } catch(e){ clearInterval(t); }
    }, 700);

    var gestos = ['pointerdown','keydown','touchstart','scroll'];
    function noGesto(){
      if(!elYt.classList.contains('ok')){ try { player.mute(); player.playVideo(); } catch(e){} }
      gestos.forEach(function(g){ window.removeEventListener(g, noGesto); });
    }
    gestos.forEach(function(g){ window.addEventListener(g, noGesto, {once:false, passive:true}); });
  }

  if(elVideo && !economiza){
    // se o mp4 proprio existir, ele ganha: sem marca do YouTube e mais leve
    elVideo.addEventListener('playing', function(){ elVideo.classList.add('ok'); });
    elVideo.addEventListener('error', fundoYoutube, true);
    var p = elVideo.play();
    if(p && p.catch) p.catch(fundoYoutube);
    // navegador que nem tenta carregar a fonte nao dispara error: confere depois
    setTimeout(function(){
      if(!elVideo.classList.contains('ok') && !elYt.firstChild) fundoYoutube();
    }, 1800);
  } else {
    fundoYoutube();
  }

  /* ---------- player da hero: abre o video completo, com som ---------- */
  var play = $('heroPlay'), modal = $('modalVideo'), corpo = $('modalCorpo'),
      fechar = $('modalClose'), aberto = false;

  function abreModal(){
    var v = HERO_VIDEOS[atual];
    clearTimeout(troca);                       // nao troca o fundo com o modal aberto
    corpo.innerHTML = '<div class="modal-video"><iframe src="https://www.youtube-nocookie.com/embed/' +
      v.id + '?autoplay=1&rel=0&modestbranding=1&playsinline=1" ' +
      'title="' + v.quem + ' &amp; Xtreme Ears" allow="accelerometer; autoplay; encrypted-media; picture-in-picture" ' +
      'allowfullscreen></iframe></div>';
    modal.classList.add('aberto');
    document.body.classList.add('is-locked');
    aberto = true;
    fechar.focus();
  }

  function fechaModal(){
    modal.classList.remove('aberto');
    document.body.classList.remove('is-locked');
    corpo.innerHTML = '';          // para o audio ao fechar
    aberto = false;
    troca = setTimeout(proximo, SEGUNDOS * 1000);
    if(play) play.focus();
  }

  if(play && modal){
    play.addEventListener('click', abreModal);
    fechar.addEventListener('click', fechaModal);
    modal.addEventListener('click', function(e){ if(e.target === modal) fechaModal(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && aberto) fechaModal(); });
  }

  function processaEmbeds(){
    if(window.instgrm && window.instgrm.Embeds) window.instgrm.Embeds.process();
  }

  /* ---------- reels da prova social ---------- */
  if(document.querySelector('.reels .instagram-media')){
    var n = 0;
    var tr = setInterval(function(){
      processaEmbeds();
      if(++n > 15) clearInterval(tr);
    }, 500);
  }

  /* ---------- personalizador de faceplate ---------- */
  var fonePerso = $('fonePerso'), corNome = $('corNome');
  if(fonePerso){
    var sombra = 'drop-shadow(0 16px 26px rgba(0,0,0,.7))';
    document.querySelectorAll('.cor').forEach(function(b){
      b.addEventListener('click', function(){
        var f = b.dataset.filtro;
        fonePerso.style.filter = (f === 'none' ? '' : f + ' ') + sombra;
        if(corNome) corNome.textContent = b.dataset.nome;
        document.querySelectorAll('.cor').forEach(function(o){
          o.setAttribute('aria-pressed', String(o === b));
        });
      });
    });
  }

  /* ---------- ano ---------- */
  if($('ano')) $('ano').textContent = new Date().getFullYear();
})();
