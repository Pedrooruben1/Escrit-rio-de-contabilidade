// bem.contado: desenhos que se desenham ao aparecer, conversa escrita letra a letra e contador anónimo.
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
  const reduzir = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const alvos = document.querySelectorAll('.hero, .bloco, .conversa');

  // Traços desenhados à mão: mede o comprimento real de cada um e esconde-o com um tracejado desse tamanho.
  // Quando a secção aparece, o tracejado desliza e o traço desenha-se (a transição está no CSS).
  const tracos = [...document.querySelectorAll('.tr')];
  if (!reduzir) {
    tracos.forEach(t => { try { const L = Math.ceil(t.getTotalLength()) + 2; t.style.strokeDasharray = L; t.style.strokeDashoffset = L; } catch (e) {} });
  }
  document.documentElement.classList.add('medido');
  const desenhar = sec => sec.querySelectorAll('.tr').forEach(t => { t.style.strokeDashoffset = 0; });

  // Conversa: escreve a pergunta e depois a resposta, uma vez, quando a secção aparece.
  const conversa = () => {
    if (reduzir) return;
    const falas = [...document.querySelectorAll('.dialogo .falado')];
    const resposta = document.querySelector('.bolha.resposta');
    // guarda a altura final para a página não saltar enquanto o texto é escrito
    document.querySelectorAll('.dialogo .bolha').forEach(b => { b.style.width = b.offsetWidth + 'px'; });
    falas.forEach(f => { f.style.minHeight = f.offsetHeight + 'px'; f.dataset.final = f.textContent; f.textContent = ''; });
    resposta.classList.add('espera');
    const escrever = (el, depois) => {
      const texto = el.dataset.final; let i = 0;
      el.classList.add('escrevendo');
      const t = setInterval(() => {
        el.textContent = texto.slice(0, ++i);
        if (i >= texto.length) { clearInterval(t); el.classList.remove('escrevendo'); if (depois) setTimeout(depois, 700); }
      }, 36);
    };
    setTimeout(() => escrever(falas[0], () => { resposta.classList.remove('espera'); escrever(falas[1]); }), 500);
  };

  if (reduzir || !('IntersectionObserver' in window)) {
    alvos.forEach(a => { a.classList.add('visivel'); if (!reduzir) desenhar(a); });
  } else {
    const io = new IntersectionObserver(entradas => entradas.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('visivel'); desenhar(e.target); io.unobserve(e.target);
      if (e.target.classList.contains('conversa')) conversa();
    }), { threshold: 0.3 });
    alvos.forEach(a => io.observe(a));
  }

  // Contador anónimo (GoatCounter da bem.contado, sem cookies). Só no endereço oficial.
  if (/^(www\.)?bemcontadopt\.pt$/.test(location.hostname)) {
    const enviar = params => {
      const url = 'https://bemcontadopt.goatcounter.com/count?' + new URLSearchParams({ ...params, rnd: Math.random().toString(36).slice(2) });
      try { if (navigator.sendBeacon && navigator.sendBeacon(url)) return; } catch (e) {}
      try { new Image().src = url; } catch (e) {}
    };
    enviar({ p: location.pathname || '/', t: document.title, r: document.referrer || '' });
    document.addEventListener('click', ev => {
      const el = ev.target.closest('[data-contar]');
      if (el) enviar({ p: '/site/' + el.dataset.contar, t: el.dataset.contar, e: 'true' });
    });
  }
});
