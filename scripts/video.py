import os, sys, json, html, base64, subprocess, re
from playwright.sync_api import sync_playwright
d = json.load(open(sys.argv[1])); F = os.path.abspath(sys.argv[2]); out = sys.argv[3]
u = lambda w: "data:font/woff2;base64,"+base64.b64encode(open(f"{F}/manrope-latin-{w}-normal.woff2","rb").read()).decode()
azul = d["fundo"] == "azul"
bg, fg = ("#17324D", "#F7F5F0") if azul else ("#FFFFFF", "#17324D")
am = "#E09F3E"; W, H, FPS = 1080, 1920, 30
css = f"""@font-face{{font-family:M;src:url({u('500')});font-weight:500}}
@font-face{{font-family:M;src:url({u('700')});font-weight:700}}
@font-face{{font-family:M;src:url({u('800')});font-weight:800}}
html,body{{margin:0}}
body{{width:{W}px;height:{H}px;background:{bg};color:{fg};font-family:M;overflow:hidden}}
#cam{{position:absolute;inset:-20px;transform-origin:50% 50%}}
.grao{{position:absolute;inset:0;opacity:.025}}
.c{{position:absolute;inset:20px;padding:220px 100px 150px;display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box}}
.k{{color:{am};font-weight:700;font-size:34px;letter-spacing:1.5px;text-transform:uppercase;transform:rotate(-1.2deg);transform-origin:left}}
h1{{font-weight:800;font-size:88px;line-height:1.14;margin:56px 0 0;letter-spacing:-1px}}
h1 .w{{display:inline-block;opacity:0}}
em{{font-style:normal;color:{am}}}
.f{{font-weight:500;font-size:30px;display:flex;justify-content:space-between;opacity:.85}}
svg.top{{position:absolute;left:20px;top:20px;overflow:visible}}"""
grao = """<svg class=grao width=1120 height=1960><filter id=n><feTurbulence type=fractalNoise baseFrequency=.85 numOctaves=3 seed=3/><feColorMatrix values="COR  0 0 0 1 0"/></filter><rect width=100% height=100% filter=url(#n)/></svg>"""
def words(t):
    out=[]; inem=False
    for tok in re.split(r'(\[|\])', t):
        if tok=='[': inem=True; continue
        if tok==']': inem=False; continue
        for w in tok.split(' '):
            if w: out.append(f'<em class=e><span class=w>{html.escape(w)}</span></em>' if inem else f'<span class=w>{html.escape(w)}</span>')
    return ' '.join(out)
