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


LABELS_EN = dict(
    kicker="Method",
    title="AI &amp; Organizational Development",
    sub="Designing the technology inside the work.",
    lede="Introducing an AI system changes how people work, decide, learn and are assessed. "
         "Designing it is therefore an organisational problem before it is a technical one.",
    meta="Whitepaper · 2026 · Alessandro Saccoia",
    strap="Culture, diagnosis, developing people and critical design of intelligent systems.",
    toc="The nine sections",
)

SECTIONS_EN = [
dict(n="01", title="Executive summary",
     sub="An AI project is judged on the context it enters, the task it takes on, the effects it "
         "produces and who bears them.",
     blocks=[
  ("p", "An intelligent system enters a network of interdependent activities, roles, identities "
        "and meanings. Its organisational value depends on how it is embedded in the processes "
        "that hold that network together."),
  ("cards", [
    ("01 / Diagnose", "Define the problem before the tool",
     "A statement such as «people resist AI» is not a diagnosis. A diagnosis requires an explicit "
     "chain, from the construct to the dimensions, the indicators, the data, their interpretation "
     "and the way findings are given back."),
    ("02 / Configure", "Automation and augmentation are configurations",
     "They are not properties of the software but ways of organising work. The same system can "
     "widen a manager's room for judgement and narrow that of a team member."),
    ("03 / Develop", "The tool is one part of the intervention",
     "The intervention includes co-design, training, new practices, governance and evaluation. "
     "Without those components the organisation gets an installed piece of software and no change "
     "in how the work is done.")]),
  ("h3", "The argument"),
  ("p", "AI inside a company is a matter of organisational development before it is a matter of "
        "models. Accuracy is necessary but not sufficient, because the meaning of a system depends "
        "on how it redefines purposes, roles, coordination, rules, assessment and identity."),
  ("h3", "How to read this document"),
  ("p", "The nine pages follow four moves. You read the organisation and its culture, you diagnose "
        "with method, you develop the people, and you design and evaluate an AI system."),
 ]),

dict(n="02", title="Where the technology enters",
     sub="Six organisational processes to examine before designing a system.",
     blocks=[
  ("p", "An organisation is both formal structure and <i>organizing</i>, meaning the informal "
        "practices and tacit knowledge without which the real work does not function. A system "
        "built on the formal representation of the work always meets that margin."),
  ("cards", [
    ("01 / Purpose", "Who defined the objective?",
     "An algorithm optimised on a single indicator ends up sacrificing quality, learning or "
     "wellbeing. It is worth asking which dimensions were left out of the objective function."),
    ("02 / Differentiation", "Different languages",
     "Data science, HR and the front line mean different things by performance, error and "
     "fairness. AI puts specialisms in contact without a shared language."),
    ("03 / Integration", "Coordination or a new divide",
     "The system can coordinate information, or open a new divide between those who understand "
     "the model and those who merely follow its output."),
    ("04 / Formalisation", "What is measurable and what counts",
     "The algorithm translates criteria of judgement into computable rules. The risk is that what "
     "the system measures is taken for what has value."),
    ("05 / Assessment", "Measurement changes behaviour",
     "More frequency and precision can support learning, or produce surveillance, anxiety and "
     "opportunistic adaptation to the indicators."),
    ("06 / Identification", "A threat to professional identity",
     "When AI takes on a task that is central to a profession, the resistance is about the "
     "identity of whoever performed it rather than about ease of use.")]),
  ("note", "Resistance often signals a <b>real loss</b> of autonomy, competence, belonging or "
           "power, and not unfamiliarity with the technology."),
 ]),

dict(n="03", title="Organisational culture",
     sub="Beneath the visible artefacts sit espoused values and assumptions taken for granted.",
     blocks=[
  ("cards", [
    ("Level 1 — visible", "Artefacts",
     "Spaces, technologies, dashboards, meetings, language, procedures. They show <i>what</i> "
     "happens, not <i>why</i>. A screen with real-time performance can express transparency and "
     "learning or control and competition, and the artefact alone does not say which."),
    ("Level 2 — espoused", "Stated values",
     "Innovation, autonomy, quality, inclusion. The distance between a stated value and the "
     "practice is diagnostic data. If whoever checks an output comes out less productive in the "
     "measurement systems, the value in practice is speed."),
    ("Level 3 — taken for granted", "Basic assumptions",
     "«Data is more reliable than people». «Only experience really understands this work». "
     "«An error is a fault to hide». They are written in no policy, yet they determine the "
     "reaction to AI. Where data is held to be superior the output becomes uncontestable, while "
     "where expert judgement counts the same system is felt as an attack on professional "
     "identity.")]),
  ("h3", "Depth, pervasiveness, stability"),
  ("p", "Culture is deep, pervasive and stable, and for that reason it gives meaning and is "
        "defended. It does not change because new values are proclaimed, but when structures, "
        "incentives, relationships and experiences change; if the new practices work for long "
        "enough they become credible and finally obvious."),
  ("h3", "Readiness belongs to a group, not to an organisation"),
  ("p", "Professional, generational and geographical subcultures read the same project "
        "differently. A system accepted by management can be refused by the professionals, and a "
        "system useful to experts can overload novices. For an assessment to be useful it has to "
        "be referred to a group, a use and precise conditions."),
  ("note", "Culture and climate are not the same. Climate concerns shared perceptions of current "
           "practices and priorities and changes faster, while assumptions require qualitative "
           "methods, observation and organisational history."),
 ]),

dict(n="04", title="Diagnosis",
     sub="An intervention fails when a vague problem becomes a solution too early.",
     blocks=[
  ("steps", [
    ("01", "Construct", "Trust, readiness, psychological safety"),
    ("02", "Dimensions", "Theoretical decomposition of the concept"),
    ("03", "Indicators", "What is observable and can be recorded"),
    ("04", "Questions", "Items and guides, each with a reason"),
    ("05", "Data", "Sources triangulated across logs, voices and observation"),
    ("06", "Interpretation", "Alternative hypotheses, not confirmations"),
    ("07", "Giving back", "Already part of the intervention: it opens dialogue or defence")]),
  ("h3", "«Acceptance» is not a single construct"),
  ("p", "Mandated use, actual use, perceived usefulness, trust and willingness to depend on the "
        "system are different constructs. A person can use it because they must and not trust it; "
        "find it useful and unfair; trust it on standard tasks and refuse it on career decisions. "
        "A high usage rate, where use is mandatory, does not demonstrate acceptance."),
  ("h3", "Divergence between sources is data"),
  ("p", "Management reads high adoption in the logs; operators describe ritual use and little "
        "trust. Triangulation serves to explain why the sources diverge, not to make them agree. "
        "An average of three can come from uniformly moderate answers or from half enthusiasts "
        "and half opponents, with opposite implications."),
  ("table", dict(head=["Faulty item", "Fault", "Rewrite"], rows=[
     ["«My mentor is available and competent»", "Double-barrelled",
      "Two separate items, one per construct"],
     ["«Do you often receive useful feedback?»", "Vague frequency",
      "«In the last four weeks, how many times…»"],
     ["«How did you overcome your resistance?»", "Presupposition",
      "«What effects has it had on the way you work?»"],
     ["«I understand AI»", "Generic construct",
      "«I know which decisions the system is allowed to make recommendations on»"]])),
  ("note", "Anonymity and confidentiality are not synonyms. In a small department role, seniority "
           "and unit together identify a person. Data minimisation is a methodological choice "
           "before it is a formal one."),
 ]),

dict(n="05", title="Developing people",
     sub="Running a course, assigning a mentor or giving feedback is not yet development.",
     blocks=[
  ("cards", [
    ("Training", "Needs analysis before the course",
     "If a person does not check the output because slowing down is punished, the problem is in "
     "the incentives. If the system is unreliable, the problem is the system and not how prepared "
     "the people are. <span class='mchips'>Organisational analysis · Task analysis (KSA) · Person "
     "analysis</span> An observable training objective asks someone to recognise four categories "
     "of risk in an output and to decide when to escalate."),
    ("Mentoring", "Matching does not produce the relationship",
     "Career functions give access and competence; psychosocial functions give identity and "
     "confidence. An algorithm that pairs two people does not «do mentoring». <span "
     "class='mchips'>Sponsorship, coaching, exposure · Acceptance, role modelling · Initiation, "
     "cultivation, separation, redefinition</span> Using private conversations to assess the "
     "relationship destroys the trust the programme set out to create."),
    ("Leadership", "Leader development and leadership development",
     "<i>Leader development</i> builds individual capability; <i>leadership development</i> builds "
     "the collective capacity for direction, alignment and commitment. Training many individuals "
     "does not produce the second. <span class='mchips'>Identity and self-regulation · Deliberate "
     "practice · Assessment, challenge, support</span> An app that tells the manager who to "
     "involve develops a leader; if only they see the data, power stays centralised.")]),
  ("h3", "Feedback does not always improve performance"),
  ("p", "It depends on where it directs attention. If it moves attention from the task to a self "
        "that feels threatened, it can make performance worse. Quality, timing, source "
        "credibility and the capacity for self-regulation count for more than frequency. An AI "
        "coach that increases frequency does not automatically increase learning."),
  ("h3", "Output is not outcome"),
  ("p", "«A hundred people trained» is an output. Reaction, learning, behaviour and results are "
        "not an automatic chain. A course people enjoy may teach nothing, and a competence "
        "acquired does not transfer if managers, tools and incentives do not support it."),
 ]),

dict(n="06", title="Colleague or cage",
     sub="The same technology becomes an algorithmic colleague or an algorithmic cage.",
     blocks=[
  ("cards", [
    ("Algorithmic colleague", "Judgement stays with the person",
     "In a context that values judgement and autonomy the system supports without replacing "
     "responsibility. Divergences are discussed as a source of learning, the override remains "
     "practicable and tacit knowledge is cultivated."),
    ("Algorithmic cage", "Autonomy erodes without a decision",
     "In a hierarchical context it stiffens the processes and reduces autonomy. The override "
     "formally exists, but every deviation requires a justification, and <i>agency</i> erodes "
     "gradually without any decision ever having revoked it.")]),
  ("h3", "Five themes from the empirical research"),
  ("olist", [
    "Human-AI collaboration produces benefits where there is <i>task-technology fit</i>, trust and "
    "the capability to use it.",
    "The algorithm is perceived as consistent and disinterested, or as decontextualised.",
    "Hope and fear coexist in the same person, and agency and the leader's support soften the fear.",
    "<i>Algorithmic management</i> assigns, monitors and sanctions, and the open question is "
    "contestability.",
    "Some technologies replace tasks, others create new ones."]),
  ("note", "Domain experience has non-linear effects. Experts may refuse the algorithmic advice, "
           "beginners may not be able to judge it, and those with intermediate experience may "
           "gain the most."),
  ("h3", "Four dimensions of analysis"),
  ("deflist", [
    ("Context", "From AI that enables decisions to AI that exercises coercive control."),
    ("Agency", "Who keeps the initiative and who sees it limited."),
    ("Interaction", "Augmentation and engagement, or automation and acceptance."),
    ("Outcomes", "Task performance and impact on people.")]),
  ("p", "The manager is the <i>first party</i> using the system; the operator is also a <i>second "
        "party</i>, because the same dashboard measures them; the customer is a <i>third party</i> "
        "and bears the decision. Vendors and data annotators remain invisible actors."),
  ("h3", "How it evolves over time"),
  ("deflist", [
    ("Institutionalisation", "Use becomes routine and norm."),
    ("Hybridisation", "Human-algorithm configurations."),
    ("Systematisation", "More tools connect to one another."),
    ("Social integration", "Effects on professions and rules.")]),
 ]),

dict(n="07", title="Allocating the tasks",
     sub="«Human + AI» on the same task is not always the best configuration.",
     blocks=[
  ("p", "<i>Within-task</i> complementarity justifies augmentation, because on the same task human "
        "and system together do better than either alone. <i>Between-task</i> complementarity "
        "instead justifies allocating tasks to whichever configuration suits each of them. In a "
        "study on an image classification task the two logics lead to appreciably different "
        "results."),
  ("stats", [("Human only", 68), ("AI only", 77), ("Human with AI advice", 80),
             ("Optimised allocation", 88)]),
  ("caption", "Accuracy on an image classification task. The figures illustrate a design logic, "
              "not a benchmark transferable to other processes."),
  ("cards", [
    ("Easy cases / high confidence", "Selective automation",
     "With error audits and sampling. But if the simple cases disappear, new hires do not build "
     "basic competence."),
    ("Intermediate cases", "Augmentation",
     "The system orders the evidence, the person adds the context. It needs a real override, not "
     "a formal one, and explanations that can be used."),
    ("Hard cases / low confidence", "Human teams",
     "Multidisciplinary. Concentrating people only on the hard cases raises cognitive load and "
     "removes chances to recover and to learn.")]),
  ("p", "Even a system on average less accurate than a person creates value when it is "
        "complementary or frees time for higher-value activity. Immediate performance does not "
        "close the decision, because responsibility, switching costs, meta-knowledge, fairness and "
        "the preservation of tacit knowledge weigh in the medium term."),
 ]),

dict(n="08", title="Designing an AI system",
     sub="Nine questions in order, from the context of the work to the risks of the system.",
     blocks=[
  ("steps", [
    ("01", "Context", "Organisation, users, process, stakeholders, subcultures involved."),
    ("02", "Need", "Specific and supported by diagnosis, not deduced from an available technology."),
    ("03", "Input", "Which data and knowledge, with what legitimacy and what minimisation."),
    ("04", "Process", "How the system transforms the input and exactly where people intervene."),
    ("05", "Output", "Evidence, alternatives and a confidence level, instead of a traffic light "
                     "that hides the uncertainty."),
    ("06", "First step", "A prototype on synthetic data and co-design, not ingestion of real "
                         "conversations."),
    ("07", "Expected value", "On quality or resources, stated in advance and verifiable against a "
                             "baseline."),
    ("08", "Human parts", "Choice of objectives, interpretation, relationship, decision and "
                          "responsibility."),
    ("09", "Risks", "Privacy, bias, drift towards assessment, dependence, misuse.")]),
  ("table", dict(head=["Risk", "Insufficient response", "Mitigation in the design"], rows=[
    ["Privacy", "Generic consent",
     "Necessity, minimisation, separate access, retention, no training on personal data"],
    ["Bias", "Declaring <i>fairness</i>",
     "Defined groups, relevant error metrics, audits, redress procedures"],
    ["Resistance", "A communication plan",
     "Examining the real losses, listening to critical knowledge, contestability"],
    ["Misuse", "A policy nobody reads",
     "Technical limits on uses, assigned responsibilities, a stop condition defined in advance"]])),
 ]),

dict(n="09", title="Evaluating in order to govern",
     sub="Four families of KPI.",
     blocks=[
  ("p", "A useful evaluation plan holds four kinds of indicator together. Outputs say the system "
        "is running, mechanism indicators explain how it is used, outcomes measure the effects on "
        "the work, and risk indicators pick up the harms the first three families do not record."),
  ("cards", [
    ("Output", "The system is running",
     "People trained, messages generated, cases processed. Necessary but not sufficient."),
    ("Mechanism", "How it is used",
     "Cognitive load, comprehension, actual use of the advice, overrides and their outcome."),
    ("Outcome", "Effects on the work",
     "Behaviour at work, quality, timing, development outcomes, retention."),
    ("Risk", "Harms the others do not record",
     "Self-censorship, flattening of language, dependence, disparities between groups, incidents.")]),
  ("h3", "A trade-off is not a failure"),
  ("p", "If performance rises while psychological safety falls, the result is ambivalent and has "
        "to be decided on the size, distribution and duration of the effects. A single composite "
        "index would hide the tension."),
  ("h3", "A measure is valid for a use"),
  ("p", "A questionnaire useful for facilitating dialogue may be unfit for classifying people. If "
        "the system produces the metric by which it is judged, the indicator is not independent."),
  ("note", "<b>Methodological note.</b> This whitepaper reworks, in original form, concepts from "
           "the literature on organisational development, organisational culture, diagnosis and "
           "evaluation, developing people, and AI in organisations (among others Schein on the "
           "levels of culture and on feedback; Kram on mentoring; Kirkpatrick and Quaglino on "
           "evaluation; Kluger and DeNisi on feedback; Day on leader and leadership development; "
           "Bankins and colleagues, Hillebrand, Raisch and Schad, Fügener, Walzner and Gupta on AI "
           "in organisations). No teaching material is reproduced. The figures cited illustrate a "
           "design logic and are not transferable benchmarks."),
 ]),
]


