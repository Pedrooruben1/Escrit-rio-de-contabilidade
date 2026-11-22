/* Salário líquido (trabalho por conta de outrem, residentes no Continente), 2026.
   Fontes (confirmadas em 22/11/2026):
   - Tabelas de retenção I, II e III: Despacho n.º 233-A/2026, de 6 de janeiro (Portal das Finanças).
   - Subsídios de férias e de Natal com retenção autónoma; em duodécimos, retém-se em cada pagamento a parte
     proporcional do imposto do subsídio inteiro: artigo 99.º-C, n.os 5 e 6, do CIRS.
   - 3 ou mais dependentes: menos 1 ponto percentual na taxa marginal (n.º 5, alínea h, do despacho).
   - IRS Jovem na retenção: taxa da remuneração total aplicada à parte não isenta, com limite mensal de
     55 x IAS / 14 (despacho, n.º 5, alínea g, e folheto "IRS Jovem 2025" da AT).
   - Subsídio de refeição isento até 6,15 € por dia em dinheiro e 10,46 € em cartão (70 % acima); o excedente
     paga IRS e Segurança Social.
   - Segurança Social do trabalhador: 11 %.
   Não inclui: tabelas da Madeira e dos Açores, pessoas com deficiência, trabalho suplementar, outros abonos. */
var SALARIO = (function () {
  var IAS = 537.13;
  // [limite superior, taxa, parcela a abater (número) ou [k, C] para a fórmula taxa × k × (C − R)]
  var TAB = {
    I: { dep: 21.43, linhas: [[920, 0, 0], [1042, 0.125, [2.6, 1273.85]], [1108, 0.157, [1.35, 1554.83]], [1154, 0.157, 94.71],
      [1212, 0.212, 158.18], [1819, 0.241, 193.33], [2119, 0.311, 320.66], [2499, 0.349, 401.19], [3305, 0.3836, 487.66],
      [5547, 0.3969, 531.62], [20221, 0.4495, 823.40], [Infinity, 0.4717, 1272.31]] },
    III: { dep: 42.86, linhas: [[991, 0, 0], [1042, 0.125, [2.6, 1372.15]], [1108, 0.125, [1.35, 1677.85]], [1119, 0.125, 96.17],
      [1432, 0.1272, 98.64], [1962, 0.157, 141.32], [2240, 0.1938, 213.53], [2773, 0.2277, 289.47], [3389, 0.257, 370.72],
      [5965, 0.2881, 476.12], [20265, 0.3843, 1049.96], [Infinity, 0.4717, 2821.13]] }
  };
  TAB.II = { dep: 34.29, linhas: TAB.I.linhas };
  var LIM = { dinheiro: 6.15, cartao: 10.46 };

  function tabela(situacao, dependentes) {
    if (situacao === "u") return TAB.III;                 // casado, único titular
    if (situacao === "n" && dependentes > 0) return TAB.II; // não casado com dependentes
    return TAB.I;                                          // não casado sem dependentes ou casado, dois titulares
  }

  function retencao(R, situacao, dependentes) {
    if (R <= 0) return 0;
    var t = tabela(situacao, dependentes), l = null;
    for (var i = 0; i < t.linhas.length; i++) { if (R <= t.linhas[i][0]) { l = t.linhas[i]; break; } }
    var taxa = l[1];
    if (taxa === 0) return 0;
    if (dependentes >= 3) taxa -= 0.01;
    var parcela = Array.isArray(l[2]) ? l[1] * l[2][0] * (l[2][1] - R) : l[2];
    return Math.max(0, R * taxa - parcela - t.dep * dependentes);
  }

  // e: {base, duodecimos: bool, refeicao (€/dia), dias, forma: "cartao"|"dinheiro", situacao: n|d|u, dependentes, jovem: 0 ou 1-10}
  function calcular(e) {
    var lim = LIM[e.forma] || LIM.dinheiro;
    var refDia = e.refeicao || 0, dias = e.dias || 0;
    var refTotal = refDia * dias, refTributado = Math.max(0, refDia - lim) * dias, refIsento = refTotal - refTributado;
    var pctJ = !e.jovem ? 0 : e.jovem === 1 ? 1 : e.jovem <= 4 ? 0.75 : e.jovem <= 7 ? 0.5 : 0.25;
    var limJ = 55 * IAS / 14;
    function retido(R) {
      var r = retencao(R, e.situacao, e.dependentes);
      if (!pctJ || R <= 0) return r;
      var isento = Math.min(R * pctJ, limJ);
      return r * (1 - isento / R);
    }
    // mês normal
    var R = e.base + refTributado;
    var irsMes = retido(R);
    var subsidio = e.base;                                 // cada subsídio igual ao salário base
    var irsSubsidio = retido(subsidio);
    var duod = e.duodecimos ? 2 * subsidio / 12 : 0;
    var irsDuod = e.duodecimos ? 2 * irsSubsidio / 12 : 0;
    var ss = 0.11 * (e.base + refTributado + duod);
    var liquido = e.base + duod + (e.forma === "dinheiro" ? refTotal : 0) - irsMes - irsDuod - ss;
    // em cartão, o subsídio vai para o cartão (incluindo a parte acima do limite, que paga IRS e SS no salário)
    var cartao = e.forma === "cartao" ? refTotal : 0;
    var liquidoSubsidio = e.duodecimos ? 0 : subsidio - irsSubsidio - 0.11 * subsidio;
    var brutoAno = e.base * 14 + refTotal * 11;
    return { R: R, irsMes: irsMes, taxaMes: R > 0 ? irsMes / R : 0, irsDuod: irsDuod, duod: duod, ss: ss, liquido: liquido,
             cartao: cartao, refTotal: refTotal, refTributado: refTributado, refIsento: refIsento, lim: lim,
             irsSubsidio: irsSubsidio, liquidoSubsidio: liquidoSubsidio, brutoAno: brutoAno };
  }
  return { calcular: calcular, retencao: retencao, LIM: LIM };
})();
if (typeof module !== "undefined") module.exports = SALARIO;
