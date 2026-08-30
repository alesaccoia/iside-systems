# -*- coding: utf-8 -*-
"""Il whitepaper «AI & Organizational Development», come pagina del sito.

Il testo è quello di Alessandro, riportato integralmente: qui cambia solo il
modo in cui è impaginato. Blocchi: p, cards, steps, table, stats, note, quote.
"""

LABELS = dict(
    kicker="Metodologia",
    title="AI &amp; Organizational Development",
    sub="Progettare la tecnologia dentro il lavoro.",
    lede="Introdurre un sistema di AI cambia il modo in cui le persone lavorano, decidono, "
         "apprendono e vengono valutate. La sua progettazione è quindi un problema organizzativo "
         "prima che tecnico.",
    meta="Whitepaper · 2026 · Alessandro Saccoia",
    strap="Cultura, diagnosi, sviluppo delle persone e design critico dei sistemi intelligenti.",
    toc="Le nove sezioni",
)

SECTIONS = [
dict(n="01", title="Executive summary",
     sub="Un progetto di AI si valuta sul contesto in cui entra, sul compito che assume, sugli "
         "effetti che produce e su chi li subisce.",
     blocks=[
  ("p", "Un sistema intelligente entra in una rete di attività interdipendenti, ruoli, identità e "
        "significati. Il suo valore organizzativo dipende da come viene incorporato nei processi "
        "che tengono insieme quella rete."),
  ("cards", [
    ("01 / Diagnostica", "Definire il problema prima dello strumento",
     "Un’affermazione come «le persone resistono all’AI» non costituisce una diagnosi. Una "
     "diagnosi richiede una catena esplicita, dal costrutto alle dimensioni, agli indicatori, ai "
     "dati, alla loro interpretazione e alla restituzione."),
    ("02 / Configura", "Automazione e augmentation come configurazioni",
     "Non sono proprietà del software ma modi di organizzare il lavoro. Lo stesso sistema può "
     "ampliare il margine di giudizio di un manager e ridurre quello di un collaboratore."),
    ("03 / Sviluppa", "Lo strumento è una parte dell’intervento",
     "L’intervento comprende co-design, formazione, nuove pratiche, governance e valutazione. "
     "Senza queste componenti l’organizzazione ottiene un software installato e nessun "
     "cambiamento nelle pratiche di lavoro.")]),
  ("h3", "La tesi"),
  ("p", "L’AI in azienda è una questione di sviluppo organizzativo prima che di modelli. "
        "L’accuratezza è necessaria ma non sufficiente, perché il significato di un sistema "
        "dipende da come ridefinisce scopi, ruoli, coordinamento, regole, valutazione e identità."),
  ("h3", "Come leggere questo documento"),
  ("p", "Le nove pagine seguono quattro passaggi. Si legge l’organizzazione e la sua cultura, si "
        "diagnostica con metodo, si sviluppano le persone, si progetta e si valuta un sistema di AI."),
 ]),

dict(n="02", title="Dove entra la tecnologia",
     sub="Sei processi organizzativi da esaminare prima di progettare un sistema.",
     blocks=[
  ("p", "Un’organizzazione è insieme struttura formale e <i>organizing</i>, cioè le pratiche "
        "informali e il sapere tacito senza cui il lavoro reale non funziona. Un sistema costruito "
        "sulla rappresentazione formale del lavoro incontra sempre quel margine."),
  ("cards", [
    ("01 / Finalizzazione", "Chi ha definito l’obiettivo?",
     "Un algoritmo ottimizzato su un solo indicatore porta a sacrificare qualità, apprendimento o "
     "benessere. Conviene chiedersi quali dimensioni sono state escluse dalla funzione obiettivo."),
    ("02 / Differenziazione", "Linguaggi diversi",
     "Data science, HR e prima linea intendono in modo diverso performance, errore ed equità. "
     "L’AI mette in contatto specializzazioni senza lingua comune."),
    ("03 / Integrazione", "Coordinamento o nuova frattura",
     "Il sistema può coordinare le informazioni oppure aprire una nuova frattura fra chi "
     "comprende il modello e chi ne segue soltanto l’output."),
    ("04 / Formalizzazione", "Ciò che è misurabile e ciò che conta",
     "L’algoritmo traduce criteri di giudizio in regole computabili. Il rischio è che ciò che il "
     "sistema misura venga preso per ciò che ha valore."),
    ("05 / Valutazione", "La misura modifica i comportamenti",
     "Più frequenza e precisione possono favorire apprendimento, o generare sorveglianza, ansia e "
     "adattamento opportunistico agli indicatori."),
    ("06 / Identificazione", "Minaccia all’identità professionale",
     "Quando l’AI assume un compito centrale per una professione, la resistenza riguarda "
     "l’identità di chi lo svolgeva più che la difficoltà d’uso.")]),
  ("note", "La resistenza segnala spesso una <b>perdita reale</b> di autonomia, competenza, "
           "appartenenza o potere, e non una scarsa familiarità con la tecnologia."),
 ]),

dict(n="03", title="Cultura organizzativa",
     sub="Sotto gli artefatti visibili agiscono valori dichiarati e assunti dati per scontato.",
     blocks=[
  ("cards", [
    ("Livello 1 — visibile", "Artefatti",
     "Spazi, tecnologie, dashboard, riunioni, linguaggio, procedure. Mostrano <i>che cosa</i> "
     "accade, non <i>perché</i>. Uno schermo con le performance in tempo reale può esprimere "
     "trasparenza e apprendimento oppure controllo e competizione, e l’artefatto da solo non dice "
     "quale dei due."),
    ("Livello 2 — dichiarato", "Valori espliciti",
     "Innovazione, autonomia, qualità, inclusione. La distanza fra valore dichiarato e pratica è "
     "un dato diagnostico. Se chi verifica un output risulta meno produttivo nei sistemi di "
     "misurazione, il valore praticato è la velocità."),
    ("Livello 3 — dato per scontato", "Assunti di base",
     "«I dati sono più affidabili delle persone». «Solo l’esperienza capisce davvero questo "
     "lavoro». «L’errore è una colpa da nascondere». Non sono scritti in nessuna policy, ma "
     "determinano la reazione all’AI. Dove i dati sono ritenuti superiori l’output diventa "
     "incontestabile, mentre dove conta il giudizio esperto lo stesso sistema viene percepito "
     "come un attacco all’identità professionale.")]),
  ("h3", "Profondità, pervasività, stabilità"),
  ("p", "La cultura è profonda, pervasiva e stabile, e proprio per questo dà significato ed è "
        "difesa. Non cambia perché si proclamano nuovi valori, ma quando si modificano strutture, "
        "incentivi, relazioni ed esperienze; se le nuove pratiche funzionano abbastanza a lungo "
        "diventano credibili e infine ovvie."),
  ("h3", "Readiness di un gruppo, non di un’organizzazione"),
  ("p", "Le sottoculture professionali, generazionali e geografiche leggono lo stesso progetto in "
        "modo diverso. Un sistema accettato dal management può essere rifiutato dai "
        "professionisti, e un sistema utile agli esperti può sovraccaricare i novizi. Perché la "
        "valutazione sia utile va riferita a un gruppo, a un uso e a condizioni precise."),
  ("note", "Cultura e clima non coincidono. Il clima riguarda percezioni condivise di pratiche e "
           "priorità attuali e cambia più rapidamente, mentre gli assunti richiedono metodi "
           "qualitativi, osservazione e storia organizzativa."),
 ]),

dict(n="04", title="Diagnosi",
     sub="Un intervento fallisce quando un problema vago diventa troppo presto una soluzione.",
     blocks=[
  ("steps", [
    ("01", "Costrutto", "Fiducia, readiness, sicurezza psicologica"),
    ("02", "Dimensioni", "Scomposizione teorica del concetto"),
    ("03", "Indicatori", "Ciò che è osservabile e rilevabile"),
    ("04", "Domande", "Item e guide, con un perché ciascuna"),
    ("05", "Dati", "Fonti triangolate fra log, voci e osservazione"),
    ("06", "Interpretazione", "Ipotesi alternative, non conferme"),
    ("07", "Restituzione", "Già parte dell’intervento, apre dialogo o difesa")]),
  ("h3", "«Accettazione» non è un costrutto unico"),
  ("p", "Uso obbligato, uso effettivo, utilità percepita, fiducia e disponibilità a dipendere dal "
        "sistema sono costrutti diversi. Una persona può usarlo perché deve e non fidarsi; "
        "considerarlo utile e ingiusto; fidarsi nei compiti standard e rifiutarlo nelle decisioni "
        "di carriera. Un alto tasso di utilizzo, quando l’uso è obbligatorio, non dimostra "
        "accettazione."),
  ("h3", "La divergenza fra le fonti è un dato"),
  ("p", "Il management legge alta adozione nei log; gli operatori descrivono uso rituale e scarsa "
        "fiducia. La triangolazione serve a spiegare perché le fonti divergono, non a farle "
        "coincidere. Una media di tre può derivare da risposte tutte moderate oppure da metà "
        "entusiasti e metà ostili, con implicazioni opposte."),
  ("table", dict(head=["Item difettoso", "Difetto", "Riformulazione"], rows=[
     ["«Il mio mentor è disponibile e competente»", "Domanda doppia",
      "Due item separati, uno per costrutto"],
     ["«Riceve spesso feedback utile?»", "Frequenza vaga",
      "«Nelle ultime quattro settimane, quante volte…»"],
     ["«Come ha superato la sua resistenza?»", "Presupposizione",
      "«Quali effetti ha avuto sul suo modo di lavorare?»"],
     ["«Comprendo l’AI»", "Costrutto generico",
      "«So per quali decisioni il sistema è autorizzato a raccomandare»"]])),
  ("note", "Anonimato e riservatezza non sono sinonimi. In un reparto piccolo il ruolo, "
           "l’anzianità e l’unità insieme identificano una persona. La minimizzazione dei dati è "
           "una scelta metodologica prima che formale."),
 ]),

dict(n="05", title="Sviluppo delle persone",
     sub="Erogare un corso, assegnare un mentor o dare un feedback non è ancora sviluppo.",
     blocks=[
  ("cards", [
    ("Formazione", "Analisi dei bisogni prima del corso",
     "Se una persona non verifica l’output perché rallentare viene punito, il problema è negli "
     "incentivi. Se il sistema è inaffidabile, il problema sta nel sistema e non nella "
     "preparazione delle persone. <span class='mchips'>Analisi organizzativa · Analisi del "
     "compito (KSA) · Analisi della persona</span> Un obiettivo formativo osservabile chiede di "
     "riconoscere quattro categorie di rischio in un output e di decidere quando fare escalation."),
    ("Mentoring", "Il matching non produce la relazione",
     "Le funzioni di carriera danno accesso e competenza; quelle psicosociali danno identità e "
     "fiducia. Un algoritmo che accoppia due persone non «fa mentoring». <span class='mchips'>"
     "Sponsorship, coaching, esposizione · Accettazione, role modeling · Avvio, coltivazione, "
     "separazione, ridefinizione</span> Usare conversazioni private per valutare la relazione "
     "distrugge la fiducia che il programma voleva creare."),
    ("Leadership", "Leader development e leadership development",
     "Il <i>leader development</i> costruisce capacità individuali; il <i>leadership "
     "development</i> costruisce capacità collettiva di direzione, allineamento e impegno. "
     "Formare molti individui non produce la seconda. <span class='mchips'>Identità e "
     "autoregolazione · Deliberate practice · Assessment, challenge, support</span> Un’app che "
     "dice al manager chi coinvolgere sviluppa un leader; se solo lui vede i dati, il potere "
     "resta centralizzato.")]),
  ("h3", "Il feedback non migliora sempre la performance"),
  ("p", "Dipende da dove dirige l’attenzione. Se la sposta dal compito al sé percepito come "
        "minacciato, può peggiorarla. Qualità, tempismo, credibilità della fonte e capacità di "
        "autoregolazione contano più della frequenza. Un AI coach che aumenta la frequenza non "
        "aumenta automaticamente l’apprendimento."),
  ("h3", "Output non è outcome"),
  ("p", "«Cento persone formate» è un output. Reazione, apprendimento, comportamento e risultati "
        "non sono una catena automatica. Un corso apprezzato può non insegnare nulla, e una "
        "competenza acquisita non si trasferisce se manager, strumenti e incentivi non la "
        "sostengono."),
 ]),

dict(n="06", title="Collega o gabbia",
     sub="La stessa tecnologia diventa un collega algoritmico o una gabbia algoritmica.",
     blocks=[
  ("cards", [
    ("Algorithmic colleague", "Il giudizio resta alla persona",
     "In un contesto che valorizza giudizio e autonomia il sistema supporta senza sostituire la "
     "responsabilità. Le divergenze vengono discusse come fonte di apprendimento, l’override "
     "resta praticabile e il sapere tacito viene coltivato."),
    ("Algorithmic cage", "L’autonomia si erode senza decisioni",
     "In un contesto gerarchico irrigidisce i processi e riduce l’autonomia. L’override "
     "formalmente esiste, ma ogni deviazione richiede una giustificazione, e l’<i>agency</i> si "
     "erode gradualmente senza che nessuna decisione l’abbia mai revocata.")]),
  ("h3", "Cinque temi della ricerca empirica"),
  ("olist", [
    "La collaborazione umano-AI produce benefici quando ci sono <i>task-technology fit</i>, "
    "fiducia e capacità d’uso.",
    "L’algoritmo viene percepito come coerente e disinteressato oppure come decontestualizzato.",
    "Speranza e timore convivono nella stessa persona, e agency e supporto del leader attenuano "
    "il timore.",
    "L’<i>algorithmic management</i> assegna, monitora e sanziona, e la questione aperta è la "
    "contestabilità.",
    "Alcune tecnologie sostituiscono compiti, altre ne creano di nuovi."]),
  ("note", "L’esperienza di dominio ha effetti non lineari. Gli esperti possono rifiutare il "
           "consiglio algoritmico, i principianti non saperlo valutare, e chi ha esperienza "
           "intermedia trarne il massimo vantaggio."),
  ("h3", "Quattro dimensioni di analisi"),
  ("deflist", [
    ("Contesto", "Da AI che abilita decisioni a AI che esercita un controllo coercitivo."),
    ("Agency", "Chi mantiene iniziativa e chi la vede limitata."),
    ("Interazione", "Augmentation ed engagement oppure automazione e accettazione."),
    ("Outcomes", "Performance del compito e impatto sulle persone.")]),
  ("p", "Il manager è <i>first party</i> che usa il sistema; l’operatore è anche <i>second "
        "party</i>, perché la stessa dashboard lo misura; il cliente è <i>third party</i> e "
        "subisce la decisione. Vendor e annotatori di dati restano attori invisibili."),
  ("h3", "Come evolve nel tempo"),
  ("deflist", [
    ("Istituzionalizzazione", "L’uso diventa routine e norma."),
    ("Ibridazione", "Configurazioni umano-algoritmo."),
    ("Sistematizzazione", "Più strumenti si collegano."),
    ("Integrazione sociale", "Effetti su professioni e regole.")]),
 ]),

dict(n="07", title="Allocazione dei compiti",
     sub="«Umano + AI» sullo stesso compito non è sempre la configurazione migliore.",
     blocks=[
  ("p", "La complementarità <i>within-task</i> giustifica l’augmentation, perché sullo stesso "
        "compito umano e sistema insieme fanno meglio di ciascuno dei due. La complementarità "
        "<i>between-task</i> giustifica invece l’allocazione dei compiti alla configurazione più "
        "adatta a ciascuno di essi. In uno studio su un compito di classificazione di immagini le "
        "due logiche portano a risultati sensibilmente diversi."),
  ("stats", [("Solo umano", 68), ("Solo AI", 77), ("Umano con consiglio AI", 80),
             ("Allocazione ottimizzata", 88)]),
  ("caption", "Accuratezza su un compito di classificazione di immagini. I valori illustrano una "
              "logica di progettazione, non un benchmark trasferibile ad altri processi."),
  ("cards", [
    ("Casi facili / alta confidenza", "Automazione selettiva",
     "Con audit sugli errori e campionamento. Ma se i casi semplici scompaiono, i nuovi assunti "
     "non costruiscono competenza di base."),
    ("Casi intermedi", "Augmentation",
     "Il sistema ordina le evidenze, la persona integra il contesto. Serve un override reale, non "
     "formale, e spiegazioni utilizzabili."),
    ("Casi difficili / bassa confidenza", "Team umani",
     "Multidisciplinari. Concentrare le persone solo sui casi duri alza il carico cognitivo e "
     "toglie occasioni di recupero e apprendimento.")]),
  ("p", "Anche un sistema mediamente meno accurato di una persona crea valore quando è "
        "complementare o libera tempo per attività a maggiore valore. La performance immediata "
        "non chiude comunque la decisione, perché responsabilità, costi di switching, "
        "meta-conoscenza, equità e conservazione del sapere tacito pesano nel medio periodo."),
 ]),

dict(n="08", title="Progettare un sistema di AI",
     sub="Nove domande in ordine, dal contesto del lavoro ai rischi del sistema.",
     blocks=[
  ("steps", [
    ("01", "Contesto", "Organizzazione, utenti, processo, stakeholder, sottoculture coinvolte."),
    ("02", "Bisogno", "Specifico e sostenuto da diagnosi, non dedotto da una tecnologia disponibile."),
    ("03", "Input", "Quali dati e conoscenze, con quale legittimità e quale minimizzazione."),
    ("04", "Processo", "Come il sistema trasforma l’input e dove esattamente intervengono le persone."),
    ("05", "Output", "Evidenze, alternative e livello di confidenza, invece di un semaforo che "
                     "nasconde l’incertezza."),
    ("06", "Primo passo", "Prototipo con dati sintetici e co-design, non ingestione di "
                          "conversazioni reali."),
    ("07", "Valore atteso", "Su qualità o risorse, dichiarato prima e verificabile su baseline."),
    ("08", "Parti umane", "Scelta degli obiettivi, interpretazione, relazione, decisione e "
                          "responsabilità."),
    ("09", "Rischi", "Privacy, bias, deriva verso la valutazione, dipendenza, misuse.")]),
  ("table", dict(head=["Rischio", "Risposta insufficiente", "Mitigazione nel design"], rows=[
    ["Privacy", "Consenso generico",
     "Necessità, minimizzazione, accessi separati, retention, nessun training sui dati personali"],
    ["Bias", "Dichiarare <i>fairness</i>",
     "Gruppi definiti, metriche di errore rilevanti, audit, procedure di riparazione"],
    ["Resistenza", "Piano di comunicazione",
     "Esame delle perdite reali, ascolto della conoscenza critica, contestabilità"],
    ["Misuse", "Una policy che nessuno legge",
     "Limiti tecnici agli usi, responsabilità assegnate, condizione di stop definita prima"]])),
 ]),

dict(n="09", title="Valutare per governare",
     sub="Quattro famiglie di KPI.",
     blocks=[
  ("p", "Un piano di valutazione utile tiene insieme quattro tipi di indicatore. Gli output dicono "
        "che il sistema è in funzione, gli indicatori di meccanismo spiegano come viene usato, gli "
        "outcome misurano gli effetti sul lavoro e quelli di rischio rilevano i danni che le prime "
        "tre famiglie non registrano."),
  ("cards", [
    ("Output", "Il sistema è in funzione",
     "Persone formate, messaggi generati, pratiche processate. Sono necessari ma non sufficienti."),
    ("Meccanismo", "Come viene usato",
     "Carico cognitivo, comprensione, uso effettivo del consiglio, override e loro esito."),
    ("Outcome", "Effetti sul lavoro",
     "Comportamenti sul lavoro, qualità, tempi, esiti di sviluppo, permanenza."),
    ("Rischio", "Danni che gli altri non registrano",
     "Autocensura, omologazione del linguaggio, dipendenza, disparità fra gruppi, incidenti.")]),
  ("h3", "Un trade-off non è un fallimento"),
  ("p", "Se la performance sale mentre la sicurezza psicologica scende, il risultato è ambivalente "
        "e va deciso in base a grandezza, distribuzione e durata degli effetti. Un indice "
        "composito unico nasconderebbe la tensione."),
  ("h3", "Una misura è valida per un uso"),
  ("p", "Un questionario utile a facilitare dialogo può essere inadatto a classificare persone. Se "
        "il sistema produce la metrica con cui viene valutato, l’indicatore non è indipendente."),
  ("note", "<b>Nota metodologica.</b> Questo whitepaper rielabora in forma originale concetti "
           "della letteratura su sviluppo organizzativo, cultura organizzativa, diagnosi e "
           "valutazione, sviluppo delle persone e AI nelle organizzazioni (fra gli altri Schein "
           "sui livelli della cultura e sul feedback; Kram sul mentoring; Kirkpatrick e Quaglino "
           "sulla valutazione; Kluger e DeNisi sul feedback; Day sul leader e leadership "
           "development; Bankins e colleghi, Hillebrand, Raisch e Schad, Fügener, Walzner e Gupta "
           "sull’AI nelle organizzazioni). Nessun contenuto didattico è riprodotto. I dati citati "
           "illustrano una logica di progettazione e non costituiscono benchmark trasferibili."),
 ]),
]