# Sulla pagina il whitepaper è un'anteprima: le tabelle e gli elenchi di
# definizioni restano al PDF, che è il documento completo.
PREVIEW_SKIP = {"table", "deflist"}


def render(sections, preview=False, more=""):
    out = []
    for s in sections:
        out.append(f'<section class="msec rv" id="s{s["n"]}">')
        out.append(f'  <div class="mhead"><span class="n">{s["n"]}</span>'
                   f'<h2>{s["title"]}</h2><p class="msub">{s["sub"]}</p></div>')
        skipped = 0
        for kind, payload in s["blocks"]:
            if preview and kind in PREVIEW_SKIP:
                skipped += 1
                continue
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
        if preview and skipped and more:
            out.append(f'  <p class="mmore">{more}</p>')
        out.append("</section>")
    return "\n".join(out)


def toc(sections):
    return "".join(f'<a href="#s{s["n"]}"><span>{s["n"]}</span>{s["title"]}</a>' for s in sections)


# ---------------------------------------------------------------- il download
# La pagina è un'anteprima; il PDF completo arriva per mail, quindi il modulo
# chiede i contatti. Le stringhe stanno qui accanto al testo che descrivono.
PDF = "/assets/doc/iside-systems-whitepaper-ai-organizational-development.pdf"

