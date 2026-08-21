/* ============================================================
   AI MATURITY CHECK
   Sixteen questions across five axes. Context questions (size,
   sector, market, function) carry no score: they shape the advice.
   ============================================================ */
(function(){
var $=function(s){return document.querySelector(s)};
var push=function(name,data){
  window.dataLayer=window.dataLayer||[];
  window.dataLayer.push(Object.assign({event:name},data||{}));
};

/* id, axis label, question, help, options|null, weights, {free, optional, cols} */
var QS=[
["size","AZIENDA","Quante persone siete?","Serve a calibrare cosa è realistico nei prossimi 90 giorni.",
 [["1–9","Micro impresa o studio professionale."],["10–49","Piccola impresa strutturata."],
  ["50–249","Media impresa con funzioni distinte."],["250+","Grande organizzazione o gruppo."]],{},{cols:2}],
["sector","SETTORE","In che settore lavorate?","Il settore cambia i casi d’uso che pagano davvero.",
 [["Servizi B2B e consulenza","Progetti, ore, proposte, delivery."],["Manifattura e industria","Produzione, supply chain, qualità."],
  ["Retail ed e-commerce","Vendita, catalogo, assistenza clienti."],["Sanità e farma","Cura, compliance, dati sensibili."],
  ["Finanza e assicurazioni","Rischio, istruttorie, normativa."],["Education e formazione","Didattica, studenti, contenuti."],
  ["PA e non profit","Servizi al pubblico, bandi, rendicontazione."],["Altro","Nessuna delle precedenti."]],{},{cols:2}],
["market","MERCATO","Vendete soprattutto a imprese o a persone?","Cambia il funnel, i canali e la misurazione.",
 [["B2B","Clienti aziendali, cicli lunghi, poche trattative di valore."],
  ["B2C","Consumatori finali, volumi alti, decisione rapida."],
  ["Entrambi","Due motori diversi che convivono."]],{},{}],
["goal","OBIETTIVI","Quali risultati vuoi sbloccare per primi?","Puoi sceglierne più di uno: sono le pressioni dei prossimi 90 giorni.",
 [["Più tempo","Ridurre lavoro manuale e passaggi ripetitivi."],
  ["Più qualità","Meno errori, risposte più coerenti, decisioni migliori."],
  ["Più crescita","Generare, qualificare o seguire meglio domanda e clienti."],
  ["Più controllo","Rendere informazioni e processi osservabili."]],{processi:2,adozione:1},{multi:true,cols:2}],
["funzione","FUNZIONI","Quali funzioni sono più sotto pressione?","Seleziona tutte quelle che senti. Da qui esce la formazione mirata, non quella generica.",
 [["Marketing e vendite","Contenuti, campagne, offerte, follow-up."],
  ["Operations e delivery","Produzione del servizio o del prodotto."],
  ["Amministrazione e finanza","Documenti, controllo, adempimenti."],
  ["Customer service","Richieste, assistenza, post-vendita."],
  ["Tecnologia e prodotto","Sviluppo, dati, sistemi."],
  ["Management e direzione","Decisioni, riunioni, reportistica."],
  ["HR e personale","Selezione, onboarding, formazione, amministrazione del personale."],
  ["Tutta l’azienda","La pressione è distribuita."]],{},{multi:true,cols:2}],
["dati","DATI","Quanto sono disponibili i dati che servono?","Pensa a clienti, vendite, operazioni e performance.",
 [["Bisogna cercarli","Sparsi, poco affidabili o in ritardo."],
  ["Ci sono, ma manuali","Esportazioni e fogli aiutano, ma costano lavoro."],
  ["Abbastanza accessibili","Database, dashboard o API per i dati principali."],
  ["Già utilizzabili","Dati definiti, aggiornati, con responsabilità chiare."]],{dati:3},{}],
["sistemi","SISTEMI","Dove vive oggi il lavoro?","Non cercare la risposta ideale: scegli quella più vera.",
 [["In testa alle persone","Passaggi informali, tra mail, chat e memoria."],
  ["In fogli e documenti","Soprattutto Excel, Drive, PDF, presentazioni."],
  ["In software separati","CRM, ERP o verticali che non dialogano."],
  ["In un flusso connesso","I sistemi principali sono integrati o pronti a esserlo."],
  ["Dipende dalla business unit","Reparti diversi lavorano in modi diversi, con strumenti diversi."]],{dati:1,processi:2},{cols:2}],
["canali","MARKETING","Come vi fate trovare oggi?","Il canale decide quali dati esistono.",
 [["Passaparola e rete personale","Poca presenza costruita."],
  ["Sito e social organici","Presenza digitale, senza spesa in media."],
  ["Campagne a pagamento","Google, Meta, LinkedIn o TikTok attivi."],
  ["Mix strutturato","Digitale a pagamento e organico, con un piano."]],{marketing:3},{}],
["lineari","MARKETING","Usate anche canali offline o lineari?","Fiere, stampa, radio, TV, affissioni.",
 [["No, solo digitale","Tutto passa da canali online."],
  ["Fiere ed eventi","Presenza fisica sul mercato di riferimento."],
  ["Stampa o radio locale","Copertura territoriale."],
  ["TV, radio o affissioni","Campagne offline continuative."]],{marketing:1},{}],
["social","MARKETING","Presidiate i social?","Non conta essere ovunque: conta la costanza.",
 [["No","Nessun presidio attivo."],
  ["Sì, saltuariamente","Si pubblica quando capita."],
  ["Piano editoriale regolare","C’è un calendario e qualcuno che lo tiene."],
  ["Team o agenzia dedicata","Produzione continua e misurata."]],{marketing:2},{}],
["misurazione","MISURAZIONE","Quali strumenti di misurazione avete?","È la differenza fra decidere e indovinare.",
 [["Nessuno","Guardiamo i risultati commerciali e basta."],
  ["Analytics di base","GA4 o simili, installato ma poco usato."],
  ["Analytics e tag manager","Eventi e conversioni definiti, CRM collegato in parte."],
  ["Modello unificato","Definizioni condivise, dashboard e attribuzione."]],{marketing:2,dati:2},{}],
["agenzia","PARTNER","Vi appoggiate a un’agenzia esterna?","Serve a capire dove stanno dati e competenze.",
 [["No, tutto interno","Il team fa da sé."],
  ["Sì, per creatività e contenuti","Produzione affidata fuori."],
  ["Sì, per media buying","Le campagne le gestisce l’agenzia."],
  ["Sì, full service","Strategia, creatività e media fuori casa."]],{competenze:1},{}],
["formazione","COMPETENZE","Che formazione avete fatto sull’AI?","Non è un test di competenza tecnica.",
 [["Nessuna","Chi sa, ha imparato da solo."],
  ["Sessioni introduttive","Una tantum, uguale per tutti."],
  ["Formazione per alcune funzioni","Percorsi mirati su qualche team."],
  ["Percorsi continui","Formazione ricorrente, legata ai processi reali."]],{competenze:3},{}],
["tecnologia","TECNOLOGIA","Qual è il vostro rapporto con gli strumenti AI?","Conta l’uso reale, non le licenze attive.",
 [["Sperimentazione individuale","Qualcuno usa ChatGPT o Copilot, senza metodo comune."],
  ["Team curioso","Ci sono prove, ma nessun caso d’uso è entrato nel processo."],
  ["Primi workflow","Automazioni o assistenti usati in modo regolare."],
  ["Capacità interna","Il team sa valutare, integrare e governare strumenti e API."]],{competenze:2,adozione:2},{}],
["governance","GOVERNANCE","Chi decide cosa può fare l’AI con dati e processi?","Questa è una domanda di fiducia, non di burocrazia.",
 [["Nessuno in particolare","Non abbiamo regole o responsabilità definite."],
  ["Regole informali","Ci sono cautele, non condivise né documentate."],
  ["Un responsabile","Qualcuno valuta dati, rischi e strumenti prima dell’uso."],
  ["Un modo di lavorare","Policy, responsabilità e verifiche dentro il processo."]],{governance:3},{}],
["norme","NORMATIVA","Quanto conoscete le regole che vi riguardano?","AI Act, GDPR, mercato unico digitale: non serve essere giuristi, serve sapere cosa vi tocca.",
 [["Ne abbiamo sentito parlare","Sappiamo che esistono, non cosa comportano per noi."],
  ["Conosciamo il GDPR","Privacy presidiata; sull’AI Act siamo scoperti."],
  ["Stiamo mappando gli obblighi","Qualcuno sta guardando classificazione dei sistemi e adempimenti."],
  ["Presidio strutturato","Ruoli, registro dei sistemi e verifiche periodiche, con supporto legale."]],{governance:3},{}]
];

var AXES={dati:"DATI",processi:"PROCESSI",marketing:"MARKETING",competenze:"COMPETENZE",governance:"GOVERNANCE",adozione:"ADOZIONE"};
var RADAR=["dati","processi","marketing","competenze","governance"];
var state={i:0,a:{},started:0,sent:false};

/* ---------------- rail ---------------- */
function rail(){
  var s=score(),html="<ul>";
  RADAR.forEach(function(k){
    var on=(QS[state.i][5]||{})[k]?" on":"";
    html+='<li class="'+on.trim()+'">'+AXES[k]+'<span class="track"><i style="width:'+s[k]+'%"></i></span></li>';
  });
  $("#rail").innerHTML=html+"</ul>";
}

function toTop(){
  var flow=$("#flow"),bar=$("#topbar");
  if(!flow)return;
  var y=flow.getBoundingClientRect().top+(window.pageYOffset||0)
        -((bar&&!bar.hidden?bar.offsetHeight:0)+12);
  var smooth=!matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(window.scrollTo)window.scrollTo(smooth?{top:Math.max(0,y),behavior:"smooth"}:0,smooth?undefined:Math.max(0,y));
}

/* ---------------- one step ---------------- */
function render(dir){
  var q=QS[state.i],a=state.a[q[0]],opt=q[6]||{},box=$("#answers"),card=$("#card");
  var pct=Math.round((state.i+1)*100/QS.length);
  $("#topfill").style.width=pct+"%";
  $("#topnum").textContent=pct+"% completato";
  $("#title").textContent=q[2];
  $("#help").textContent=q[3];
  $("#back").hidden=state.i===0;
  $("#next").innerHTML=(state.i===QS.length-1?"Genera la mappa":"Continua")+" <em>→</em>";
  box.innerHTML="";
  var oldHint=$("#multi-hint");if(oldHint)oldHint.remove();
  $("#free-wrap").hidden=!opt.free;

  if(opt.free){
    $("#free").value=a?a.text:"";
    $("#count").textContent=$("#free").value.length;
    $("#next").disabled=false;                   // free text is optional
  }else{
    box.className="answers-grid"+(opt.cols===2?" cols2":"")+(opt.multi?" multi":"");
    var picked=(a&&a.ns)||[];
    q[4].forEach(function(o,n){
      var b=document.createElement("button");
      b.type="button";
      b.className="answer"+(opt.multi?(picked.indexOf(n)>=0?" selected":""):(a&&a.n===n?" selected":""));
      b.style.setProperty("--i",n);
      b.innerHTML="<b>"+(opt.multi?"+":"0"+(n+1))+"</b>"+o[0]+"<small>"+o[1]+"</small>";
      b.onclick=function(){
        if(opt.multi){
          var at=picked.indexOf(n);
          if(at>=0)picked.splice(at,1);else picked.push(n);
          picked.sort(function(x,y){return x-y});
          b.classList.toggle("selected",picked.indexOf(n)>=0);
          if(!picked.length){delete state.a[q[0]];$("#next").disabled=true;rail();return}
          state.a[q[0]]={
            ns:picked,
            n:Math.round(picked.reduce(function(t,k){return t+k},0)/picked.length),
            text:picked.map(function(k){return q[4][k][0]}).join(", "),
            detail:picked.map(function(k){return q[4][k][1]}).join(" ")};
        }else{
          state.a[q[0]]={n:n,text:o[0],detail:o[1]};
          [].forEach.call(box.children,function(c){c.classList.remove("selected")});
          b.classList.add("selected");
        }
        $("#next").disabled=false;
        rail();
      };
      box.appendChild(b);
    });
    $("#next").disabled=!a;
    if(opt.multi&&!$("#multi-hint")){
      var hint=document.createElement("small");
      hint.id="multi-hint";hint.textContent="Scelta multipla — seleziona tutte quelle che valgono.";
      box.parentNode.insertBefore(hint,box);
    }
  }
  card.classList.remove("out");
  card.classList.remove("in");
  void card.offsetWidth;                          // restart the animation
  card.classList.add("in");
  rail();
  // a long list of answers leaves you far down the page: the next question has
  // to start from its own top, not wherever the previous one ended
  if(dir) toTop();
}

function step(delta){
  var card=$("#card");
  card.classList.remove("in");card.classList.add("out");
  setTimeout(function(){state.i+=delta;render(true)},170);
}

/* ---------------- scoring ---------------- */
function score(){
  var raw={},max={};
  RADAR.forEach(function(k){raw[k]=0;max[k]=0});
  raw.adozione=0;max.adozione=0;
  QS.forEach(function(q){
    var w=q[5]||{},opt=q[6]||{},a=state.a[q[0]];
    Object.keys(w).forEach(function(k){
      max[k]+=w[k]*3;
      if(!a) return;
      raw[k]+=opt.free?(a.text&&a.text.trim()?w[k]*2:0):a.n*w[k];
    });
  });
  var out={};
  Object.keys(raw).forEach(function(k){out[k]=max[k]?Math.round(20+80*raw[k]/max[k]):50});
  return out;
}
function overall(s){
  var t=0;RADAR.forEach(function(k){t+=s[k]});
  return Math.round(t/RADAR.length);
}

/* ---------------- the plan ----------------
   The sequence is deliberate and nearly the same for everyone: training when
   it is missing, then workshops with the business units, then what to build
   and what it is worth, then two agents in production. Only two blocks are
   conditional — marketing data, and how far the aggregation promise can go. */
function plan(s){
  var fn=(state.a.funzione||{}).text||"le funzioni sotto pressione",
      canali=(state.a.canali||{}).n||0,
      social=(state.a.social||{}).n||0,
      misura=(state.a.misurazione||{}).n||0,
      lineari=(state.a.lineari||{}).n||0,
      agenzia=(state.a.agenzia||{}).n||0,
      wins=[];

  if(s.competenze<60)
    wins.push({title:"Formazione prima di tutto",
      body:"Senza una base comune ogni strumento resta un esperimento personale. Mezza giornata "+
           "per tutti, poi un modulo per "+fn.toLowerCase()+"."});

  wins.push({title:"Workshop interni con le business unit",
    body:"Due o tre sessioni con chi fa il lavoro: si mappano i passaggi reali, non quelli del "+
         "manuale. È qui che si vede dove l’AI toglie tempo e dove non serve."});
  wins.push({title:"Tecnologie e colli di bottiglia",
    body:"Dai workshop esce la lista: quali strumenti avete già, quali servono davvero, e i punti "+
         "in cui il lavoro si ferma. Si sceglie a ragion veduta, non per moda."});
  wins.push({title:"ROI stimato per ogni iniziativa",
    body:"Ore risparmiate, errori evitati, ricavi sbloccati, costo di esercizio: ogni iniziativa "+
         "ha un numero prima di partire, così la priorità non è un’opinione."});
  wins.push({title:"Due agenti in produzione nei 90 giorni",
    body:"Non un pilota da dimostrazione: due agenti sui processi scelti, usati ogni giorno, con "+
         "criteri di qualità e un responsabile."});

  // marketing: only promise what their setup can actually deliver
  var attivi=(canali>=2?1:0)+(social>=2?1:0)+(lineari>=1?1:0);
  if(attivi>=2||misura>=1){
    wins.push({title:"Aggregazione dei dati di marketing",
      body:agenzia===0
        ? "Investite su più canali senza un partner che tenga insieme i numeri: si parte da "+
          "definizioni condivise e da un’unica base dati, un canale alla volta."
        : "Definizioni condivise e una sola base dati fra i canali e chi li gestisce, così i "+
          "numeri dell’agenzia e i vostri raccontano la stessa storia."});
  }

  wins.push({title:"Codice di condotta AI e posizionamento normativo",
    body:"Una pagina su cosa si può fare con quali dati, più la posizione su AI Act, GDPR e "+
         "Digital Services Act: serve a decidere in fretta, non a rallentare."});
  return wins;
}

function fallback(s){
  var low=RADAR.slice().sort(function(a,b){return s[a]-s[b]}),
      fn=(state.a.funzione||{}).text||"il team",
      sector=(state.a.sector||{}).text||"il vostro settore";
  return {
    title:overall(s)<55?"Le fondamenta vengono prima dell’automazione.":"C’è spazio per costruire, con una sequenza precisa.",
    summary:"Il punto non è aggiungere strumenti, è seguire una sequenza: capire il lavoro com’è "+
      "davvero, scegliere dove l’AI paga, misurarlo, e mettere in produzione poche cose che "+
      "funzionano. L’anello più debole oggi è "+AXES[low[0]].toLowerCase()+".",
    wins:plan(s),
    training:[
      {title:"Alfabetizzazione AI per tutta l’azienda",
       body:"Mezza giornata comune: cosa sa e cosa non sa fare un modello, dati che non si "+
            "incollano, come si verifica un output."},
      {title:"Formazione mirata su "+fn.toLowerCase(),
       body:"Casi reali delle funzioni più sotto pressione in "+sector.toLowerCase()+", con i "+
            "prompt e i controlli di qualità del vostro processo."}],
    advice:"Evita progetti troppo ampi. Un AI Opportunity Sprint mette in fila workshop, scelta "+
      "delle tecnologie, ROI e i primi due agenti, con la formazione che li rende usabili."};
}

/* ---------------- radar ---------------- */
function radar(s,t){
  var c=$("#radar"),r=(c.parentNode||c).getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);  // measure the container: the canvas own width is whatever we last set
  var z=Math.max(280,Math.min(r.width||320,620)),x=z/2,y=z/2,ctx=c.getContext("2d");
  var fs=Math.max(9,z*.023),pad=fs*3.4,R=(z/2-pad)*.92;
  // the element used to stretch to the container while the backing store stayed
  // at 640: that is the softness. Pin both to the same size.
  c.width=z*d;c.height=z*d;c.style.width=z+"px";c.style.height=z+"px";
  ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,z,z);
  var ang=function(i){return -Math.PI/2+i*Math.PI*2/RADAR.length};
  for(var n=1;n<5;n++){
    ctx.beginPath();
    RADAR.forEach(function(k,i){var q=R*n/4;
      var X=x+Math.cos(ang(i))*q,Y=y+Math.sin(ang(i))*q;i?ctx.lineTo(X,Y):ctx.moveTo(X,Y)});
    ctx.closePath();ctx.strokeStyle="rgba(236,234,228,.14)";ctx.lineWidth=1;ctx.stroke();
  }
  ctx.font="600 "+fs+"px "+"SFMono-Regular,Menlo,monospace";
  RADAR.forEach(function(k,i){
    ctx.beginPath();ctx.moveTo(x,y);
    ctx.lineTo(x+Math.cos(ang(i))*R,y+Math.sin(ang(i))*R);
    ctx.strokeStyle="rgba(236,234,228,.14)";ctx.stroke();
    // labels used to run past the canvas edge; keep them inside by measuring
    var lx=x+Math.cos(ang(i))*(R+fs*1.5),ly=y+Math.sin(ang(i))*(R+fs*1.5)+fs*.36;
    var w=ctx.measureText(AXES[k]).width,half=w/2;
    ctx.textAlign="center";
    if(lx-half<4){ctx.textAlign="left";lx=4}
    else if(lx+half>z-4){ctx.textAlign="right";lx=z-4}
    ctx.fillStyle="#a6a3a9";ctx.fillText(AXES[k],lx,ly);
  });
  ctx.beginPath();
  RADAR.forEach(function(k,i){var q=R*(s[k]/100)*t;
    var X=x+Math.cos(ang(i))*q,Y=y+Math.sin(ang(i))*q;i?ctx.lineTo(X,Y):ctx.moveTo(X,Y)});
  ctx.closePath();
  ctx.fillStyle="rgba(255,74,43,.2)";ctx.fill();
  ctx.strokeStyle="#ff4a2b";ctx.lineWidth=2;ctx.stroke();
  RADAR.forEach(function(k,i){var q=R*(s[k]/100)*t;
    ctx.beginPath();ctx.arc(x+Math.cos(ang(i))*q,y+Math.sin(ang(i))*q,3,0,7);
    ctx.fillStyle="#ff4a2b";ctx.fill()});
}
function radarIn(s){
  var t0=performance.now(),dur=900;
  (function frame(now){
    var p=Math.min(1,(now-t0)/dur),e=1-Math.pow(1-p,3);
    radar(s,e);
    if(p<1)requestAnimationFrame(frame);
  })(t0);
}
function countTo(v){
  var el=$("#score"),t0=performance.now(),dur=900;
  (function frame(now){
    var p=Math.min(1,(now-t0)/dur);
    el.textContent=Math.round(v*(1-Math.pow(1-p,3)));
    if(p<1)requestAnimationFrame(frame);
  })(t0);
}

