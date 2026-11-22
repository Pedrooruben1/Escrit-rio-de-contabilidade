/* Salário líquido (trabalho por conta de outrem, residentes no Continente), 2026.
   Fontes (confirmadas em 22/11/2026):
   - Tabelas de retenção I, II e III: Continente, Despacho n.º 233-A/2026, de 6 de janeiro; Madeira, Despacho
     regional n.º 19/2026, divulgado pela Circular n.º 2/2026 da AT; Açores, Despacho n.º 1179/2026 (Portal das Finanças).
   - Subsídios de férias e de Natal com retenção autónoma; em duodécimos, retém-se em cada pagamento a parte
     proporcional do imposto do subsídio inteiro: artigo 99.º-C, n.os 5 e 6, do CIRS.
   - 3 ou mais dependentes: menos 1 ponto percentual na taxa marginal (n.º 5, alínea h, do despacho).
   - IRS Jovem na retenção: taxa da remuneração total aplicada à parte não isenta, com limite mensal de
     55 x IAS / 14 (despacho, n.º 5, alínea g, e folheto "IRS Jovem 2025" da AT).
   - Subsídio de refeição isento até 6,15 € por dia em dinheiro e 10,46 € em cartão (70 % acima); o excedente
     paga IRS e Segurança Social.
   - Segurança Social do trabalhador: 11 %.
   Não inclui: pessoas com deficiência, trabalho suplementar, outros abonos. */
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
  var MAD = {
    I: { dep: 21.43, linhas: [[980, 0, 0], [1028, 0.0872, [2.6, 1356.92]], [1099, 0.1204, [1.35, 1696.78]], [1201, 0.1204, 97.17],
      [1623, 0.1763, 164.31], [2332, 0.223, 240.11], [3203, 0.2242, 242.91], [3614, 0.2727, 398.26], [6585, 0.2778, 416.70],
      [6954, 0.2802, 432.51], [21411, 0.2924, 517.35], [Infinity, 0.3278, 1275.30]] },
    III: { dep: 42.86, linhas: [[997, 0, 0], [1099, 0.0872, [1.35, 1819.64]], [1141, 0.0872, 84.84], [1857, 0.1033, 103.22],
      [2485, 0.1091, 114.00], [3331, 0.1236, 150.04], [3895, 0.1404, 206.01], [6673, 0.1595, 280.41], [6878, 0.2213, 692.81],
      [21411, 0.2493, 885.40], [Infinity, 0.3278, 2566.17]] }
  };
  MAD.II = { dep: 34.29, linhas: MAD.I.linhas };
  var ACO = {
    I: { dep: 21.43, linhas: [[966, 0, 0], [1042, 0.0875, [2.6, 1337.54]], [1108, 0.1099, [1.35, 1652.49]], [1154, 0.1099, 80.79],
      [1212, 0.1484, 125.22], [1819, 0.1687, 149.83], [2119, 0.2177, 238.97], [2499, 0.2443, 295.34], [3305, 0.2685, 355.82],
      [5547, 0.2779, 386.89], [20221, 0.3146, 590.47], [Infinity, 0.3302, 905.92]] },
    III: { dep: 42.86, linhas: [[1226, 0, 0], [1267, 0.0728, 89.26], [1602, 0.0964, 119.17], [1962, 0.1099, 140.80],
      [2240, 0.1357, 191.42], [2900, 0.1594, 244.51], [3389, 0.1799, 303.96], [5965, 0.2017, 377.85], [20265, 0.2710, 791.23],
      [Infinity, 0.3302, 1990.92]] }
  };
  ACO.II = { dep: 34.29, linhas: ACO.I.linhas };
  var REGIOES = { cont: TAB, mad: MAD, aco: ACO };
  var LIM = { dinheiro: 6.15, cartao: 10.46 };

  function tabela(situacao, dependentes, regiao) {
    var T = REGIOES[regiao] || TAB;
    if (situacao === "u") return T.III;                   // casado, único titular
    if (situacao === "n" && dependentes > 0) return T.II; // não casado com dependentes
    return T.I;                                            // não casado sem dependentes ou casado, dois titulares
  }

  function retencao(R, situacao, dependentes, regiao) {
    if (R <= 0) return 0;
    var t = tabela(situacao, dependentes, regiao), l = null;
    for (var i = 0; i < t.linhas.length; i++) { if (R <= t.linhas[i][0]) { l = t.linhas[i]; break; } }
    var taxa = l[1];
    if (taxa === 0) return 0;
    if (dependentes >= 3) taxa -= 0.01;
    var parcela = Array.isArray(l[2]) ? l[1] * l[2][0] * (l[2][1] - R) : l[2];
    return Math.max(0, R * taxa - parcela - t.dep * dependentes);
  }

  // e: {regiao: cont|mad|aco, base, outros (abonos mensais com IRS), outrosSS: bool, duodecimos: bool, refeicao (€/dia), dias, forma: "cartao"|"dinheiro", situacao: n|d|u, dependentes, jovem: 0 ou 1-10}
  function calcular(e) {
    var lim = LIM[e.forma] || LIM.dinheiro;
    var refDia = e.refeicao || 0, dias = e.dias || 0;
    var refTotal = refDia * dias, refTributado = Math.max(0, refDia - lim) * dias, refIsento = refTotal - refTributado;
    var pctJ = !e.jovem ? 0 : e.jovem === 1 ? 1 : e.jovem <= 4 ? 0.75 : e.jovem <= 7 ? 0.5 : 0.25;
    var limJ = 55 * IAS / 14;
    function retido(R) {
      var r = retencao(R, e.situacao, e.dependentes, e.regiao);
      if (!pctJ || R <= 0) return r;
      var isento = Math.min(R * pctJ, limJ);
      return r * (1 - isento / R);
    }
    // mês normal
    var outros = e.outros || 0;
    var R = e.base + outros + refTributado;
    var irsMes = retido(R);
    var subsidio = e.base;                                 // cada subsídio igual ao salário base
    var irsSubsidio = retido(subsidio);
    var duod = e.duodecimos ? 2 * subsidio / 12 : 0;
    var irsDuod = e.duodecimos ? 2 * irsSubsidio / 12 : 0;
    var ss = 0.11 * (e.base + refTributado + duod + (e.outrosSS ? outros : 0));
    var liquido = e.base + outros + duod + (e.forma === "dinheiro" ? refTotal : 0) - irsMes - irsDuod - ss;
    // em cartão, o subsídio vai para o cartão (incluindo a parte acima do limite, que paga IRS e SS no salário)
    var cartao = e.forma === "cartao" ? refTotal : 0;
    var liquidoSubsidio = e.duodecimos ? 0 : subsidio - irsSubsidio - 0.11 * subsidio;
    var brutoAno = e.base * 14 + outros * 12 + refTotal * 11;
    return { R: R, irsMes: irsMes, taxaMes: R > 0 ? irsMes / R : 0, irsDuod: irsDuod, duod: duod, ss: ss, liquido: liquido,
             cartao: cartao, refTotal: refTotal, refTributado: refTributado, refIsento: refIsento, lim: lim,
             irsSubsidio: irsSubsidio, liquidoSubsidio: liquidoSubsidio, brutoAno: brutoAno };
  }
  return { calcular: calcular, retencao: retencao, LIM: LIM };
})();
if (typeof module !== "undefined") module.exports = SALARIO;
