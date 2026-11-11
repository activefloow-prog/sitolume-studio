#!/usr/bin/env python3
"""Luca Cloud Studio: original visual assets for Sito Lume; no local Mac usage.
Requires Pillow. 1080x1350 feed / carousel, 1080x1920 story and reel frames.
Never publishes to Instagram. Promotional examples only; no fake client proof.
"""
import argparse, json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

C = {"bg": (9,9,12), "panel": (20,20,24), "lime": (237,194,112),
     "white": (247,244,235), "muted": (194,183,170), "gold": (214,165,87)}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CONTENT = [
  {"number":"01","eyebrow":"PRESENZA DIGITALE","title":["IL TUO SITO","LAVORA PER TE?"],"highlight":1,"body":"Un bel sito non basta. Deve aiutare le persone a capire cosa offri.","pill":"SCOPRI I 3 ERRORI PIU COMUNI"},
  {"number":"02","eyebrow":"ERRORE N. 1","title":["NON SI CAPISCE","COSA OFFRI"],"highlight":1,"body":"Chi visita da smartphone deve capire il tuo servizio in pochi secondi.","pill":"CHIAREZZA PRIMA DI TUTTO"},
  {"number":"03","eyebrow":"ERRORE N. 2","title":["TROPPI CLICK","PER CONTATTARTI"],"highlight":1,"body":"Un percorso semplice verso chiamata e preventivo migliora l'esperienza.","pill":"SEMPLIFICA IL CONTATTO"},
  {"number":"04","eyebrow":"ERRORE N. 3","title":["NESSUNA FIDUCIA","A PRIMA VISTA"],"highlight":1,"body":"Testi leggibili, servizi chiari e design curato contano davvero.","pill":"RENDi IL VALORE VISIBILE"},
  {"number":"05","eyebrow":"SITO LUME • ITALIA","title":["UN SITO CHE","TI RAPPRESENTA"],"highlight":1,"body":"Progettiamo esperienze web professionali per attivita in tutta Italia.","pill":"SCRIVICI DAL SITO"},
]
CAPTION = ("Hai un'attivita e vuoi capire se il tuo sito comunica davvero il tuo valore?\n\n"
 "Ecco 3 errori comuni: messaggio poco chiaro, contatto complicato e mancanza di fiducia visiva.\n\n"
 "In Sito Lume progettiamo siti professionali pensati per essere chiari, accessibili e coerenti con la tua attivita. "
 "La prima valutazione parte da una conversazione concreta.\n\n"
 "Scopri di piu dal link in bio.\n\n#SitoLume #SitiWeb #WebDesignItalia #PiccoleImprese #PresenzaOnline")
VOICE_TEXT = (
 "Un sito web bello non basta. Deve farti capire al primo sguardo. "
 "Se i servizi sono confusi, i contatti nascosti e il design poco curato, "
 "le persone possono andarsene. Sito Lume: siti web professionali per attivita in tutta Italia. "
 "Scopri il nostro lavoro dal link in bio."
)