/* ---------------- result ---------------- */
function list(target,items,mark){
  var box=$(target);box.innerHTML="";
  items.forEach(function(w,i){
    var e=document.createElement("article");
    e.className="win";
    e.innerHTML="<span>"+mark+("0"+(i+1)).slice(-2)+"</span><strong></strong><p></p>";
    e.querySelector("strong").textContent=w.title;
    e.querySelector("p").textContent=w.body;
    box.appendChild(e);
  });
}
function show(s,r){
  state.report=r;state.scores=s;
  $("#loading").hidden=true;$("#result").hidden=false;
  $("#topbar").hidden=true;document.body.classList.remove("running");
  $("#result-title").textContent=r.title;
  $("#summary").textContent=r.summary;
  $("#advice").textContent=r.advice;
  list("#win-list",plan(s),"");
  var tr=(r.training&&r.training.length?r.training:fallback(s).training);
  list("#training-list",tr,"");
  $("#result").scrollIntoView({behavior:"smooth",block:"start"});
  countTo(overall(s));
  requestAnimationFrame(function(){radarIn(s)});
  push("ai_maturity_complete",{ai_score:overall(s),ai_dati:s.dati,ai_processi:s.processi,
    ai_marketing:s.marketing,ai_competenze:s.competenze,ai_governance:s.governance,
    ai_settore:(state.a.sector||{}).text||"",ai_dimensione:(state.a.size||{}).text||"",
    ai_mercato:(state.a.market||{}).text||"",
    ai_durata_sec:Math.round((Date.now()-state.started)/1000)});
}
function done(){
  var s=score(),f=fallback(s);
  $("#flow").hidden=true;$("#loading").hidden=false;
  $("#topfill").style.width="100%";$("#topnum").textContent="100% completato";
  $("#loading").scrollIntoView({block:"start"});
  fetch("/api/ai-maturity",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({answers:state.a,scores:s})})
    .then(function(x){return x.ok?x.json():f})
    .then(function(x){show(s,x&&x.summary?x:f)})
    .catch(function(){show(s,f)});
}

