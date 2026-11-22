/* Quanto pôr de lado por mês para o IRS e a Segurança Social (recibos verdes, regime simplificado).
   Valores de 2026. Fontes (confirmadas em 22/11/2026):
   - IRS, taxas: artigo 68.º do CIRS, redação do DL 212/2026 (Portal das Finanças).
   - Regime simplificado: artigo 31.º do CIRS (coeficientes, n.º 2, n.º 10, n.º 13).
   - Dedução específica: artigo 25.º, n.º 1, a) do CIRS (8,54 x IAS).
   - Mínimo de existência: artigo 70.º do CIRS.
   - Retenção na fonte: artigo 101.º, n.º 1 do CIRS (23 % e 11,5 %).
   - IAS 2026: 537,13 € (Portaria 480-A/2025/1).
   - Segurança Social: Guia Prático "Novo regime dos trabalhadores independentes" v1.14 (21,4 %, 70 % / 20 %,
     mínimo de 20 €, máximo de 12 x IAS, primeiro enquadramento só ao fim de 12 meses). */
var CALC = (function () {
  var IAS = 537.13;
  var ESCALOES = [[8342, 0.122], [12587, 0.152], [17838, 0.207], [23089, 0.236], [29397, 0.306],
                  [43090, 0.346], [46566, 0.431], [86634, 0.446], [Infinity, 0.48]];
  // p: tabela do art. 151.º; o: código 1519 da tabela (sem mínimo de existência); s: outros serviços; v: vendas
  var COEF = { p: 0.75, o: 0.75, s: 0.35, v: 0.15 };
  var RET = { p: 0.23, o: 0.23, s: 0.115, v: 0 };
  var DESP_GERAIS = 250;                          // dedução à coleta por despesas gerais familiares (assumida)

  function irsTaxas(c) {
    var imposto = 0, ant = 0;
    for (var i = 0; i < ESCALOES.length; i++) {
      var lim = ESCALOES[i][0], t = ESCALOES[i][1];
      if (c > ant) imposto += (Math.min(c, lim) - ant) * t;
      ant = lim;
    }
    return imposto;
  }

  function minimoExistencia(bruto, rl) {
    // artigo 70.º: abatimento ao rendimento coletável; dedução específica = bruto - rendimento líquido
    var VR = Math.max(12880, 1.5 * 14 * IAS), T1 = ESCALOES[0][1], L1 = ESCALOES[0][0];
    if (bruto > 2.2 * 14 * IAS) return 0;
    var L = VR - DESP_GERAIS / (T1 * 3.6) + L1 / 3.6;
    var ded = bruto - rl, base;
    if (bruto <= VR) base = VR - (ded + DESP_GERAIS / T1);
    else if (bruto <= L) base = VR - 2.6 * (bruto - VR) - (ded + DESP_GERAIS / T1);
    else base = L - L1 - 1.35 * (bruto - L) - ded;
    return Math.max(0, Math.min(base, rl));
  }

  // e: {mensal, tipo: p|o|s|v, ano: 1|2|3 (3 = terceiro ou seguintes), despesas (mensais), retencao: 0|0.5|1}
  function calcular(e) {
    var bruto = e.mensal * 12;
    var servicos = e.tipo !== "v";
    // Segurança Social (por mês, sobre a média; isenção nos primeiros 12 meses)
    var baseSS = Math.min((servicos ? 0.7 : 0.2) * e.mensal, 12 * IAS);
    var ssMes = e.ano === 1 ? 0 : (e.mensal > 0 ? Math.max(20, 0.214 * baseSS) : 20);
    var ssAno = ssMes * 12;
    // IRS
    var coef = COEF[e.tipo];
    if (servicos && e.ano === 1) coef *= 0.5;
    if (servicos && e.ano === 2) coef *= 0.75;
    var rl = bruto * coef;
    var faltaDespesas = 0;
    if (servicos) {
      var dedSS = Math.max(0, ssAno - 0.1 * bruto);               // n.º 2
      rl = Math.max(0, rl - dedSS);
      var a = Math.max(8.54 * IAS, ssAno - dedSS);                 // n.º 13, a)
      faltaDespesas = Math.max(0, 0.15 * bruto - (a + e.despesas * 12));
      rl += faltaDespesas;
    }
    var abat = e.tipo === "p" ? minimoExistencia(bruto, rl) : 0;
    var coletavel = Math.max(0, rl - abat);
    var irs = Math.max(0, irsTaxas(coletavel) - DESP_GERAIS);
    var retido = bruto * RET[e.tipo] * e.retencao;
    var acerto = irs - retido;                                     // > 0: a pagar em agosto; < 0: reembolso
    var porMes = ssMes + Math.max(0, acerto) / 12;
    return { bruto: bruto, ssMes: ssMes, ssAno: ssAno, irs: irs, retido: retido, acerto: acerto, porMes: porMes,
             coletavel: coletavel, faltaDespesas: faltaDespesas, abatimento: abat,
             pct: e.mensal > 0 ? porMes / e.mensal : 0 };
  }
  return { calcular: calcular, irsTaxas: irsTaxas };
})();
if (typeof module !== "undefined") module.exports = CALC;
