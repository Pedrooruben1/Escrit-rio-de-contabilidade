import json, os, sys, html, base64
from playwright.sync_api import sync_playwright
d = json.load(open(sys.argv[1])); F = os.path.abspath(sys.argv[2]); out = sys.argv[3]
u = lambda w: "data:font/woff2;base64,"+base64.b64encode(open(f"{F}/manrope-latin-{w}-normal.woff2","rb").read()).decode()
azul = d["fundo"] == "azul"
bg, fg = ("#17324D", "#F7F5F0") if azul else ("#FFFFFF", "#17324D")
grao = 0.05 if azul else 0.02
cor = "0 0 0 0 .97  0 0 0 0 .96  0 0 0 0 .94" if azul else "0 0 0 0 .2  0 0 0 0 .2  0 0 0 0 .25"
css = f"""@font-face{{font-family:M;src:url({u('500')});font-weight:500}}
@font-face{{font-family:M;src:url({u('700')});font-weight:700}}
@font-face{{font-family:M;src:url({u('800')});font-weight:800}}
html,body{{margin:0}}
body{{width:1080px;height:1350px;background:{bg};color:{fg};font-family:M;position:relative;overflow:hidden}}
.grao{{position:absolute;inset:0;opacity:{grao};pointer-events:none}}
.c{{position:absolute;inset:0;padding:120px 100px 100px;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box}}
.k{{color:#E09F3E;font-weight:700;font-size:32px;letter-spacing:1.5px;text-transform:uppercase;transform:rotate(-1.2deg);transform-origin:left}}
h1{{font-weight:800;font-size:__TAM__px;line-height:1.14;margin:48px 0 0;letter-spacing:-1px}}
em{{font-style:normal;color:#E09F3E;position:relative}}
.f{{font-weight:500;font-size:28px;display:flex;justify-content:space-between;align-items:center;opacity:.85}}
svg.mao{{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}}"""
grao_svg = """<svg class=grao width=1080 height=1350><filter id=n><feTurbulence type=fractalNoise baseFrequency=.85 numOctaves=3 stitchTiles=stitch/><feColorMatrix values="COR  0 0 0 1 0"/></filter><rect width=100% height=100% filter=url(#n)/></svg>"""
js = """(fg) => {
 const r = Math.random; const svgNS='http://www.w3.org/2000/svg';
 const s = document.createElementNS(svgNS,'svg'); s.setAttribute('class','mao'); s.setAttribute('width','1080'); s.setAttribute('height','1350');
 s.innerHTML = '<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="'+Math.floor(r()*99)+'"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs>';
 const add = (dd, w, col, dash) => { const p=document.createElementNS(svgNS,'path'); p.setAttribute('d',dd); p.setAttribute('fill','none'); p.setAttribute('stroke',col); p.setAttribute('stroke-width',w); p.setAttribute('stroke-linecap','round'); p.setAttribute('stroke-linejoin','round'); p.setAttribute('filter','url(#rough)'); if(dash) p.setAttribute('stroke-dasharray',dash); s.appendChild(p); };
 document.querySelectorAll('em').forEach(e => { for (const b of e.getClientRects()) {
   const y=b.bottom-6, x0=b.left-8, x1=b.right+10, m=(x0+x1)/2;
   add(`M${x0} ${y+3} Q${m} ${y-6+r()*4} ${x1} ${y+1}`, 9, '#E09F3E');
   add(`M${x0+30} ${y+16} Q${m} ${y+10} ${x1-20} ${y+14}`, 5, '#E09F3E');
 }});
 const f=document.querySelector('.f').getBoundingClientRect(); const yy=f.top-34;
 add(`M100 ${yy} C 380 ${yy-6}, 700 ${yy+6}, 980 ${yy-2}`, 3, fg, '2 14');
 const h=document.querySelector('h1').getBoundingClientRect(); const ax=940, ay=h.bottom+150;
 if (ay < yy-120 && !document.querySelector('svg.des')) { add(`M${ax} ${ay} C ${ax+30} ${ay-90}, ${ax-10} ${ay-150}, ${ax-90} ${h.bottom+30}`, 4, '#E09F3E');
   add(`M${ax-90} ${h.bottom+30} l 6 34 M${ax-90} ${h.bottom+30} l 32 12`, 4, '#E09F3E'); }
 document.body.appendChild(s);
}"""

n = len(d["slides"])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    for i, s in enumerate(d["slides"], 1):
        t = html.escape(s["texto"]).replace("[", "<em>").replace("]", "</em>")
        fs = 92 if len(s["texto"]) < 70 else 74
        num = ""
        k = s.get("svg")
        des = f'<svg class=des width=1080 height=360 style="position:absolute;left:0;top:760px;overflow:visible"><g fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" filter="url(#rough2)">{k.replace("FG", fg).replace("BG", bg)}</g><defs><filter id="rough2"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter></defs></svg>' if k else ""
        pg.set_content(f"<html><head><meta charset=utf-8><style>{css.replace('__TAM__', str(fs))}</style></head><body>{grao_svg.replace('COR', cor)}{des}<div class=c><div><div class=k>{html.escape(d['etiqueta'])}</div><h1>{t}</h1></div><div class=f><span>bem.contado</span><span>{num}</span><span>@bem.contadopt</span></div></div></body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.evaluate(js, fg)
        pg.screenshot(path=os.path.join(out, f"slide_{i}.png"))
    b.close()