/* ---------------- lead ---------------- */
function transcript(){
  var s=state.scores||score(),rows=["Richiesta dalla pagina AI Maturity Check.","",
    "PUNTEGGIO COMPLESSIVO: "+overall(s)+"/100"];
  RADAR.forEach(function(k){rows.push("  "+AXES[k]+": "+s[k])});
  rows.push("","RISPOSTE:");
  QS.forEach(function(q){
    var a=state.a[q[0]];
    if(!a||!a.text)return;
    rows.push("  "+q[2]+" → "+a.text+(a.detail?" ("+a.detail+")":""));
  });
  if(state.report){
    rows.push("","SINTESI: "+state.report.title,state.report.summary,"","QUICK WIN:");
    (state.report.wins||[]).forEach(function(w){rows.push("  - "+w.title+": "+w.body)});
    if(state.report.training&&state.report.training.length){
      rows.push("","FORMAZIONE:");
      state.report.training.forEach(function(w){rows.push("  - "+w.title+": "+w.body)});
    }
    rows.push("","PRIMO PASSO: "+state.report.advice);
  }
  return rows.join("\n");
}
function sent(address){
  var form=$("#lead-form");
  form.classList.remove("sending");
  var box=document.createElement("div");
  box.className="sent";
  box.innerHTML='<svg viewBox="0 0 40 40" aria-hidden="true">'+
    '<circle cx="20" cy="20" r="18"/><path d="M12 20.5l5.5 5.5L28 15"/></svg>'+
    '<div><b>Mappa inviata.</b>'+
    '<p>È partita a <span class="to"></span>. Ti scrivo io a breve, di persona, '+
    'per dirti da dove partirei nel tuo caso.</p></div>';
  box.querySelector(".to").textContent=address;
  var section=form.parentNode;
  section.replaceChild(box,form);
  $("#l-msg")&&$("#l-msg").remove();
  // the "name, surname and email" line has nothing left to explain
  var note=section.querySelector("small");
  if(note)note.remove();
  box.scrollIntoView({behavior:"smooth",block:"center"});
}