setup_js = """() => {
 const NS='http://www.w3.org/2000/svg'; const top=document.getElementById('top'); const off=top.getBoundingClientRect();
 const add=(d,w,col,cls,dash)=>{const p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('fill','none');p.setAttribute('stroke',col);p.setAttribute('stroke-width',w);p.setAttribute('stroke-linecap','round');p.setAttribute('filter','url(#rough)');p.setAttribute('class',cls);if(dash)p.setAttribute('stroke-dasharray',dash);else p.setAttribute('pathLength','1');top.appendChild(p);};
 const rects=[]; document.querySelectorAll('em.e').forEach(e=>{for(const b of e.getClientRects())rects.push(b)});
 const lines={}; rects.forEach(b=>{const k=Math.round(b.bottom);(lines[k]=lines[k]||[]).push(b)});
 Object.values(lines).forEach(bs=>{const x0=Math.min(...bs.map(b=>b.left))-8-off.left,x1=Math.max(...bs.map(b=>b.right))+10-off.left,y=bs[0].bottom-6-off.top,m=(x0+x1)/2;
   add(`M${x0} ${y+3} Q${m} ${y-4} ${x1} ${y+1}`,9,'AMC','ul'); add(`M${x0+30} ${y+16} Q${m} ${y+10} ${x1-20} ${y+14}`,5,'AMC','ul');});
 const f=document.querySelector('.f').getBoundingClientRect(); const yy=f.top-40-off.top;
 add(`M100 ${yy} C 380 ${yy-6}, 700 ${yy+6}, 980 ${yy-2}`,3,'FGC','dot','2 14');
 document.querySelectorAll('.ul,.dr').forEach(p=>{p.style.strokeDasharray='1';p.style.strokeDashoffset='1';});
}"""
anim_js = """(t) => {
 const ease=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
 const easeIO=x=>x<0?0:x>1?1:(x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2);
 const cam=document.getElementById('cam');
 const x=3.2*Math.sin(t*2.1)+1.4*Math.sin(t*5.3+1), y=2.4*Math.sin(t*1.7+2)+1.1*Math.sin(t*4.1), r=0.12*Math.sin(t*1.3);
 cam.style.transform=`translate(${x}px,${y}px) rotate(${r}deg) scale(${1+0.012*Math.min(t/4,1)})`;
 const ws=[...document.querySelectorAll('h1 .w')];
 ws.forEach((w,i)=>{const p=ease((t-0.15-i*0.06)/0.26); w.style.opacity=p; w.style.transform=`translateY(${(1-p)*14}px)`;});
 const tEnd=0.15+ws.length*0.06+0.2;
 document.querySelectorAll('.ul').forEach((p,i)=>{p.style.strokeDashoffset=1-ease((t-tEnd-i*0.15)/0.4);});
 document.querySelectorAll('.dr').forEach(p=>{const q=ease((t-(+p.dataset.s))/(+p.dataset.d));p.style.strokeDashoffset=1-q;p.style.fillOpacity=q>0?1:0;});
 document.querySelectorAll('.ap').forEach(p=>{p.style.opacity=t>=+p.dataset.s?1:0;});
 document.querySelectorAll('.mv').forEach(g=>{const a=g.dataset.from.split(',').map(Number), b=g.dataset.to.split(',').map(Number), c=g.dataset.c.split(',').map(Number);
   const q=easeIO((t-(+g.dataset.s))/(+g.dataset.d)); const v=a.map((ai,i)=>ai+(b[i]-ai)*q);
   g.setAttribute('transform',`translate(${v[0]} ${v[1]}) rotate(${v[2]} ${c[0]} ${c[1]})`); g.style.opacity = t<+g.dataset.s && a[3]==0 ? 0 : v[3];});
 document.querySelector('.k').style.opacity=ease(t/0.25);
}"""
cor = "0 0 0 0 .97  0 0 0 0 .96  0 0 0 0 .94" if azul else "0 0 0 0 .2  0 0 0 0 .2  0 0 0 0 .25"
def page_html(c):
    svg = c["svg"].replace('"FG"', f'"{fg}"').replace('"AM"', f'"{am}"').replace('"BG"', f'"{bg}"')
    return f"""<html><head><meta charset=utf-8><style>{css}</style></head><body><div id=cam>{grao.replace('COR', cor)}
<svg class=top width=1080 height=1920><defs><filter id="rough2"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter></defs><g fill="none" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" filter="url(#rough2)">{svg}</g></svg>
<svg id=top class=top width=1080 height=1920><defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="11"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter></defs></svg>
<div class=c><div><div class=k>{html.escape(d['etiqueta'])}</div><h1>{words(c['texto'])}</h1></div><div class=f><span>bem.contado</span><span>@bem.contadopt</span></div></div></div></body></html>"""
files = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":W,"height":H})
    for i, c in enumerate(d["cenas"], 1):
        pg.set_content(page_html(c)); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.evaluate(setup_js.replace("FGC", fg).replace("AMC", am))
        dur = float(c.get("dur", 4.0)); tmp = f"v{i}.tmp.mp4"
        pg.evaluate(anim_js, dur - 0.05); pg.screenshot(path=f"video_cena_{i}.png")
        ff = subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-r",str(FPS),tmp], stdin=subprocess.PIPE)
        for fr in range(int(round(dur*FPS))):
            pg.evaluate(anim_js, fr/FPS); ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); assert ff.wait() == 0; os.rename(tmp, f"v{i}.mp4"); files.append(f"v{i}.mp4")
    b.close()
open("lista_video.txt","w").write("".join(f"file '{f}'\n" for f in files))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","lista_video.txt","-c","copy","final.tmp.mp4"], check=True)
os.rename("final.tmp.mp4", out)
