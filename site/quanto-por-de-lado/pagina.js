(function () {
  function euros(v) { return Math.round(v).toLocaleString("pt-PT"); }
  function iniciar() {
    var f = document.getElementById("calc"), res = document.getElementById("resultado");
    if (!f || typeof CALC === "undefined") return;
    function val(nome) { var r = f.querySelector('input[name="' + nome + '"]:checked'); return r ? r.value : null; }
    function num(id) { var v = parseFloat(String(document.getElementById(id).value).replace(",", ".")); return isFinite(v) && v > 0 ? v : 0; }
    function atualizar() {
      var e = { mensal: num("mensal"), tipo: val("tipo"), ano: parseInt(val("ano"), 10), despesas: num("despesas"), retencao: parseFloat(val("retencao")) };
      var servicos = e.tipo !== "v";
      f.classList.toggle("vendas", !servicos);
      if (!servicos) e.retencao = 0;
      document.getElementById("taxa-ret").textContent = servicos ? "Nesta atividade, a retenção é de " + (e.tipo === "s" ? "11,5 %" : "23 %") + ". Quem fatura menos de 15.000 € por ano pode pedir dispensa." : "";
      var r = CALC.calcular(e);
      document.getElementById("r-mes").textContent = euros(r.porMes);
      document.getElementById("r-pct").textContent = e.mensal > 0 ? "Cerca de " + Math.round(r.pct * 100) + " % do que faturas." : "";
      document.getElementById("r-ss").textContent = e.ano === 1 ? "0 € (isento no primeiro ano)" : euros(r.ssMes) + " € por mês";
      document.getElementById("r-irs").textContent = euros(r.irs) + " €";
      document.getElementById("l-ret").hidden = !(r.retido > 0);
      document.getElementById("r-ret").textContent = euros(r.retido) + " €";
      var t = document.getElementById("r-acerto-t"), a = document.getElementById("r-acerto");
      if (r.acerto >= 0) { t.textContent = "A pagar na declaração de IRS"; a.textContent = euros(r.acerto) + " €"; }
      else { t.textContent = "Reembolso estimado"; a.textContent = euros(-r.acerto) + " €"; }
      var notas = [];
      if (r.retido > 0 && r.acerto < 0) notas.push("As retenções dos clientes já cobrem o IRS estimado, por isso o valor por mês é só a Segurança Social.");
      if (r.faltaDespesas > 0) notas.push("Faltam " + euros(r.faltaDespesas) + " € de despesas com fatura para justificar os 15 %: esse valor foi somado ao rendimento. Se tiveres despesas da atividade, põe-nas acima.");
      if (e.ano === 2) notas.push("No segundo ano, a Segurança Social começa a meio do ano: contámos o ano inteiro, por isso o valor está um pouco acima.");
      if (e.ano !== 3 && servicos) notas.push("A redução do IRS nos dois primeiros anos só se aplica se não tiveres salário nem pensão.");
      document.getElementById("r-notas").textContent = notas.join(" ");
      res.hidden = false;
    }
    f.addEventListener("input", atualizar);
    f.addEventListener("change", atualizar);
    f.addEventListener("submit", function (ev) { ev.preventDefault(); });
    atualizar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