function lead(e){
  e.preventDefault();
  var first=$("#l-first"),last=$("#l-last"),mail=$("#l-email"),msg=$("#l-msg");
  [first,last,mail].forEach(function(f){f.classList.remove("bad")});
  var ok=first.value.trim()&&last.value.trim()&&/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(mail.value.trim());
  if(!ok){
    [first,last].forEach(function(f){if(!f.value.trim())f.classList.add("bad")});
    if(!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(mail.value.trim()))mail.classList.add("bad");
    msg.textContent="Servono nome, cognome e un indirizzo email valido.";msg.className="formmsg";
    return;
  }
  var name=first.value.trim()+" "+last.value.trim(),body=transcript(),
      sc=state.scores||score(),
      rep=state.report||fallback(sc),
      payload={
        score:overall(sc),
        axes:RADAR.map(function(k){return {name:AXES[k],value:sc[k]}}),
        title:rep.title,summary:rep.summary,advice:rep.advice,
        wins:plan(sc),
        answers:QS.map(function(q){
          var a=state.a[q[0]];
          return a&&a.text?{q:q[2],a:a.text,detail:a.detail||""}:null;
        }).filter(Boolean),
        training:(rep.training&&rep.training.length?rep.training:fallback(sc).training)
      };
  msg.textContent="Invio in corso…";msg.className="formmsg";
  $("#lead-form").classList.add("sending");
  $("#l-send").disabled=true;
  fetch("/api/contact",{method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({name:name,email:mail.value.trim(),topic:"AI Maturity Check",
      message:body,report:payload,website:$("#l-site").value,page:location.pathname})})
   .then(function(r){
     if(r.ok){
       sent(mail.value.trim());
       if(!state.sent){state.sent=true;push("ai_maturity_lead",{ai_score:overall(state.scores||score())})}
       return;
     }
     throw new Error("fallback");
   })
   .catch(function(){
     // no mail credentials on the server: hand the whole thing to a mail client
     $("#lead-form").classList.remove("sending");
     msg.textContent="Apro il tuo client di posta con il riepilogo già dentro.";
     msg.className="formmsg ok";
     if(!state.sent){state.sent=true;push("ai_maturity_lead",{ai_score:overall(state.scores||score()),ai_invio:"mailto"})}
     location.href="mailto:alessandro@iside.systems?subject="+
       encodeURIComponent("AI Maturity Check — "+name)+"&body="+encodeURIComponent(body);
   })
   .then(function(){$("#l-send").disabled=false;$("#lead-form").classList.remove("sending")});
}

/* ---------------- wiring ---------------- */
$("#start").onclick=function(){
  state.started=Date.now();
  $("#intro").hidden=true;$("#flow").hidden=false;
  $("#topbar").hidden=false;document.body.classList.add("running");
  push("ai_maturity_start",{ai_domande:QS.length});
  render(true);
};
$("#next").onclick=function(){if(state.i===QS.length-1)done();else step(1)};
$("#back").onclick=function(){if(state.i>0)step(-1)};
$("#free").oninput=function(e){
  state.a[QS[state.i][0]]={text:e.target.value};
  $("#count").textContent=e.target.value.length;
};
$("#lead-form").addEventListener("submit",lead);
$("#restart").onclick=function(){location.reload()};
addEventListener("keydown",function(e){
  if($("#flow").hidden)return;
  var q=QS[state.i],opt=q[6]||{};
  if(!opt.free&&e.key>="1"&&e.key<="9"){
    var b=$("#answers").children[+e.key-1];
    if(b){b.click();e.preventDefault()}
  }
  if(e.key==="Enter"&&!$("#next").disabled&&document.activeElement.tagName!=="TEXTAREA")$("#next").click();
});
addEventListener("resize",function(){if(!$("#result").hidden)radar(state.scores||score(),1)});
})();
