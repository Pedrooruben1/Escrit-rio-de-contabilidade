(function () {
  function euros(v) {
    var neg = v < 0, c = Math.round(Math.abs(v) * 100), int = String(Math.floor(c / 100)), dec = ("0" + (c % 100)).slice(-2);
    return (neg ? "-" : "") + int.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + dec;
  }
  function lerEuros(t) {
    var s = String(t).trim().replace(/[\s€]/g, "");
    if (s.indexOf(",") > -1) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, "");
    var v = parseFloat(s);
    return isFinite(v) && v > 0 ? v : 0;
  }
  function pct(v) { return (Math.round(v * 1000) / 10).toFixed(1).replace(".", ",") + " %"; }

  function iniciar() {
    var $ = function (id) { return document.getElementById(id); };
    var f = $("calc-sal");
    if (!f || typeof SALARIO === "undefined") return;
    var q = new URLSearchParams(location.search);

    // escolha do modo
    function mostrar(modo) {
      $("modo-c").hidden = modo !== "c";
      $("modo-r").hidden = modo !== "r";
      document.documentElement.setAttribute("data-modo", modo);
      document.dispatchEvent(new Event("modo-mudou"));
    }
    var inicial = q.get("modo") || (q.has("m") ? "r" : null);
    document.querySelectorAll('input[name="modo"]').forEach(function (r) {
      if (r.value === inicial) r.checked = true;
      r.addEventListener("change", function () {
        mostrar(r.value);
        var alvo = $(r.value === "c" ? "modo-c" : "modo-r");
        if (alvo && alvo.scrollIntoView) alvo.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
    if (inicial) mostrar(inicial);

    // valores da ligação: ?modo=c&b=1500&u=0&v=6.15&n=22&f=dinheiro&e=n&k=0&j=0
    function marcar(nome, v) { var r = f.querySelector('input[name="' + nome + '"][value="' + v + '"]'); if (r) r.checked = true; }
    if (q.get("modo") === "c") {
      if (q.has("b")) $("s-base").value = q.get("b");
      if (q.has("v")) $("s-ref").value = q.get("v");
      if (q.has("n")) $("s-dias").value = q.get("n");
      if (q.has("u")) marcar("s-duod", q.get("u"));
      if (q.has("f")) marcar("s-forma", q.get("f"));
      if (q.has("e")) marcar("s-sit", q.get("e"));
      if (q.has("k")) $("s-dep").value = q.get("k");
      if (q.has("j") && q.get("j") !== "0") { $("s-jovem-sim").checked = true; $("s-jovem-ano").value = q.get("j"); }
    }
    ["s-base", "s-ref"].forEach(function (id) {
      var c = $(id);
      c.value = euros(lerEuros(c.value));
      c.addEventListener("blur", function () { c.value = euros(lerEuros(c.value)); });
      c.addEventListener("focus", function () { c.select(); });
    });
    function val(nome) { var r = f.querySelector('input[name="' + nome + '"]:checked'); return r ? r.value : null; }

    function dados() {
      return { base: lerEuros($("s-base").value), duodecimos: val("s-duod") === "1", refeicao: lerEuros($("s-ref").value),
               dias: Math.min(31, Math.round(lerEuros($("s-dias").value))), forma: val("s-forma"), situacao: val("s-sit"),
               dependentes: parseInt($("s-dep").value, 10) || 0,
               jovem: $("s-jovem-sim").checked ? parseInt($("s-jovem-ano").value, 10) : 0 };
    }
    function ligacao(e) {
      var p = new URLSearchParams({ modo: "c", b: String(e.base), u: e.duodecimos ? "1" : "0", v: String(e.refeicao), n: String(e.dias),
                                    f: e.forma, e: e.situacao, k: String(e.dependentes) });
      if (e.jovem) p.set("j", String(e.jovem));
      return location.origin + location.pathname + "?" + p.toString();
    }

    function atualizar() {
      var e = dados();
      f.classList.toggle("com-jovem-s", e.jovem > 0);
      var r = SALARIO.calcular(e);
      $("s-liq").textContent = euros(r.liquido);
      $("s-cartao").textContent = r.cartao > 0 ? "e " + euros(r.cartao) + " € no cartão de refeição" : "";
      $("s-r-base").textContent = euros(e.base) + " €";
      $("s-l-duod").hidden = !e.duodecimos;
      $("s-r-duod").textContent = "+" + euros(r.duod) + " €";
      $("s-r-ss").textContent = "-" + euros(r.ss) + " €";
      $("s-r-irs").textContent = "-" + euros(r.irsMes + r.irsDuod) + " €";
      $("s-r-taxa").textContent = "taxa efetiva de " + pct(r.taxaMes) + " sobre " + euros(r.R) + " €";
      $("s-r-ref").textContent = r.refTotal > 0 ? euros(r.refTotal) + " €" + (r.refTributado > 0 ? " (" + euros(r.refTributado) + " € com impostos)" : " (sem impostos)") : "0,00 €";

      var notas = [];
      if (!e.duodecimos && e.base > 0) notas.push("Nos meses dos subsídios de férias e de Natal recebes também cerca de " + euros(r.liquidoSubsidio) + " € líquidos de cada um.");
      if (r.refTributado > 0) {
        var outra = SALARIO.calcular(Object.assign({}, e, { forma: e.forma === "dinheiro" ? "cartao" : "dinheiro" }));
        if (e.forma === "dinheiro") {
          var ganho = (outra.liquido + outra.cartao) - r.liquido;
          notas.push("Acima de " + euros(r.lim) + " € por dia, o subsídio em dinheiro paga IRS e Segurança Social. Se a empresa o pagasse em cartão, ficavas com mais " + euros(ganho) + " € por mês (no cartão).");
        } else {
          notas.push("O subsídio passa os " + euros(r.lim) + " € por dia isentos em cartão: a parte acima paga IRS e Segurança Social no salário.");
        }
      }
      if (e.jovem > 0) notas.push("Com o IRS Jovem, a empresa calcula a taxa sobre o salário todo e aplica-a só à parte que não está isenta.");
      if (e.dependentes >= 3) notas.push("Com três ou mais dependentes, a taxa desce um ponto percentual.");
      notas.push("A retenção é um adiantamento: na declaração de IRS pode haver reembolso ou imposto a pagar.");
      $("s-notas").textContent = notas.join(" ");
      $("s-copiar").dataset.url = ligacao(e);
      if (!$("modo-c").hidden) { try { history.replaceState(null, "", ligacao(e)); } catch (x) {} }
    }
    $("s-copiar").addEventListener("click", function () {
      var b = this, url = b.dataset.url, antes = "Copiar a ligação com estes valores";
      function feito(t) { b.textContent = t; setTimeout(function () { b.textContent = antes; }, 2500); }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { feito("Ligação copiada"); }, function () { window.prompt("Copia esta ligação:", url); });
      else window.prompt("Copia esta ligação:", url);
    });
    document.addEventListener("modo-mudou", atualizar);
    f.addEventListener("input", atualizar);
    f.addEventListener("change", atualizar);
    f.addEventListener("submit", function (ev) { ev.preventDefault(); });
    atualizar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