GATE = {
"it": dict(
  lbl="Whitepaper completo",
  h="Scaricalo per intero, in PDF.",
  card="Otto pagine impaginate, con le tabelle e gli schemi che qui restano fuori.",
  open="Scarica il PDF",
  close="Chiudi",
  p="Lascia un contatto e te lo mando via mail. Il download parte subito.",
  meta="PDF · 8 pagine · italiano",
  name="Nome", surname="Cognome", email="Email",
  msg="Vuoi aggiungere qualcosa?",
  msg_ph="Facoltativo — su cosa stai lavorando, cosa vorresti approfondire.",
  consent="Voglio ricevere anche le comunicazioni di Iside Systems (poche, e "
          "sempre su questi temi). Puoi disiscriverti quando vuoi.",
  cta="Mandami il whitepaper",
  sending="Invio…",
  done="Fatto. Controlla la posta: il PDF è in arrivo.",
  fail="Non è partita. Scrivimi a alessandro@iside.systems e te lo mando a mano.",
  privacy="I dati servono a mandarti il PDF e a risponderti. Vedi la",
  privacy_link="privacy policy",
  more="Tabella completa nel whitepaper.",
),
"en": dict(
  lbl="Full whitepaper",
  h="Get the whole thing, as a PDF.",
  card="Eight typeset pages, with the tables and schemes left out here.",
  open="Download the PDF",
  close="Close",
  p="Leave a contact and I will send it over. The download starts right away.",
  meta="PDF · 8 pages · Italian",
  name="First name", surname="Last name", email="Email",
  msg="Anything to add?",
  msg_ph="Optional — what you are working on, what you would like to go deeper on.",
  consent="I would also like to receive news from Iside Systems (rarely, and "
          "always on these subjects). You can unsubscribe at any time.",
  cta="Send me the whitepaper",
  sending="Sending…",
  done="Done. Check your inbox: the PDF is on its way.",
  fail="It did not go through. Write to alessandro@iside.systems and I will send it by hand.",
  privacy="The data is used to send you the PDF and to reply. See the",
  privacy_link="privacy policy",
  more="Full table in the whitepaper.",
),
}