SERIES = [
    (CONTENT, CAPTION, VOICE_TEXT),
    ([
        {"number":"01","eyebrow":"PRIMA IMPRESSIONE","title":["IL TUO SITO","E CHIARO?"],"highlight":1,"body":"Un visitatore deve capire subito chi sei e perche contattarti.","pill":"INIZIA DALLA CHIAREZZA"},
        {"number":"02","eyebrow":"MOBILE FIRST","title":["BELLO ANCHE","SUL TELEFONO"],"highlight":1,"body":"Testi leggibili e pulsanti facili da usare migliorano l'esperienza.","pill":"PENSA ALLO SMARTPHONE"},
        {"number":"03","eyebrow":"PERCORSO CLIENTE","title":["CONTATTO FACILE","SENZA CACCIA"],"highlight":1,"body":"Rendi evidente il numero e il modulo per chiedere informazioni.","pill":"UN CLICK BEN POSIZIONATO"},
        {"number":"04","eyebrow":"FIDUCIA DIGITALE","title":["SERVIZI E PREZZI","SENZA CONFUSIONE"],"highlight":1,"body":"Spiega cosa fai e come funziona la tua consulenza.","pill":"TRASPARENZA CONCRETA"},
        {"number":"05","eyebrow":"SITO LUME","title":["LA TUA AZIENDA","MERITA CURA"],"highlight":1,"body":"Progettiamo siti chiari e moderni per attivita in tutta Italia.","pill":"VISITA IL NOSTRO SITO"}],
     "Il sito della tua attivita e davvero semplice da usare da smartphone? Ecco quattro aspetti utili da controllare. Progettiamo esperienze chiare per imprese in tutta Italia. Scopri Sito Lume dal link in bio.\n\n#SitoLume #WebDesign #SitiWebProfessionali #ImpresaItalia",
     "Un cliente visita il tuo sito dal telefono. Riesce a capire cosa offri, quali servizi proponi e come contattarti? Se la risposta non e chiara, e il momento di rivedere l'esperienza. Sito Lume, siti professionali per tutta Italia."),
    ([
        {"number":"01","eyebrow":"ESPERIENZA DIGITALE","title":["DA VISITATORE","A CONTATTO"],"highlight":1,"body":"Ogni pagina dovrebbe guidare le persone con semplicita.","pill":"SEGUI IL PERCORSO"},
        {"number":"02","eyebrow":"IDENTITA","title":["MOSTRA CHI SEI","SENZA ECCESSI"],"highlight":1,"body":"Le tue foto originali e una presentazione sincera contano.","pill":"AUTENTICITA PRIMA DI TUTTO"},
        {"number":"03","eyebrow":"SERVIZI","title":["POCHI MESSAGGI","MA CHIARI"],"highlight":1,"body":"Organizza i servizi per rispondere alle domande frequenti.","pill":"RIDUCI LE DISTRAZIONI"},
        {"number":"04","eyebrow":"CONTATTO","title":["IL PROSSIMO PASSO","DEVE ESSERE SEMPLICE"],"highlight":1,"body":"Telefono, email e richiesta preventivo devono essere immediati.","pill":"CHIEDERE E FACILE"},
        {"number":"05","eyebrow":"SITO LUME","title":["FAI BRILLARE","LA TUA IMPRESA"],"highlight":1,"body":"Un progetto web su misura parte dall'ascolto del tuo lavoro.","pill":"PARLIAMONE INSIEME"}],
     "Un buon sito non costringe il visitatore a cercare informazioni: guida con chiarezza, foto autentiche e un contatto immediato. Se stai progettando una nuova presenza digitale, scopri Sito Lume.\n\n#SitoLume #WebDesignItalia #SitiWeb #PiccoleImprese",
     "Da visitatore a contatto: ogni dettaglio del tuo sito ha un ruolo. Una presentazione autentica, servizi chiari e un modo semplice per chiedere informazioni. Sito Lume crea esperienze digitali curate per imprese in tutta Italia."),
    ([
        {"number":"01","eyebrow":"CHECKLIST SITO","title":["QUANDO SERVE","UN RESTYLING?"],"highlight":1,"body":"Non serve rifare tutto: prima individua i problemi veri.","pill":"FAI UN CONTROLLO"},
        {"number":"02","eyebrow":"LEGGIBILITA","title":["TESTI TROPPO","PICCOLI?"],"highlight":1,"body":"Se devi ingrandire per leggere, migliora la versione mobile.","pill":"PRIORITA ALLA LETTURA"},
        {"number":"03","eyebrow":"VELOCITA","title":["UN SITO LENTO","STANCA"],"highlight":1,"body":"Immagini ottimizzate e pagine leggere fanno la differenza.","pill":"PROVA SU MOBILE"},
        {"number":"04","eyebrow":"IDENTITA","title":["IL TUO BRAND","SI RICONOSCE?"],"highlight":1,"body":"Colori e tono coerenti aiutano la riconoscibilita.","pill":"COERENZA VISIVA"},
        {"number":"05","eyebrow":"SITO LUME","title":["UN PROGETTO WEB","PENSATO PER TE"],"highlight":1,"body":"Valutiamo soluzioni reali, senza promettere risultati impossibili.","pill":"SCOPRI I NOSTRI MODELLI"}],
     "Hai un sito che non ti convince piu? Prima di cambiare tutto, controlla testi, velocita, versioni mobile e coerenza visiva. Per una valutazione concreta, Sito Lume e online.\n\n#SitoLume #RestylingSito #WebDesigner #SitiWebItalia",
     "Il tuo sito ha bisogno di un restyling? Parti dalle cose concrete: leggibilita, velocita, identita e contatti chiari. Non sempre bisogna rifare tutto. In Sito Lume cerchiamo soluzioni pensate per la tua attivita.")
]

