/* "Os teus prazos": filtra calendario.json pelo caso escolhido e aponta para o .ics certo.
   O caso fica guardado só neste browser (localStorage), sem cookies e sem sair do aparelho.
   As etiquetas seguem a mesma regra que etiquetas_do_perfil() em scripts/site_atualizar.py. */
(function () {
  var DIAS = ["dom", "seg", "ter", "qua", "qui", "sex", "sáb"];
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  var MESES_CURTOS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
  var IVA = { x: "iva_isento", t: "iva_trimestral", m: "iva_mensal" };
  var CHAVE = "bemcontado-perfil";
  var dados = null;

  function perfil(form) {
    var s = form.querySelector('input[name="s"]:checked').value;
    var i = form.querySelector('input[name="i"]:checked').value;
    var t = form.t.checked ? 1 : 0;
    if (s === "p") { i = "x"; t = 0; }
    return { s: s, i: i, t: t, c: form.c.checked ? 1 : 0, h: form.h.checked ? 1 : 0 };
  }

  function etiquetas(p) {
    var et = {};
    if (p.c) et.carro = 1;
    if (p.h) et.casa = 1;
    if (p.s !== "p") {
      et.atividade = 1; et[IVA[p.i]] = 1;
      if (p.s === "s" || p.s === "o") et.independente = 1;
      if (p.s === "o" || p.s === "e") et.retencao = 1;
      if (p.s === "e") et.empresa = 1;
      if (p.t) { et.empregador = 1; et.retencao = 1; }
    }
    return et;
  }

  function el(tag, cls, texto) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (texto != null) n.textContent = texto;
    return n;
  }

  function hoje() {
    var d = new Date();
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  }

  function desenhar(form) {
    var p = perfil(form);
    var et = etiquetas(p);
    var caixa = document.getElementById("lista-teus");
    form.classList.toggle("particular", p.s === "p");
    try { localStorage.setItem(CHAVE, JSON.stringify(p)); } catch (e) {}

    var nome = p.s + p.i + p.t + p.c + p.h + ".ics";
    var url = "https://bemcontadopt.pt/prazos/ics/" + nome;
    document.getElementById("cal-ics").href = "ics/" + nome;
    var webcal = "webcal://bemcontadopt.pt/prazos/ics/" + nome;
    document.getElementById("cal-sub").href = webcal;
    document.getElementById("cal-google").href = "https://calendar.google.com/calendar/render?cid=" + encodeURIComponent(webcal);
    document.getElementById("cal-outlook").href = "https://outlook.live.com/calendar/0/addfromweb?url=" + encodeURIComponent(url) + "&name=" + encodeURIComponent("Prazos (bem.contado)");
    document.getElementById("cal-copiar").dataset.url = url;

    caixa.textContent = "";
    if (!dados) return;
    var h = hoje();
    var meus = dados.prazos.filter(function (x) {
      return x.data >= h && x.quem.some(function (q) { return et[q]; });
    });
    var fim = new Date(dados.ate + "T12:00:00");
    var ateTxt = fim.getDate() + " de " + MESES[fim.getMonth()];
    if (!meus.length) {
      caixa.appendChild(el("p", "vazio", "Não há prazos para o teu caso até " + ateTxt + "."));
    } else {
      var mesAtual = "", lista = null;
      meus.forEach(function (x) {
        var d = new Date(x.data + "T12:00:00");
        var m = MESES[d.getMonth()] + " de " + d.getFullYear();
        if (m !== mesAtual) {
          mesAtual = m;
          caixa.appendChild(el("h3", "mes-titulo", m.charAt(0).toUpperCase() + m.slice(1)));
          lista = el("ol", "prazos");
          caixa.appendChild(lista);
        }
        var li = el("li", "prazo");
        var dia = el("p", "dia");
        dia.appendChild(el("span", "semana", DIAS[d.getDay()]));
        dia.appendChild(el("span", "numero", String(d.getDate())));
        dia.appendChild(el("span", "mes", MESES_CURTOS[d.getMonth()]));
        var corpo = el("div");
        corpo.appendChild(el("h4", null, x.titulo));
        corpo.appendChild(el("p", null, x.descricao));
        if (x.nota) corpo.appendChild(el("p", "nota-prazo", x.nota));
        li.appendChild(dia); li.appendChild(corpo);
        lista.appendChild(li);
      });
    }
    var rodape = "A lista vai até " + ateTxt + ".";
    if (dados.falta) rodape += " " + dados.falta;
    caixa.appendChild(el("p", "pequeno", rodape));
  }

  function iniciar() {
    var form = document.getElementById("perfil");
    if (!form) return;
    try {
      var g = JSON.parse(localStorage.getItem(CHAVE) || "null");
      if (g) {
        var r = form.querySelector('input[name="s"][value="' + g.s + '"]'); if (r) r.checked = true;
        r = form.querySelector('input[name="i"][value="' + g.i + '"]'); if (r) r.checked = true;
        form.t.checked = !!g.t; form.c.checked = !!g.c; form.h.checked = !!g.h;
      }
    } catch (e) {}
    form.addEventListener("change", function () { desenhar(form); });
    document.getElementById("cal-copiar").addEventListener("click", function () {
      var b = this, url = b.dataset.url, antes = "copia o endereço";
      function feito(txt) { b.textContent = txt; setTimeout(function () { b.textContent = antes; }, 2500); }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { feito("endereço copiado"); }, function () { window.prompt("Copia este endereço:", url); });
      else window.prompt("Copia este endereço:", url);
    });
    document.getElementById("cal").hidden = false;
    desenhar(form);
    fetch("calendario.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (j) {
      dados = j; desenhar(form);
    }).catch(function () {
      document.getElementById("lista-teus").appendChild(el("p", "vazio", "Não foi possível carregar a lista. Tenta recarregar a página."));
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