def render(sections):
    out = []
    for s in sections:
        out.append(f'<section class="msec rv" id="s{s["n"]}">')
        out.append(f'  <div class="mhead"><span class="n">{s["n"]}</span>'
                   f'<h2>{s["title"]}</h2><p class="msub">{s["sub"]}</p></div>')
        for kind, payload in s["blocks"]:
            if kind == "p":
                out.append(f"  <p>{payload}</p>")
            elif kind == "h3":
                out.append(f"  <h3>{payload}</h3>")
            elif kind == "note":
                out.append(f'  <aside class="mnote">{payload}</aside>')
            elif kind == "caption":
                out.append(f'  <p class="mcap">{payload}</p>')
            elif kind == "cards":
                cards = "".join(
                    f'<article class="mcard"><div class="k">{k}</div><h4>{t}</h4><p>{b}</p></article>'
                    for k, t, b in payload)
                out.append(f'  <div class="mcards">{cards}</div>')
            elif kind == "steps":
                rows = "".join(
                    f'<div class="mstep"><span class="n">{n}</span><span class="t">{t}</span>'
                    f'<span class="s">{sub}</span></div>' for n, t, sub in payload)
                out.append(f'  <div class="msteps">{rows}</div>')
            elif kind == "olist":
                items = "".join(f"<li>{i}</li>" for i in payload)
                out.append(f'  <ol class="mlist">{items}</ol>')
            elif kind == "deflist":
                items = "".join(f"<div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in payload)
                out.append(f'  <dl class="mdef">{items}</dl>')
            elif kind == "stats":
                top = max(v for _, v in payload)
                bars = "".join(
                    f'<div class="mstat"><span class="v">{v}%</span>'
                    f'<span class="bar"><i style="width:{v*100//top}%"></i></span>'
                    f'<span class="l">{l}</span></div>' for l, v in payload)
                out.append(f'  <div class="mstats">{bars}</div>')
            elif kind == "table":
                head = "".join(f"<th>{h}</th>" for h in payload["head"])
                rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                               for r in payload["rows"])
                out.append(f'  <div class="mtable"><table><thead><tr>{head}</tr></thead>'
                           f"<tbody>{rows}</tbody></table></div>")
        out.append("</section>")
    return "\n".join(out)


def toc(sections):
    return "".join(f'<a href="#s{s["n"]}"><span>{s["n"]}</span>{s["title"]}</a>' for s in sections)