def chosen_series():
    import datetime
    idx=(datetime.datetime.now(datetime.timezone.utc).isocalendar().week-46)%len(SERIES)
    return SERIES[idx]

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, int(size))

def fit(draw,text,limit,start=71):
    sz=start
    while sz>30 and draw.textlength(text,font=font(sz,True))>limit: sz-=2
    return font(sz,True)

def background(w,h,seed):
    rng=random.Random(seed)
    bg=Image.new("RGB",(w,h),C["bg"])
    glows=Image.new("RGBA",(w,h),(0,0,0,0))
    d=ImageDraw.Draw(glows)
    for x,y,r,col in [(w*.89,h*.10,w*.68,(123,82,38,105)),
                       (-w*.20,h*.72,w*.64,(77,52,33,80)),
                       (w*.65,h*.86,w*.51,(74,59,40,65))]:
        d.ellipse((int(x-r),int(y-r),int(x+r),int(y+r)),fill=col)
    bg=Image.alpha_composite(bg.convert("RGBA"),glows.filter(ImageFilter.GaussianBlur(125))).convert("RGB")
    b=ImageDraw.Draw(bg)
    for j in range(0,w,61):
        b.line((j,0,j,h),fill=(24,22,22),width=1)
    for j in range(0,h,61):
        b.line((0,j,w,j),fill=(17,30,23),width=1)
    for _ in range(55):
        x=rng.randrange(75,w-75);y=rng.randrange(100,h-100)
        b.ellipse((x,y,x+1,y+1),fill=(74,62,49))
    return bg

def brand(im,draw,w,h,scale):
    pad=round(82*scale)
    top=round((300 if h>1500 else 82)*scale)
    official=Path(__file__).resolve().parent.parent/"assets"/"email"/"sitolume-signature.png"
    if not official.is_file(): raise FileNotFoundError("Official Sito Lume logo missing")
    logo=Image.open(official).convert("RGBA").resize((round(55*scale),round(55*scale)))
    im.paste(logo,(pad,top),logo)
    draw.text((pad+73*scale,top+8*scale),"SITO LUME",font=font(24*scale,True),fill=C["white"])
    draw.text((pad+74*scale,top+40*scale),"STUDIO DIGITALE",font=font(14*scale),fill=C["muted"])

