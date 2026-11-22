(function () {
  var MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
  // 1580.85 -> "1.580,85" (o toLocaleString de pt-PT não separa os milhares abaixo de 10.000)
  function euros(v) {
    var neg = v < 0, c = Math.round(Math.abs(v) * 100), int = String(Math.floor(c / 100)), dec = ("0" + (c % 100)).slice(-2);
    return (neg ? "-" : "") + int.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + dec;
  }
  // Aceita "1.500,00", "1500,5", "1.500", "1500" e "1500.50"
  function lerEuros(t) {
    var s = String(t).trim().replace(/[\s€]/g, "");
    if (s.indexOf(",") > -1) s = s.replace(/\./g, "").replace(",", ".");
    else if (/^\d{1,3}(\.\d{3})+$/.test(s)) s = s.replace(/\./g, "");
    var v = parseFloat(s);
    return isFinite(v) && v > 0 ? v : 0;
  }

  function iniciar() {
    var f = document.getElementById("calc"), res = document.getElementById("resultado");
    if (!f || typeof CALC === "undefined") return;
    var $ = function (id) { return document.getElementById(id); };
    function val(nome) { var r = f.querySelector('input[name="' + nome + '"]:checked'); return r ? r.value : null; }
    function marcar(nome, v) { var r = f.querySelector('input[name="' + nome + '"][value="' + v + '"]'); if (r) r.checked = true; }

    // valores na ligação: ?m=1500&t=p&a=3&i=9&r=0&d=0&s=0&j=0
    var q = new URLSearchParams(location.search);
    if (q.has("m")) $("mensal").value = euros(lerEuros(q.get("m")));
    if (q.has("d")) $("despesas").value = euros(lerEuros(q.get("d")));
    if (q.has("t")) marcar("tipo", q.get("t"));
    if (q.has("a")) marcar("ano", q.get("a"));
    if (q.has("r")) marcar("retencao", q.get("r"));
    if (q.has("i")) $("mes").value = q.get("i");
    if (q.has("s")) $("ajuste").value = q.get("s");
    if (q.has("j") && q.get("j") !== "0") { f["jovem-sim"].checked = true; $("jovem-ano").value = q.get("j"); }
    // garante que os campos de texto começam formatados e legíveis
    ["mensal", "despesas"].forEach(function (id) {
      var c = $(id);
      c.value = euros(lerEuros(c.value));
      c.addEventListener("blur", function () { c.value = euros(lerEuros(c.value)); });
      c.addEventListener("focus", function () { c.select(); });
    });

    function dados() {
      return { mensal: lerEuros($("mensal").value), tipo: val("tipo"), ano: parseInt(val("ano"), 10),
               mes: parseInt($("mes").value, 10), ajuste: parseFloat($("ajuste").value) || 0,
               despesas: lerEuros($("despesas").value), retencao: parseFloat(val("retencao")),
               jovem: f["jovem-sim"].checked ? parseInt($("jovem-ano").value, 10) : 0 };
    }

    function ligacao(e) {
      var p = new URLSearchParams({ modo: "r", m: String(e.mensal), t: e.tipo, a: String(e.ano), r: String(e.retencao) });
      if (e.ano !== 3) p.set("i", String(e.mes));
      if (e.despesas) p.set("d", String(e.despesas));
      if (e.ajuste) p.set("s", String(e.ajuste));
      if (e.jovem) p.set("j", String(e.jovem));
      return location.origin + location.pathname + "?" + p.toString();
    }

    function atualizar() {
      var e = dados();
      var servicos = e.tipo !== "v";
      f.classList.toggle("vendas", !servicos);
      f.classList.toggle("com-jovem", e.jovem > 0);
      f.classList.toggle("com-inicio", e.ano !== 3);
      if (!servicos) e.retencao = 0;
      $("taxa-ret").textContent = servicos ? "Nesta atividade, a retenção é de " + (e.tipo === "s" ? "11,5 %" : "23 %") + ". Quem fatura menos de 15.000 € por ano pode pedir dispensa." : "";

      var r = CALC.calcular(e);
      $("r-mes").textContent = euros(r.porMes);
      $("r-pct").textContent = e.mensal > 0 ? "Cerca de " + Math.round(r.pct * 100) + " % do que faturas." : "";
      var irsMes = Math.max(0, r.acerto) / 12;
      $("r-soma").textContent = "Segurança Social " + euros(r.ssMes) + " € + IRS " + euros(irsMes) + " € = " + euros(r.porMes) + " €";

      var mesNome = MESES[(e.mes || 1) - 1];
      if (e.ano === 1) $("r-ss").textContent = "0,00 € este ano";
      else if (e.ano === 2) $("r-ss").textContent = euros(r.ssMesCheio) + " € por mês, desde " + mesNome;
      else $("r-ss").textContent = euros(r.ssMes) + " € por mês";
      $("r-irs").textContent = euros(r.irs) + " €";
      $("l-ret").hidden = !(r.retido > 0);
      $("r-ret").textContent = euros(r.retido) + " €";
      if (r.acerto >= 0) { $("r-acerto-t").textContent = r.ppc > 0 ? "IRS a pagar (por conta e na declaração)" : "A pagar na declaração de IRS"; $("r-acerto").textContent = euros(r.acerto) + " €"; }
      else { $("r-acerto-t").textContent = "Reembolso estimado"; $("r-acerto").textContent = euros(-r.acerto) + " €"; }

      var notas = [];
      if (e.ano === 1) notas.push("Atenção: a Segurança Social começa em " + mesNome + " do próximo ano, com cerca de " + euros(r.ssMesCheio) + " € por mês. A partir daí, guarda " + euros(r.ssMesCheio + irsMes) + " € por mês.");
      if (e.ano === 2) notas.push("Contámos " + r.ssMeses + " " + (r.ssMeses === 1 ? "mês" : "meses") + " de Segurança Social este ano, de " + mesNome + " a dezembro.");
      if (r.ppc > 0) notas.push("Sem retenção, parte do IRS paga-se antes da declaração: se o teu IRS de há dois anos foi parecido, são três pagamentos por conta de cerca de " + euros(r.ppc) + " € até 20 de julho, 20 de setembro e 20 de dezembro, e o resto na declaração.");
      if (r.retido > 0 && r.acerto < 0) notas.push("As retenções dos clientes já cobrem o IRS estimado, por isso o valor por mês é só a Segurança Social.");
      if (r.faltaDespesas > 0) notas.push("Faltam " + euros(r.faltaDespesas) + " € de despesas com fatura para justificar os 15 %: esse valor foi somado ao rendimento. Se tiveres despesas da atividade, põe-nas acima.");
      if (e.jovem > 0) notas.push("Com o IRS Jovem, " + euros(r.isento) + " € do que faturas ficam isentos. Se os clientes retêm IRS, retêm sobre o valor todo, a não ser que lhes digas que estás no IRS Jovem.");
      if (e.ano !== 3 && servicos) notas.push("A redução do IRS nos dois primeiros anos só se aplica se não tiveres salário nem pensão.");
      if (r.bruto > 15000) notas.push("Ao faturar mais de 15.000 € por ano deixas de poder ficar isento de IVA pelo artigo 53.º (a partir do ano seguinte, ou logo se passares dos 18.750 €). O IVA que cobrares não entra nestas contas: guarda-o à parte.");
      $("r-notas").textContent = notas.join(" ");

      // comparação com e sem retenção
      var comp = "";
      if (servicos && e.mensal > 0) {
        var sem = CALC.calcular(Object.assign({}, e, { retencao: 0 })), com = CALC.calcular(Object.assign({}, e, { retencao: 1 }));
        var taxa = e.tipo === "s" ? "11,5 %" : "23 %";
        comp = "Sem retenção, guardas " + euros(sem.porMes) + " € por mês e pagas " + euros(Math.max(0, sem.acerto)) + " € de IRS" + (sem.ppc > 0 ? ", em pagamentos por conta e na declaração. " : " na declaração. ") +
          "Com retenção de " + taxa + " em todos os recibos, os clientes entregam " + euros(com.retido / 12) + " € por mês por ti e, no fim, " +
          (com.acerto < 0 ? "recebes cerca de " + euros(-com.acerto) + " € de reembolso." : "ainda pagas cerca de " + euros(com.acerto) + " €.");
      }
      $("r-compara").textContent = comp;
      $("copiar-ligacao").dataset.url = ligacao(e);
      if (!$("modo-r").hidden) { try { history.replaceState(null, "", ligacao(e)); } catch (x) {} }
      res.hidden = false;
    }

    $("copiar-ligacao").addEventListener("click", function () {
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
