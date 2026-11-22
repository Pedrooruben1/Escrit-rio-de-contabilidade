/* Barra fixa com o resultado, no telemóvel: aparece enquanto se preenche o formulário e o resultado não está à vista. */
(function () {
  function iniciar() {
    var $ = function (id) { return document.getElementById(id); };
    if (!$("modo-c") || !$("modo-r")) return;
    var barra = document.createElement("button");
    barra.type = "button"; barra.className = "barra-resultado"; barra.setAttribute("aria-label", "Ver o resultado completo");
    barra.innerHTML = '<span><span class="br-rotulo"></span><br><span class="br-valor"></span></span><span class="br-ver">Ver o resultado</span>';
    document.body.appendChild(barra);
    var vis = { secao: false, resultado: false };
    function modo() { return document.documentElement.getAttribute("data-modo"); }
    function alvos() { return modo() === "c" ? { secao: $("modo-c"), resultado: $("resultado-sal") } : { secao: $("modo-r"), resultado: $("resultado") }; }
    function atualizar() {
      var m = modo();
      if (m === "c") { barra.querySelector(".br-rotulo").textContent = "Recebes na conta, por mês"; barra.querySelector(".br-valor").textContent = $("s-liq").textContent + " €"; }
      else if (m === "r") { barra.querySelector(".br-rotulo").textContent = "Põe de lado, por mês"; barra.querySelector(".br-valor").textContent = $("r-mes").textContent + " €"; }
      var ativa = (m === "c" || m === "r") && vis.secao && !vis.resultado;
      barra.classList.toggle("ativa", ativa);
      barra.hidden = !ativa;
    }
    var obs = new IntersectionObserver(function (entradas) {
      var a = alvos();
      entradas.forEach(function (en) { if (en.target === a.secao) vis.secao = en.isIntersecting; if (en.target === a.resultado) vis.resultado = en.isIntersecting; });
      atualizar();
    }, { threshold: [0, 0.25] });
    function observar() { obs.disconnect(); vis = { secao: false, resultado: false }; var a = alvos(); if (a.secao && a.resultado) { obs.observe(a.secao); obs.observe(a.resultado); } }
    document.addEventListener("modo-mudou", function () { requestAnimationFrame(function () { observar(); atualizar(); }); });
    document.addEventListener("input", function () { requestAnimationFrame(atualizar); });
    document.addEventListener("change", function () { requestAnimationFrame(atualizar); });
    barra.addEventListener("click", function () { var r = alvos().resultado; if (r) r.scrollIntoView({ behavior: "smooth", block: "start" }); });
    observar(); atualizar();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