def slide(item,w,h,seed):
    scale=w/1080
    im=background(w,h,seed)
    d=ImageDraw.Draw(im)
    brand(im,d,w,h,scale)
    pad=round(86*scale);mid=int(h*.53)
    d.rounded_rectangle((pad,int(h*.22),w-pad,int(h*.79)),radius=28*scale,fill=C["panel"],outline=(85,65,45),width=2)
    d.rounded_rectangle((pad+36*scale,int(h*.29),pad+172*scale,int(h*.29)+6*scale),radius=3*scale,fill=C["lime"])
    d.text((pad+36*scale,int(h*.315)),item["eyebrow"],font=font(21*scale,True),fill=C["lime"])
    y=int(h*.394)
    for idx,t in enumerate(item["title"]):
        f=fit(d,t,w-2*pad-70*scale,start=69*scale)
        color=C["lime"] if idx==item["highlight"] else C["white"]
        d.text((pad+35*scale,y),t,font=f,fill=color)
        y+=88*scale
    body=item["body"]
    words=body.split();lines=[];current=""
    for word in words:
        nxt=(current+" "+word).strip()
        if d.textlength(nxt,font=font(29*scale))>w-2*pad-92*scale and current:
            lines.append(current);current=word
        else:current=nxt
    if current:lines.append(current)
    for i,line in enumerate(lines[:4]):
        d.text((pad+37*scale,int(h*.605)+43*scale*i),line,font=font(29*scale),fill=C["muted"])
    pill=item["pill"].upper()
    by=int(h*.73)
    d.rounded_rectangle((pad+35*scale,by,w-pad-35*scale,by+58*scale),radius=16*scale,outline=(166,119,67),width=2)
    pf=fit(d,pill,w-2*pad-114*scale,start=22*scale)
    d.text((pad+57*scale,by+17*scale),pill,font=pf,fill=C["lime"])
    d.text((pad,int(h*.905)),item["number"]+" / 05",font=font(24*scale,True),fill=C["lime"])
    d.text((w-pad-530*scale,int(h*.91)),"sitolume-studio.pages.dev",font=font(20*scale),fill=C["muted"])
    return im

def story(w=1080,h=1920):
    im=background(w,h,88);d=ImageDraw.Draw(im)
    brand(im,d,w,h,1)
    d.rounded_rectangle((80,490,w-80,1500),radius=35,fill=C["panel"],outline=(51,73,56),width=3)
    d.text((123,620),"UN SITO",font=font(108,True),fill=C["white"])
    d.text((123,790),"CHE PARLA",font=font(100,True),fill=C["lime"])
    d.text((123,960),"DI TE.",font=font(125,True),fill=C["lime"])
    d.text((123,1180),"Siti web professionali",font=font(34),fill=C["muted"])
    d.text((123,1230),"per aziende in tutta Italia.",font=font(34),fill=C["muted"])
    d.rounded_rectangle((122,1350,650,1440),radius=20,fill=C["lime"])
    d.text((158,1377),"SCOPRI SITO LUME",font=font(31,True),fill=C["bg"])
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True);a=p.parse_args()
    root=Path(a.out);root.mkdir(parents=True,exist_ok=True)
    cards,caption,spoken=chosen_series()
    for i,item in enumerate(cards):
        im=slide(item,1080,1350,i+41)
        im.save(root/f"carousel-{i+1:02d}.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    slide(cards[0],1080,1350,101).save(root/"post-01.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    story().save(root/"story-01.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    # Vertical motion frames are assets for cloud Reel video build, not a published Reel.
    for i,item in enumerate([cards[0],cards[1],cards[3],cards[4]]):
        v=slide(item,1080,1920,i+71)
        v.save(root/f"reel-frame-{i+1:02d}.jpg","JPEG",quality=94,optimize=True,subsampling=0)
    manifest={"account":"sitolume_studio","format":"cloud-first","approved_for_publishing":False,
              "story":"story-01.jpg","post":"post-01.jpg",
              "carousel":[f"carousel-{i:02d}.jpg" for i in range(1,6)],
              "reel_frames":[f"reel-frame-{i:02d}.jpg" for i in range(1,5)],
              "voices":{"male":"Ryan","female":"Serena","model":"Qwen3-TTS"},
              "caption":caption,"tts_script":spoken,
              "status":"visual-assets-only-until-voice-and-review"}
    (root/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print("Luca Cloud Studio: 6 feed JPG, 1 story JPG, 4 motion frames + manifest")
if __name__=="__main__": main()
