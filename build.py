#!/usr/bin/env python3
"""
Builds the Iside Systems site in two languages.

  /            Italian  (index.html, progetti.html, chi-sono.html)
  /en/         English  (index.html, projects.html, about.html)

Copy lives in the L_IT / L_EN dictionaries below — edit there, then re-run:
    python3 build.py
"""
import os
import blog as B, metodo as M, html, datetime, json

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- projects
# Shared structure; only the prose differs per language.
# `url` is optional: when present the tile links out and is marked with an arrow.
PROJECTS = [
    dict(seed=3,  cat="ai product",           year="2024 →",
         featured=True,
         it=("Thembi", "Co-fondatore · prodotto, backend, sistemi AI",
             "Piattaforma di policy intelligence europea. Knowledge Representation, Information "
             "Extraction, Ingestione e retrieval su corpora legislativi che cambiano ogni "
             "settimana, ricerca semantica e stesura assistita dei documenti.",
             ["Retrieval", "Ricerca semantica", "Prodotto"]),
         en=("Thembi", "Co-founder · product, backend, AI systems",
             "EU policy intelligence platform. Knowledge representation, information extraction, "
             "ingestion and retrieval over legislative corpora that change weekly, semantic "
             "search, and assisted drafting of documents.",
             ["Retrieval", "Semantic search", "Product"])),
    dict(seed=6,  cat="analytics ai",         year="2026 →",
         featured=True,
         it=("Mentor Ripetizioni", "Modello di crescita e infrastruttura di marketing",
             "Ripetizioni online. Framework di misurazione omnichannel su Google Ads, Meta, "
             "LinkedIn Ads e TikTok, tool proprietario per costruire i piani editoriali sugli stadi "
             "del funnel di vendita, e un tutor AI che copre le ore in cui i tutor umani non ci sono.",
             ["Misurazione omnichannel", "Piani editoriali", "Tutor AI"]),
         en=("Mentor Ripetizioni", "Growth model and marketing infrastructure",
             "Italian online tutoring. Omnichannel measurement framework across Google Ads, Meta, "
             "LinkedIn Ads and TikTok, proprietary tooling that builds editorial plans against the "
             "stages of the sales funnel, and an AI tutor covering the hours human tutors cannot.",
             ["Omnichannel measurement", "Editorial planning", "AI tutor"])),
    dict(seed=9,  cat="research ai strategy", year="2023 — 24",
         it=("IULM AI Lab", "Chief technology officer",
             "Direzione tecnica di un laboratorio universitario di AI: progetti di ricerca "
             "applicata con partner industriali, prototipi, e il programma didattico che vi ruotava "
             "attorno.",
             ["Ricerca applicata", "Prototipi"]),
         en=("IULM AI Lab", "Chief technology officer",
             "Technical direction of a university AI lab: applied research projects with industry "
             "partners, prototype development, and the teaching programme that ran alongside them.",
             ["Applied research", "Prototypes"])),
    dict(seed=5,  cat="analytics strategy",   year="2022 — 23",
         it=("Nielsen", "Senior manager, marketing effectiveness",
             "Efficacia del marketing e misurazione dei media per grandi investitori pubblicitari. "
             "Da qui viene la disciplina di misurazione e attribuzione cross-canale che "
             "regge oggi il lavoro di operations.",
             ["Misurazione media", "Attribuzione"]),
         en=("Nielsen", "Senior manager, marketing effectiveness",
             "Marketing effectiveness and media measurement for large advertisers — where the "
             "cross-channel measurement and attribution discipline behind the operations work was "
             "learned.",
             ["Media measurement", "Attribution"])),
    dict(seed=8,  cat="strategy product",     year="2021 — 22",
         it=("Vodafone Business", "Product manager · Vodafone Analytics",
             "Vodafone Analytics: analisi territoriale e martech costruiti sui big data della rete "
             "telco. Requisiti, roadmap e delivery fra team tecnici e commerciali, in un contesto "
             "dove la governance del dato non è facoltativa.",
             ["Big data telco", "Geoanalytics", "Martech", "Prodotto"]),
         en=("Vodafone Business", "Product manager · Vodafone Analytics",
             "Vodafone Analytics: territorial analysis and martech built on telco network big data. "
             "Requirements, roadmap and delivery across engineering and commercial teams, in an "
             "environment where data governance is not optional.",
             ["Telco big data", "Geoanalytics", "Martech", "Product"])),
    dict(seed=4,  cat="ai analytics",         year="2018 — 20",
         it=("Beintoo", "Head of data science",
             "Guida della data science nell'ad-tech: dataset comportamentali e di localizzazione su "
             "larga scala, modellazione delle audience e le pipeline necessarie a tenerli in piedi "
             "a volume.",
             ["Data mining", "Scala"]),
         en=("Beintoo", "Head of data science",
             "Data science leadership in ad-tech: large-scale behavioural and location datasets, "
             "audience modelling, and the pipelines to keep it all running at volume.",
             ["Data mining", "Scale"])),
    dict(seed=7,  cat="research ai",          year="2012 — 16",
         it=("Dinahmoe", "Direttore tecnico · Stoccolma",
             "Audio interattivo e sistemi in tempo reale per campagne e prodotti internazionali, "
             "con lavori realizzati per HBO, Nike e Google. Direzione ingegneristica su progetti in "
             "cui la tecnologia era l'esperienza.",
             ["Audio real-time", "HBO · Nike · Google"]),
         en=("Dinahmoe", "Technical director · Stockholm",
             "Interactive audio and real-time systems for international campaigns and products, "
             "with work delivered for HBO, Nike and Google. Engineering leadership on projects "
             "where the technology was the experience.",
             ["Real-time audio", "HBO · Nike · Google"])),
    dict(seed=10, cat="research product",     year="2017 — 18",
         it=("Mogees", "Project manager, data science · Londra",
             "Lavoro su sensing gestuale e microfoni a contatto trasformato in un prodotto di "
             "consumo: elaborazione del segnale e machine learning applicati a un'interfaccia fisica.",
             ["Machine listening", "Signal processing"]),
         en=("Mogees", "Project manager, data science · London",
             "Work on gesture and contact-microphone sensing turned into a consumer product — "
             "signal processing and machine learning applied to a physical interface.",
             ["Machine listening", "Signal processing"])),
    dict(seed=1,  cat="research",             year="2010 — 11",
         it=("IRCAM", "Machine learning engineer · Parigi",
             "Ingegneria della ricerca all'istituto per la ricerca acustica e musicale: machine "
             "listening e analisi di dati audio sperimentali. L'origine della dimestichezza con i "
             "dataset scientifici.",
             ["Ricerca", "Machine listening"]),
         en=("IRCAM", "Machine learning engineer · Paris",
             "Research engineering at the institute for acoustic and music research: machine "
             "listening and analysis of experimental audio data. The origin of this practice's "
             "comfort with scientific datasets.",
             ["Research", "Machine listening"])),
    dict(seed=11, cat="strategy",             year="In corso",
         it=("Programmi executive sull'AI", "IULM · Università Cattolica · Camera di Commercio di Milano",
             "Docenza e workshop su AI Adoption, governance e marketing data-driven — inclusi "
             "i seminari sugli agenti AI per la produttività aziendale con Microsoft e la Camera di "
             "Commercio di Milano.",
             ["Docenza", "Adozione"]),
         en=("Executive AI programmes", "IULM · Università Cattolica · Camera di Commercio Milano",
             "Teaching and workshop programmes on AI adoption, governance and data-driven "
             "marketing — including seminars on AI agents for business productivity run with "
             "Microsoft and the Milan Chamber of Commerce.",
             ["Teaching", "Adoption"])),
    dict(seed=13, cat="ai research product", year="2024",
         featured=True,
         url="https://github.com/alesaccoia/VoiceStreamAI",
         it=("VoiceStreamAI", "Open source · Python / JavaScript · MIT",
             "Server e client per trascrizione audio in near-realtime: streaming via WebSocket, "
             "voice activity detection di Huggingface e Whisper (faster-whisper) per il "
             "riconoscimento. Design modulare per sostituire VAD e ASR, strategie di chunking "
             "configurabili, supporto multilingua.",
             ["Whisper", "VAD", "WebSocket", "Real-time"]),
         en=("VoiceStreamAI", "Open source · Python / JavaScript · MIT",
             "Server and client for near-realtime audio transcription: WebSocket streaming, "
             "Huggingface voice activity detection and Whisper (faster-whisper) for recognition. "
             "Modular design for swapping VAD and ASR components, configurable chunking "
             "strategies, multilingual support.",
             ["Whisper", "VAD", "WebSocket", "Real-time"])),
    dict(seed=14, cat="research analytics product", year="2025",
         url="https://github.com/alesaccoia/priors",
         it=("Priors", "Open source · React · MIT",
             "Strumento web per costruire e analizzare reti bayesiane: canvas interattivo, tabelle "
             "di probabilità condizionata modificabili, inferenza esatta in tempo reale e "
             "aggiornamento visivo dei posteriori quando si osserva un'evidenza. Un'alternativa "
             "leggera e moderna a strumenti desktop come GeNIe, con estetica ispirata a Tufte.",
             ["Reti bayesiane", "Inferenza esatta", "Modelli decisionali", "React"]),
         en=("Priors", "Open source · React · MIT",
             "Web tool for building and analysing Bayesian networks: interactive canvas, editable "
             "conditional probability tables, real-time exact inference, and posteriors that update "
             "visually as evidence is set. A light, modern alternative to desktop tools such as "
             "GeNIe, with a Tufte-inspired interface.",
             ["Bayesian networks", "Exact inference", "Decision models", "React"])),

    # ---- recovered from the previous site (mindmaker_www) ----
    dict(seed=15, cat="ai strategy", year="2023",
         it=("Mai Dire AI", "Formato divulgativo · con Angela, Christelle, Sara, Cristian",
             "Un formato che rende l'intelligenza artificiale accessibile e comprensibile. Prende "
             "per mano chi guarda e lo accompagna dentro un mondo affascinante e complicato, senza "
             "gergo e senza mal di testa.",
             ["Divulgazione", "Formato", "AI"]),
         en=("Mai Dire AI", "Explainer format · with Angela, Christelle, Sara, Cristian",
             "An AI format that makes artificial intelligence accessible and understandable — like "
             "the cousin who can explain complex things without giving you a headache.",
             ["Outreach", "Format", "AI"])),
    dict(seed=16, cat="research product", year="2020",
         url="https://github.com/alesaccoia/festival_flinger",
         it=("Festival Flinger", "Open source · recupero archeologico",
             "Missione di salvataggio del modulo Flinger per il sintetizzatore vocale cantato "
             "Festival, ormai scomparso: Makefile mancanti o obsoleti, codice pesantemente "
             "modificato e pensato per Windows. Portato su Unix/macOS sistemando l'aritmetica dei "
             "puntatori a 32 bit e i flag di configurazione.",
             ["Sintesi vocale", "C/C++", "Porting"]),
         en=("Festival Flinger", "Open source · archaeological rescue",
             "Rescue of the nearly vanished Flinger module for the Festival singing speech "
             "synthesiser: hacked source, missing or outdated Makefiles, Windows-only build. Ported "
             "to Unix/macOS with 32-bit pointer arithmetic fixes and proper configuration flags.",
             ["Speech synthesis", "C/C++", "Porting"])),
    dict(seed=17, cat="creative product", year="2015",
         url="https://abcdinamo.com/typefaces/galapagos",
         it=("Galapagos App", "Dinamo · con Felix Salut, Johannes Breyer, Fabian Harb",
             "App per il carattere ABC Galapagos di Dinamo: un sistema tipografico modulare con 42 "
             "tagli e 5 pesi, in cui le forme evolvono l'una dall'altra. Permette ai designer di "
             "sperimentare allineamento verticale e alternative stilistiche, traducendo in digitale "
             "i blocchi fisici del Galapagos Game.",
             ["Tipografia", "App", "Design tool"]),
         en=("Galapagos App", "Dinamo · with Felix Salut, Johannes Breyer, Fabian Harb",
             "App for Dinamo's ABC Galapagos typeface — a modular system of 42 cuts and 5 weights "
             "whose character forms evolve from one another. Lets designers explore vertical grid "
             "alignment and stylistic alternates, turning Felix Salut's physical Galapagos Game "
             "blocks into a font.",
             ["Typography", "App", "Design tool"])),
    dict(seed=18, cat="creative", year="2014",
         url="https://dinahmoe.com/canada-goose-out-there",
         it=("Canada Goose — Out There", "Dinahmoe · direzione tecnica",
             "Esperienza digitale interattiva per la campagna «Out There» di Canada Goose: "
             "contenuti web immersivi per esplorare l'eredità outdoor del marchio attraverso "
             "storytelling e interazione.",
             ["Interattivo", "Web audio", "Campagna"]),
         en=("Canada Goose — Out There", "Dinahmoe · technical direction",
             "Interactive digital experience for Canada Goose's “Out There” campaign: immersive "
             "web content letting users explore the brand's outdoor heritage through digital "
             "storytelling and interaction.",
             ["Interactive", "Web audio", "Campaign"])),
    dict(seed=19, cat="creative research", year="2013",
         url="https://www.dandad.org/awards/professional/2013/digital-design/19613/this-exquisite-forest/",
         it=("This Exquisite Forest", "Google Creative Lab · Tate Modern · Dinahmoe",
             "Installazione interattiva prodotta da Google e Tate Modern: gli artisti creano brevi "
             "animazioni con strumenti web di disegno e musica e possono ramificarsi dalle "
             "animazioni altrui, generando linee temporali ad albero. Alla Tate i visitatori "
             "esploravano e contribuivano ad alberi di animazioni a grandezza naturale. D&amp;AD "
             "Wood Pencil per il Digital Design.",
             ["Installazione", "Google · Tate", "D&amp;AD Wood Pencil"]),
         en=("This Exquisite Forest", "Google Creative Lab · Tate Modern · Dinahmoe",
             "Interactive installation produced by Google and Tate Modern: artists collaboratively "
             "create short animations with web drawing and music tools, branching off one another "
             "into tree-like timelines. At Tate Modern visitors explored and contributed to "
             "life-size animation trees. Awarded a D&amp;AD Wood Pencil for Digital Design.",
             ["Installation", "Google · Tate", "D&amp;AD Wood Pencil"])),
    dict(seed=20, cat="creative", year="2013",
         url="https://dinahmoe.com/beck-hello-again",
         it=("Beck — Hello Again", "Dinahmoe · direzione tecnica",
             "Esperienza musicale interattiva per «Hello Again» di Beck: un ambiente digitale che "
             "risponde alla musica e permette di attraversare il brano in modo non lineare.",
             ["Interattivo", "Web audio", "Musica"]),
         en=("Beck — Hello Again", "Dinahmoe · technical direction",
             "Interactive music experience for Beck's “Hello Again”: an immersive digital "
             "environment that responds to the music and lets users explore the track.",
             ["Interactive", "Web audio", "Music"])),
    dict(seed=21, cat="creative", year="2013",
         url="https://dinahmoe.com/infiniti-deja-view",
         it=("Infiniti — Deja View", "Dinahmoe · direzione tecnica",
             "Campagna digitale interattiva per Infiniti: esperienze web costruite attorno "
             "all'approccio del marchio al design e alla tecnologia dell'auto.",
             ["Interattivo", "Campagna"]),
         en=("Infiniti — Deja View", "Dinahmoe · technical direction",
             "Interactive digital campaign for Infiniti: web experiences built around the brand's "
             "approach to automotive design and technology.",
             ["Interactive", "Campaign"])),
    dict(seed=22, cat="creative", year="2013",
         url="https://dinahmoe.com/outcast",
         it=("Outcast", "Dinahmoe · direzione tecnica",
             "Esperienza digitale immersiva sui temi dell'isolamento e della connessione, "
             "costruita su storytelling interattivo.",
             ["Interattivo", "Narrazione"]),
         en=("Outcast", "Dinahmoe · technical direction",
             "Immersive digital experience exploring isolation and connection through interactive "
             "storytelling.",
             ["Interactive", "Narrative"])),
    dict(seed=23, cat="creative research", year="2012",
         url="https://agneschavez.com/xtreeprojectother-works/xtrees/",
         it=("(x)trees", "Agnes Chavez · concept originale Jared Tarbell",
             "Installazione che genera dinamicamente una foresta di alberi a partire da SMS e "
             "tweet. Conversione da Flash a OpenFrameworks per la mostra Machine Wilderness di "
             "ISEA2012 all'Albuquerque Museum of Fine Art: proiezione d'angolo 20×20 piedi, "
             "messaggi del pubblico che diventano rami in tempo reale. Citata nel volume «Modes of "
             "Knowing: Resources from the Baroque» (Mattering Press, 2016).",
             ["Installazione", "OpenFrameworks", "ISEA2012"]),
         en=("(x)trees", "Agnes Chavez · original concept Jared Tarbell",
             "Installation generating a forest of trees from SMS and tweets. Converted from Flash "
             "to OpenFrameworks for the ISEA2012 Machine Wilderness exhibit at Albuquerque Museum "
             "of Fine Art: a 20×20ft corner projection where audience messages become branches in "
             "real time. Cited in “Modes of Knowing: Resources from the Baroque” (Mattering Press, "
             "2016).",
             ["Installation", "OpenFrameworks", "ISEA2012"])),
    # ---- labs ----
    dict(seed=24, cat="creative product", year="Lab",
         url="https://www.mpcsmith.com/",
         it=("MPC Smith", "Applicazione macOS nativa",
             "Creazione e manipolazione di pattern MIDI: interfaccia a griglia per pattern ritmici "
             "complessi, uscita MIDI in tempo reale e integrazione con hardware esterno. Swift e "
             "Core MIDI.",
             ["Swift", "Core MIDI", "macOS"]),
         en=("MPC Smith", "Native macOS application",
             "MIDI pattern creation and manipulation: grid-based interface for complex rhythmic "
             "patterns, real-time MIDI output and integration with external hardware. Built with "
             "Swift and Core MIDI.",
             ["Swift", "Core MIDI", "macOS"])),
    dict(seed=25, cat="creative", year="Lab",
         url={"it": "algosynth.html", "en": "algosynth.html"},
         it=("AlgoSynth", "Sequencer algoritmico",
             "Ispirato ad Acroyear di Autechre: generazione di pattern, uscita MIDI, controllo dello "
             "swing e song mode multitraccia, con controllo dei parametri in tempo reale e supporto "
             "Web MIDI.",
             ["Web MIDI", "Algoritmico", "Sequencer"]),
         en=("AlgoSynth", "Algorithmic sequencer",
             "Inspired by Autechre's Acroyear: pattern generation, MIDI output, swing control and "
             "multi-track song mode, with real-time parameter control and Web MIDI support.",
             ["Web MIDI", "Algorithmic", "Sequencer"])),
    dict(seed=26, cat="creative", year="Lab",
         url={"it": "moire.html", "en": "moire.html"},
         it=("Moire", "Sintesi audiovisiva",
             "Generatore di pattern moiré con sintesi audio-video sincronizzata: più tipi di "
             "pattern (linee, griglia, cerchi, radiale), controllo dei parametri in tempo reale e "
             "sintesi FM agganciata alla parte visiva.",
             ["WebGL", "Sintesi FM", "Audiovisivo"]),
         en=("Moire", "Audio-visual synthesis",
             "Moiré pattern generator with synchronised audio-visual synthesis: multiple pattern "
             "types (lines, grid, circles, radial), real-time parameter control, and FM synthesis "
             "locked to the visuals.",
             ["WebGL", "FM synthesis", "Audio-visual"])),
    dict(seed=27, cat="creative", year="Lab",
         it=("Spray", "Video sintetizzatore WebGL",
             "Sintetizzatore video minimale ispirato ad Alva Noto e Ryoji Ikeda: quindici modalità "
             "shader procedurali — strisce, griglia, punti, rumore, voronoi, increspature, moiré, "
             "quasicristallo, caleidoscopio, halftone, flow — con controllo in tempo reale e "
             "modalità a schermo intero.",
             ["WebGL", "Shader", "Generativo"]),
         en=("Spray", "WebGL video synthesiser",
             "Minimalist video synthesiser inspired by Alva Noto and Ryoji Ikeda: fifteen "
             "procedural shader modes — stripes, grid, dots, noise, warp, voronoi, ripples, moiré, "
             "quasicrystal, kaleidoscope, crackle, halftone, flow — with real-time control and "
             "fullscreen support.",
             ["WebGL", "Shaders", "Generative"])),
    dict(seed=28, cat="ai product", year="Lab",
         url="https://wiki.mindmaker.it/index.php/Pagina_principale",
         it=("Wiki AI", "Base di conoscenza pubblica",
             "Wiki divulgativa sull'intelligenza artificiale: voci, definizioni e materiali "
             "didattici mantenuti pubblicamente.",
             ["Wiki", "Divulgazione"]),
         en=("Wiki AI", "Public knowledge base",
             "A public wiki on artificial intelligence: entries, definitions and teaching material "
             "maintained openly.",
             ["Wiki", "Outreach"])),
    dict(seed=30, cat="research ai", year="Lab",
         url="https://github.com/alesaccoia/chessmaster",
         it=("ChessMaster", "Open source · PyTorch",
             "Implementazione in PyTorch di reinforcement learning profondo per gli scacchi, "
             "ispirata all'approccio self-play di AlphaZero: l'agente impara giocando contro se "
             "stesso, con registrazione automatica delle partite e generazione video.",
             ["PyTorch", "Reinforcement learning", "Self-play"]),
         en=("ChessMaster", "Open source · PyTorch",
             "PyTorch implementation of deep reinforcement learning for chess, inspired by "
             "AlphaZero's self-play approach: the agent learns entirely by playing itself, with "
             "automatic game recording and video generation.",
             ["PyTorch", "Reinforcement learning", "Self-play"])),
]

# ---------------------------------------------------------------- copy
L_IT = dict(
    lang="it", other_label="EN", brand_sub="Data, AI e Marketing",
    nav=("Studio", "Progetti", "Chi sono", "Case study", "Blog", "Metodologia"),
    nav_open="Apri il menu",
    news_label="In evidenza",
    news=[("10 agosto 2026", "Nuovo case study — James: misurazione omnichannel e piano editoriale per una società di servizi educativi", "case-james.html"),
          ("Apr — Mag 2026", "Tre seminari «Agenti AI e strumenti di Intelligenza Artificiale per la produttività aziendale» con Microsoft e Camera di commercio di Milano — primo appuntamento 4 maggio, Microsoft House"),
          ("2026", "Disponibile per conferenze, keynote e lezioni su AI Adoption, strategia dei dati e crescita"),
          ("A.A. 2025/26", "Corsi attivi: IULM e Università Cattolica")],
    title="Iside Systems — AI Enablement, Data e Marketing Strategy",
    desc="Strategia e scienza dei dati, AI Adoption, operations di marketing e crescita. "
         "Costruisco la base su cui i team decidono. Alessandro Saccoia, Milano.",
    hero_meta="Iside Systems SRLS — Milano",
    h1="AI Enablement, Data e Marketing Strategy.",
    lede="Costruisco la base agentica su cui un team prende decisioni data driven, guido le "
         "organizzazioni nell'AI Adoption e curo le operations di marketing e growth — strumenti, "
         "automazioni, misurazione — trasformando entrambe in pratica quotidiana. Affianco i team "
         "con percorsi di formazione e supporto strategico continuativo, anche in modalità "
         "fractional. Né un'agenzia né una software house.",
    chips=["Strategia e Data Sciences", "AI Adoption", "Operations marketing e crescita", "Advisory e docenza"],
    m_lbl="Metodologia",
    m_h2="L’AI in azienda è<br>sviluppo organizzativo<br>prima che modelli.",
    m_p="Un whitepaper in nove sezioni: dove entra la tecnologia nei processi, come si legge la "
        "cultura, come si diagnostica un problema prima di scegliere lo strumento, come si "
        "sviluppano le persone, come si allocano i compiti fra umano e sistema, e con quali "
        "indicatori si valuta il risultato.",
    m_steps=["Diagnosi", "Cultura", "Sviluppo delle persone", "Allocazione dei compiti",
             "Progettazione", "Valutazione"],
    m_cta="Leggi il whitepaper",
    blog_lbl="Dal blog",
    blog_h2="Scrivo quello<br>che imparo.",
    blog_more="Tutti gli articoli",
    am_lbl="AI Maturity Check",
    am_h2="A che punto è la tua azienda con l’AI?",
    am_p="16 domande, 5 minuti, gratis.",
    am_cta="Fai il check",
    pos_lbl="01 — Il punto",
    pos_h2="Mancano numeri<br>di cui fidarsi.",
    pos_p=["Quasi tutti sanno già, a grandi linee, cosa dovrebbero fare. Quello che li blocca è che i "
           "numeri non parlano fra loro, gli strumenti non si comunicano, e metà settimana se ne va "
           "a montare report a mano e a analizzarli, togliendo tempo al team.",
           "<mark>Il mio lavoro è informato dalla strategia ma parte dalla base: decidere cosa "
           "misurare e cosa modellare, far arrivare i dati dove servono senza che nessuno li "
           "ricopi, costruire i modelli che trasformano quei numeri in una decisione, e quando "
           "serve portare l'AI dentro il flusso di lavoro fino al punto in cui toglie davvero "
           "lavoro ripetitivo alle persone.</mark>",
           "Posso costruire e prototipare tutto questo, attingendo da una codebase personale estesa. "
           "Per lo sviluppo finale lavoro insieme al vostro team, oppure a un partner che posso "
           "coinvolgere io."],
    cap_lbl="02 — Cosa faccio",
    caps=[("Strategia e<br>Data Science",
           "Cosa misurare e cosa modellare, prima ancora di quale strumento comprare. Modelli "
           "statistici, data mining e machine learning sui dati che avete già: previsioni, "
           "segmentazione, esperimenti, e una lettura intuitiva dei risultati.",
           ["Modellazione statistica", "Data mining", "Machine learning", "Previsione", "Esperimenti", "Dati scientifici"]),
          ("AI <br>Adoption",
           "Portare l'adozione fino al punto in cui l'organizzazione va avanti da sola. Casi d'uso "
           "che pagano davvero, "
           "costo reale di esercizio, chi deve cambiare modo di lavorare, cosa l'AI Act obbliga a "
           "documentare. Certificato in AI &amp; Law e AI Governance.",
           ["Selezione casi d'uso", "Pilota → produzione", "Governance", "AI Act", "Formazione", "Change"]),
          ("Operations di<br>marketing e crescita",
           "L'impianto che rende autonomo un team: tracking plan seguito davvero, eventi e pipeline "
           "in un unico posto, flussi CRM e lifecycle che partono da soli, dashboard con una cadenza "
           "di lettura. Una definizione condivisa di conversione, e basta numeri montati a mano.",
           ["Tracking plan", "GA4 · GTM", "Pipeline dati", "CRM e lifecycle", "Automazioni", "Dashboard"]),
          ("Advisory per<br>founder e team",
           "Le decisioni difficili, senza una casella nell'organigramma: è fattibile con i dati e le "
           "persone che avete, si compra o si costruisce, quale fornitore, chi assumere per primo. "
           "Se uno strumento esistente risolve già il problema, lo dico invece di aprire un cantiere.",
           ["Fattibilità", "Build vs buy", "Scelta fornitori", "Due diligence", "Assunzioni", "Retainer o equity"])],
    sect_lbl="03 — Dove si applica",
    sect_h2="Qualunque campo<br>con dati da scavare.",
    sect_p="Marketing e crescita. Formazione. Operations e conoscenza interna. Dati scientifici e "
           "di ricerca — elaborazione del segnale, machine listening e dataset sperimentali sono il "
           "punto di partenza, all'IRCAM, e restano pienamente in perimetro.",
    sect_chips=["Marketing e crescita", "Policy e regolazione", "Formazione", "Operations", "Ricerca scientifica", "Media e audio"],
    proj_lbl="04 — Progetti selezionati",
    proj_more="Vedi l'indice completo dei progetti →",
    fig_lbl="05 — Misurazione omnichannel",
    fig_h2="Un solo modello,<br>tutte le piattaforme.",
    fig_p1="Imposto un framework di misurazione omnichannel e multitouch, con definizioni condivise "
           "e dati che confluiscono in un unico modello, invece di mille dashboard che raccontano "
           "storie diverse.",
    fig_p2="Un software proprietario, che genera piani editoriali "
           "coerenti con le esigenze di costruzione del funnel di vendita: ogni contenuto e ogni "
           "investimento risponde a uno stadio preciso, e la misurazione torna indietro sullo stesso "
           "schema.",
    fig_legend="peso pianificato per stadio",
    fig_plan="piano editoriale ↗",
    fig_note="Figura: struttura illustrativa — dati dei clienti non riportati",
    speak_lbl="06 — Conferenze e docenza",
    speak_h2="Disponibile per<br>conferenze e lezioni.",
    speak_p="Intervengo volentieri a conferenze pubbliche, keynote, panel, lezioni universitarie e "
            "workshop aziendali, in italiano, inglese o francese. I temi ricorrenti sono l'AI Adoption "
            "nelle organizzazioni, la strategia dei dati e il marketing data-driven — "
            "trattati come problemi operativi, con esempi reali, non come panoramiche di settore.",
    speak_topics=["AI Adoption in azienda", "Agenti e automazione", "Governance e AI Act",
                  "Strategia e scienza dei dati", "Marketing data-driven", "Modelli decisionali"],
    speak_rows=[("Apr — Mag 2026", "Agenti AI e strumenti di Intelligenza Artificiale per la produttività aziendale",
                 "Ciclo di tre seminari con Camera di commercio Milano Monza Brianza Lodi, Formaper "
                 "e Microsoft. Primo appuntamento il 4 maggio 2026, 15:00–18:00, Microsoft House, "
                 "Viale Pasubio 21, Milano: assistenti e agenti AI, prompt engineering per le PMI, "
                 "strumenti di automazione e laboratorio pratico finale. Ingresso gratuito, posti "
                 "limitati.", "https://www.formaper.it/servizi-per-le-imprese/formazione-impresa-digitale/agenti-ai-produttivita-aziendale-evento-cciaa-microsoft/"),
                ("Dal 2022", "Modelli decisionali per il marketing data-driven",
                 "Corso a contratto, IULM — tenuto ogni anno accademico dal 2022.", "https://iulm.coursecatalogue.cineca.it/corsi/2025/487/insegnamenti/2026/1992_22102_7871/2025/1992?schemaid=1499"),
                ("A.A. 2025/26", "Statistica — primo modulo",
                 "Università Cattolica, corso di laurea in Business and Finance.", "https://www.unicatt.it/corsi/triennale/business-and-finance-brescia.html"),
                ("A.A. 2025/26", "Intelligenza artificiale",
                 "Università Cattolica, master in Comunicazione per le industrie creative, Milano.", "https://www.unicatt.it/corsi/master-universitari/milano/comunicazione-per-le-industrie-creative.html"),
                ("2025", "Statistica e AI",
                 "Camera di commercio di Milano Monza Brianza Lodi — corso Data Analyst &amp; AI Explorer."),
                ("2013 — 2017", "Machine learning per l'audio · elaborazione del segnale",
                 "Visiting professor, Université de Franche-Comté / Conservatoire du Pays de "
                 "Montbéliard, Montbéliard (Francia). Music technology e AI al Conservatorio, con "
                 "focus sul machine learning per l'analisi audio. Quattro anni."),
                ("In corso", "Workshop executive su adozione e governance dell'AI",
                 "Sessioni private per team di leadership, su richiesta.")],
    speak_cta="Richieste per conferenze e docenza →",
    eng_lbl="07 — Come si lavora insieme",
    engs=[("Sprint di setup", "Quattro / sei settimane",
           "Strumentare, collegare, automatizzare. Alla fine il team ha un unico insieme di numeri "
           "condivisi, i report arrivano da soli, e le prime due o tre automazioni sono attive e "
           "documentate."),
          ("Embedded", "Giorni al mese",
           "Lavoro dentro il team con continuità: tenere onesto lo stack, estendere le automazioni, "
           "reggere la cadenza di misurazione e integrare l'AI nei flussi man mano che il team è "
           "pronto."),
          ("Advisory", "Mensile o equity",
           "Impegno più leggero per founder e leadership. Sessioni regolari in cui rivediamo le "
           "decisioni prese, verifico le affermazioni tecniche dei fornitori e stimo la "
           "fattibilità prima che partano i costi. A retainer o, "
           "in early stage, in parte in equity."),
          ("Collaborazione tecnica", "Da valutare insieme",
           "Per qualunque progetto che valga la pena costruire. Se l'idea è interessante e c'è "
           "spazio per lavorarci davvero, si trova la forma: collaborazione fra pari, ricerca, "
           "prototipo condiviso, contributo open source. Scrivimi cosa hai in mente.")],
    cta_h2="Si parte dal report<br>di cui nessuno si fida.",
    cta_p="Di solito è la via d'ingresso più rapida. La prima conversazione copre cosa misura oggi "
          "il team, dove finisce il lavoro manuale, e cosa si può automatizzare o far rispondere "
          "all'AI entro un mese. Se quello che serve è un'agenzia o una software house, lo dico.",
    cta_link="Chi sono, CV e contatti →",
    foot_pages="Pagine", foot_caps="Cosa faccio", foot_studio="Iside Systems SRLS",
    foot_sdi="Codice destinatario",
    foot_colophon="Iside Systems SRLS — P.IVA 14733480967",
    # ---- projects page
    p_title="Progetti — Iside Systems",
    p_desc="Indice dei progetti: sistemi AI, analytics e crescita, ricerca e strategia. Iside Systems, Alessandro Saccoia.",
    p_kicker="Indice progetti",
    p_h1="Esperienza in sistemi, misurazione e decisioni.",
    p_lede="Ruoli ricoperti, non progetti venduti. Ogni voce indica la posizione — fondatore, CTO, "
           "responsabile di funzione, ingegnere di ricerca — perché quello che conta qui è "
           "l'ampiezza dei problemi affrontati.",
    p_filters=[("all","Tutti"),("ai","Sistemi AI"),("analytics","Analytics e crescita"),
               ("product","Prodotti e open source"),("creative","Interattivo e audio"),
               ("research","Ricerca"),("strategy","Strategia")],
    p_count="voci mostrate",
    p_note="Le voci contrassegnate con ↗ portano al repository o alla pagina ufficiale del progetto.",
    # ---- about page
    a_title="Chi sono e contatti — Iside Systems",
    a_desc="Alessandro Saccoia — strategia dei dati, AI Adoption, operations di marketing e crescita, docenza. CV e contatti.",
    portrait_file="img/alessandro.jpg",
    portrait_alt="Alessandro Saccoia",
    portrait_cap="Alessandro Saccoia — Milano",
    a_kicker="Chi sono",
    a_h1="Iside Systems è lo studio di Alessandro Saccoia.",
    privacy_link="Privacy policy",
    privacy_updated="Ultimo aggiornamento",
    a_lede="Tecnologo, professore a contratto, co-founder. Anni di esperienza in misurazione, "
           "dati, strumenti e automazione — fra istituti di ricerca, ad-tech, telco, misurazione "
           "dei media e oggi le mie stesse aziende.",
    a_p=["Iside Systems è il modo in cui questo lavoro viene venduto: strategia e scienza dei dati, "
         "AI Adoption, e le operations di marketing e crescita che le tengono insieme. Né "
         "agenzia né software house. Costruisco e prototipo quello che serve allo strato "
         "operativo; quando qualcosa cresce oltre, spetta al vostro team o a un partner.",
         "Attualmente co-fondatore di Thembi, piattaforma di policy intelligence europea; alla guida "
         "del marketing di Mentor Ripetizioni, dove l'infrastruttura è costruita in casa; e "
         "professore a contratto alla IULM."],
    a_cur="01 — Oggi", a_prev="02 — In precedenza", a_cred="03 — Formazione, credenziali, docenza",
    a_speak="04 — Conferenze e docenza", a_contact="05 — Contatti",
    a_cred_cards=[("Formazione", "Informatica, Università degli Studi di Milano."),
                  ("Certificazioni", "AI and Law. AI Governance. AWS Certified Cloud Engineer. Formazione in transformative AI e AI safety."),
                  ("Docenza", "IULM — Modelli decisionali per il marketing data-driven, dal 2022/23. "
                              "Università Cattolica — Statistica (Business and Finance) e "
                              "Intelligenza artificiale (master in Comunicazione per le industrie "
                              "creative, Milano). Université de Franche-Comté / Conservatoire du Pays "
                              "de Montbéliard — visiting professor 2013–2017. Camera di commercio di "
                              "Milano e Formaper — AI per le imprese."),
                  ("Lingue", "Italiano, inglese e francese: lezioni, conferenze e materiali in tutte e tre. "
                             "Il francese viene da quattro anni di insegnamento in Francia, "
                             "all'Université de Franche-Comté. Lavoro in Italia e all'estero.")],
    a_contact_h2="Si parte dal problema,<br>non dalla tecnologia.",
    a_contact_p="I messaggi utili raccontano cosa misura oggi il team, dove finisce il lavoro "
                "manuale, e quale decisione continua a essere presa a sensazione. Una conversazione "
                "basta di solito per dire cosa è sistemabile entro un mese. Se serve un'agenzia o "
                "una software house, lo dico.",
    a_studio="Studio", a_direct="Diretto",
    f_name="Nome", f_email="Email", f_org="Organizzazione", f_topic="Di cosa si tratta",
    f_msg="Messaggio", f_send="Invia richiesta",
    f_topics=["Strategia e scienza dei dati", "AI Adoption", "Operations marketing e crescita",
              "Conferenza o docenza", "Advisory", "Altro"],
    f_req="Nome, email e messaggio sono obbligatori.",
    f_ok="Messaggio inviato. Ti rispondo entro pochi giorni.",
    f_sending="Invio in corso…",
    f_fallback="Invio diretto non disponibile. Apro il tuo client di posta con il messaggio pronto.",
    f_hp="Lascia vuoto questo campo",
    f_done_title="Messaggio inviato.",
    f_done_lead="Ti rispondo entro pochi giorni, di solito prima. Se nel frattempo vuoi aggiungere "
                "qualcosa, scrivi direttamente ad {mail}.",
    f_done_reply="Risponderò a",
    f_done_again="Invia un altro messaggio",
    elsewhere="Altrove",
    cs_title="Case study — Iside Systems",
    cs_desc="Tre esperienze recenti: adozione dell'AI dentro le business unit di una società di "
            "consulenza, James — la piattaforma di marketing operations per una società di servizi "
            "educativi — e la messa in sicurezza dell'infrastruttura di una startup.",
    cs_kicker="Case study",
    cs_h1="I miei modi di far entrare i dati e l'AI in un'organizzazione.",
    cs_lede="Tre esperienze recenti in cui ho aiutato altrettanti clienti: la prima parte dalle "
            "persone e dai loro processi, la seconda dagli strumenti di misurazione, la terza "
            "dall'infrastruttura che regge tutto il resto.",
    mini_cta=["Un problema simile sul tavolo? Scrivimi →",
              "Se il pezzo che manca è questo, scrivimi →",
              "Prima conversazione senza impegno — scrivimi →",
              "Curioso di capire come si applica da voi? Scrivimi →"],
    cs_card_cta="Leggi il caso",
    cs_home_lbl="04 — Case study",
    cs_home_h2="Tre modi diversi<br>di entrare.",
    cs_home_p="Formazione che finisce dentro i processi, misurazione che tiene insieme le varie "
              "piattaforme, infrastruttura che regge la crescita. Tre esperienze recenti, "
              "raccontate per intero.",
    cs_home_more="Tutti i case study →",
    cs_back="Torna ai case study",
    cs_other="Gli altri case study",
    cs_fig_out="FUNNEL|PIANO|CALENDARIO|SOV",
    cs_fig_src="META|TIKTOK|ADS SEARCH|ADS DISPLAY|CRM · DEM|REFERRAL",
    cs_cta_h2="Tre porte diverse<br>sullo stesso problema.",
    cs_cta_p="Sono tre punti d'ingresso diversi: le persone, la misurazione, l'infrastruttura. "
             "Il primo passo è capire quale dei tre corrisponde al problema che avete adesso.",
    cs_cta_link="Scrivimi →",
    cs_cases=[dict(
        slug="ai-adoption",
        n="01", lbl="Adozione dell'AI — società di consulenza e formazione",
        card="Un percorso che parte dall'aula e finisce dentro i processi: seminari progressivi "
             "per costruire il linguaggio comune, poi workshop con le singole business unit per "
             "mappare il lavoro reale, individuare i low hanging fruit e disegnare agenti che "
             "rispettino i metodi già in uso.",
        h2="Dall'aula<br>dentro i processi.",
        ctx=["L'AI era già entrata in azienda dalla porta di servizio. Ognuno usava lo strumento "
             "che preferiva, con criteri propri, senza una risposta condivisa alle due domande "
             "che bloccano tutti — dove finiscono i nostri dati, e di chi è la responsabilità "
             "sull'output.",
             "I rischi erano organizzativi. Competenze che divergono, know-how che esce senza che "
             "nessuno se ne accorga, e un uso che resta confinato alla curiosità personale invece "
             "di diventare capacità dell'organizzazione."],
        fig="training",
        steps=[("Fondamenta", "Come funzionano davvero gli strumenti",
                "Un modello mentale non tecnico: come i modelli generano contenuti, differenza fra "
                "generazione, ricerca e knowledge, estrazione di dati da documenti e immagini, "
                "ruolo del contesto, perché sbagliano."),
               ("Rischi", "Uso consapevole e gestione dei rischi",
                "Cosa succede ai dati: input, elaborazione, output, dove risiedono. GDPR e AI Act "
                "inquadrati in modo pratico, protezione del know-how, rischi di leakage e uso "
                "improprio degli output."),
               ("Automazione", "Produttività e automazione",
                "Dal task singolo al processo: pattern ricorrenti, automazioni deterministiche, "
                "introduzione agli agenti, e soprattutto quando automatizzare e quando no."),
               ("Workshop", "Con le singole business unit",
                "Qui il percorso smette di essere formazione e diventa analisi. Sessioni dedicate "
                "a ogni business unit per capire a fondo come si lavora davvero: quali passaggi si "
                "ripetono, dove si perde tempo, quali controlli non sono negoziabili. Da lì "
                "emergono i low hanging fruit — le cose che si possono migliorare subito, senza "
                "riscrivere il modo di lavorare."),
               ("Progettazione", "Agenti disegnati sui metodi esistenti",
                "Gli agenti nascono dalla mappatura e seguono i metodi che l'organizzazione ha "
                "già, invece di chiederle di adattarsi a loro. Uno strumento che impone il proprio "
                "metodo viene aggirato nel giro di un mese."),
               ("Nel tempo", "Pillole di aggiornamento",
                "Contenuti brevi e ricorrenti costruiti sui feedback dei seminari e sull'uso "
                "osservato: riassumere documenti lunghi, estrarre dati strutturati, deep research, "
                "aggiornamenti normativi.")],
        out="Alla fine le persone fanno le stesse cose meglio e più in fretta, e l'organizzazione "
            "sa fare cose che prima non sapeva fare. I seminari costruiscono il "
            "linguaggio comune, i workshop con le business unit trovano dove intervenire davvero, "
            "gli agenti consolidano il guadagno, le pillole impediscono che tutto si spenga dopo "
            "un mese.",
        chips=["Percorso di seminari", "Workshop per business unit", "Mappatura dei processi",
               "Low hanging fruit", "Agenti sui metodi esistenti", "GDPR e AI Act"]),
    dict(
        slug="james",
        n="02", lbl="James — marketing operations per una società di servizi educativi",
        card="Meta, TikTok, Google Ads Search e Display, più le iniziative CRM sulla base "
             "clienti: piattaforme diverse, dashboard diverse, nessun numero condiviso. "
             "James unisce ingestione dei dati, modello del funnel, pianificazione e misurazione "
             "in un unico posto: il piano editoriale nasce dagli stadi del funnel invece di essere "
             "scritto a parte.",
        date="10 agosto 2026",
        h2="Tante piattaforme di marketing,<br>una sola versione<br>dei numeri.",
        ctx=["Meta, Google, il sito, il CRM: ogni piattaforma con la sua dashboard e la sua "
             "definizione di conversione. Il piano editoriale viveva su un foglio, il budget su un "
             "altro, e nessuno dei due parlava con la spesa reale.",
             "Invece di comprare l'ennesimo strumento ho costruito James: una piattaforma che tiene "
             "insieme ingestione dei dati, modello del funnel, pianificazione e misurazione. È "
             "indipendente dal cliente e riutilizzabile."],
        fig="james",
        steps=[("Ingestione", "Un solo magazzino",
                "I dati arrivano dalle piattaforme pubblicitarie e analytics e vengono raccolti in "
                "un unico posto, deduplicati per chiave naturale, così le sincronizzazioni "
                "ripetute non creano doppioni."),
               ("Modello", "Funnel configurabile",
                "Stadi e KPI si definiscono dall'interfaccia: metrica di origine, aggregazione, "
                "rapporti fra metriche, moltiplicatori, livello di entità. Ogni stadio può essere "
                "agganciato alle campagne reali."),
               ("Pianificazione", "Piano contro speso",
                "I piani budget scompongono il periodo per linea, in percentuale o in importo, e "
                "il confronto con la spesa reale è automatico. Le voci che sono effort operativo e "
                "non budget media restano fuori dai conti."),
               ("Esecuzione", "Calendario e cadenze",
                "Ogni canale ha una cadenza attesa — minimo e massimo di uscite nel periodo — e un "
                "ruolo dichiarato nel funnel. I contenuti in calendario portano canale, "
                "responsabile, campagna collegata e link al post pubblicato."),
               ("Canali", "Paid, ricerca e social",
                "Il modello copre l'intero mix: Meta, TikTok, Google Ads Search e Google Ads "
                "Display. Ogni canale entra con la propria spesa e il proprio ruolo nel funnel — "
                "la ricerca intercetta domanda esistente, display e social la costruiscono — e "
                "viene misurato con le stesse definizioni degli altri."),
               ("Base installata", "CRM, DEM e referral",
                "Accanto all'acquisizione ci sono le iniziative sulla base clienti: campagne DEM "
                "per il recupero dei clienti inattivi e programmi referral. Vivono nello stesso "
                "modello del paid, così il costo per acquisizione di un canale si confronta con "
                "quello di una riattivazione invece di stare su un foglio a parte."),
               ("Contesto", "Tag, eventi, concorrenza",
                "Tassonomia multidimensionale con quote attese per dimensione, eventi annotati "
                "direttamente sui grafici, e traffico mensile dei concorrenti importato per "
                "confrontare la propria quota con quella del mercato.")],
        out="Pianificazione e misurazione ora usano lo stesso modello. Il piano editoriale nasce "
            "dagli stadi del funnel invece di "
            "essere scritto a parte, e a fine mese la domanda «quanto abbiamo speso su cosa» ha "
            "una sola risposta.",
        chips=["Meta", "TikTok", "Google Ads Search", "Google Ads Display", "CRM e DEM",
               "Referral", "Funnel configurabile", "Piano vs speso", "Calendario editoriale",
               "Share of voice"]),
    dict(
        slug="cloud-scale",
        n="03", lbl="Infrastruttura e governance — startup educational",
        date="2026",
        card="Una piattaforma che funzionava, cresciuta più in fretta dell'ambiente che la "
             "ospitava. Migrazione su un'infrastruttura che regge la crescita, processo di "
             "sviluppo controllato, e un assessment su dati, AI Act e condizioni d'uso.",
        h2="Far reggere<br>quello che già<br>funziona.",
        ctx=["Il prodotto c'era ed era stato costruito con pragmatismo: piattaforma "
             "viva, utenti veri, funzionalità AI già in produzione. Quello che non reggeva era "
             "l'ambiente sotto — pensato per partire, non per assorbire traffico crescente e "
             "utenti contemporanei.",
             "Il rischio in questi casi arriva più tardi del down di oggi. Si manifesta quando "
             "ogni aumento di utilizzo obbliga a riprogettare tutto, e intanto nessuno sa dire dove "
             "passano i dati né con quali condizioni il servizio viene erogato."],
        fig="cloud",
        steps=[("Infrastruttura", "Migrazione verso un ambiente che scala",
                "Esportazione della piattaforma dall'ambiente esistente e configurazione ordinata "
                "di applicazione, database, accessi, backup e deployment. L'obiettivo è "
                "assorbire la crescita senza riprogettare il sistema a ogni salto di utilizzo."),
               ("Osservabilità", "Monitoraggio dal primo giorno",
                "Strumenti di monitoraggio impostati prima del primo incidente. Sapere come sta "
                "il sistema fa parte dell'infrastruttura quanto i server."),
               ("Processo", "Sviluppo più rapido e più controllato",
                "Organizzazione dell'ambiente e del processo di sviluppo — repository, revisione, "
                "assistenti di codice — per andare più veloci lungo un percorso documentato e "
                "tracciabile."),
               ("Assessment", "Dati, AI e fornitori esterni",
                "Analisi tecnico-organizzativa delle funzionalità AI e dei flussi di dati: cosa "
                "esce dal perimetro, verso quali fornitori, con quali implicazioni rispetto a "
                "GDPR, AI Act e sicurezza."),
               ("Condizioni", "Termini d'uso e licenza",
                "Dall'assessment nascono termini di utilizzo e licenza coerenti con come la "
                "piattaforma funziona davvero. Gli aspetti ordinari si gestiscono internamente; "
                "la revisione legale si riserva alle questioni che la meritano.")],
        out="Da fuori non si vede niente. Nessuna funzionalità nuova, nessun redesign. Cambia la "
            "traiettoria — la piattaforma può crescere senza rifarsi, il "
            "team sviluppa più in fretta con più controllo, e le domande su dati e condizioni "
            "d'uso hanno una risposta scritta prima che arrivi qualcuno a farle.",
        chips=["Migrazione cloud", "Backup e deployment", "Monitoraggio", "Processo di sviluppo",
               "GDPR e AI Act", "Termini d'uso"])],
    cookie_title="Cookie.",
    cookie_text="Questo sito usa cookie di misurazione per capire quali pagine vengono lette. "
                "Niente pubblicità, niente profilazione rivenduta a terzi. Se rifiuti, il sito "
                "funziona esattamente allo stesso modo.",
    cookie_accept="Accetto",
    cookie_reject="Rifiuto",
)

L_EN = dict(
    lang="en", other_label="IT", brand_sub="Data, AI and marketing",
    nav=("Practice", "Projects", "About", "Case studies", "Blog", "Methodology"),
    nav_open="Open the menu",
    news_label="Latest",
    news=[("10 August 2026", "New case study — James: omnichannel measurement and editorial planning for an online education company", "case-james.html"),
          ("Apr — May 2026", "Three seminars, “AI agents and AI tools for business productivity”, with Microsoft and the Milan Chamber of Commerce — first date 4 May, Microsoft House"),
          ("2026", "Available for conferences, keynotes and lectures on AI adoption, data strategy and growth"),
          ("2025/26", "Teaching at IULM and Università Cattolica")],
    title="Iside Systems — AI Enablement, Data and Marketing Strategy",
    desc="Data strategy and science, AI adoption, and the marketing and growth operations that make "
         "both real. Alessandro Saccoia, Milan.",
    hero_meta="Iside Systems SRLS — Milan",
    h1="AI Enablement, Data and Marketing Strategy.",
    lede="I build the agentic foundation a team makes data-driven decisions on, guide organisations "
         "through AI adoption, and run the marketing and growth operations — tooling, automation, "
         "measurement — turning both into daily practice. I work alongside teams through training "
         "programmes and continuing strategic support, fractional where that fits. Neither an "
         "agency nor a software house.",
    chips=["Data strategy &amp; data sciences", "AI adoption", "Marketing &amp; growth operations", "Advisory &amp; speaking"],
    m_lbl="Method",
    m_h2="AI in a company is<br>organisational development<br>before it is models.",
    m_p="A whitepaper in nine sections, in Italian: where the technology enters the processes, how "
        "to read the culture, how to diagnose a problem before choosing a tool, how people are "
        "developed, how tasks are allocated between human and system, and which indicators tell "
        "you whether it worked.",
    m_steps=["Diagnosis", "Culture", "Developing people", "Task allocation",
             "Design", "Evaluation"],
    m_cta="Read the whitepaper",
    blog_lbl="From the blog",
    blog_h2="I write down<br>what I learn.",
    blog_more="All posts",
    am_lbl="AI Maturity Check",
    am_h2="Where does your company stand on AI?",
    am_p="16 questions, 5 minutes, free — in Italian.",
    am_cta="Take the check",
    pos_lbl="01 — The point",
    pos_h2="The numbers<br>nobody trusts.",
    pos_p=["Most already know roughly what they should be doing. What stops them is that the numbers "
           "do not speak to each other, the tools do not communicate, and half the week goes to "
           "assembling reports by hand and reading them — time the team does not get back.",
           "<mark>My work is informed by strategy but starts at the foundation: deciding what to "
           "measure and what to model, getting the data where it is needed without anyone copying "
           "it, building the models that turn those numbers into a decision, and — where it helps — "
           "bringing AI into the workflow to the point where it genuinely removes repetitive "
           "work.</mark>",
           "I can build and prototype all of this, drawing on an extensive personal codebase. For "
           "the final development I work alongside your team, or with a partner I can bring in."],
    cap_lbl="02 — What I do",
    caps=[("Data strategy<br>&amp; data science",
           "What to measure and what to model, before the question of which tool to buy. Statistical "
           "modelling, data mining and machine learning on the data you already hold: forecasting, "
           "segmentation, experiments, and an intuitive reading of the result.",
           ["Statistical modelling", "Data mining", "Machine learning", "Forecasting", "Experiments", "Scientific data"]),
          ("AI <br>Adoption",
           "Driving adoption to the point where the organisation carries it on its own. The use "
           "cases that actually pay, "
           "the real cost of running them, who has to change how they work, what the AI Act obliges "
           "you to document. Certified in AI &amp; Law and AI Governance.",
           ["Use-case selection", "Pilot → production", "Governance", "EU AI Act", "Training", "Change"]),
          ("Marketing &amp; growth<br>operations",
           "The plumbing that makes a team autonomous: a tracking plan people follow, events and "
           "pipelines into one place, CRM and lifecycle flows that fire unsupervised, dashboards "
           "with a reporting cadence. One agreed definition of a conversion, and no more assembling "
           "Monday's numbers by hand.",
           ["Tracking plan", "GA4 · GTM", "Data pipelines", "CRM &amp; lifecycle", "Automation", "Dashboards"]),
          ("Advisory for<br>founders &amp; teams",
           "The hard calls, without a box on the org chart: is this feasible with the data and people "
           "you have, build or buy, which vendor, who to hire first. Where an existing tool already "
           "solves the problem, I say so rather than open a building site.",
           ["Feasibility", "Build vs buy", "Vendor selection", "Due diligence", "Hiring", "Retainer or equity"])],
    sect_lbl="03 — Where it applies",
    sect_h2="Any field with<br>data worth mining.",
    sect_p="Marketing and growth. Education. Operations and internal knowledge. Scientific and "
           "research data — signal processing, machine listening and experimental datasets are "
           "where I started, at IRCAM, and remain fully in scope.",
    sect_chips=["Marketing &amp; growth", "Policy &amp; regulation", "Education", "Operations", "Scientific research", "Media &amp; audio"],
    proj_lbl="04 — Selected projects",
    proj_more="View the full project index →",
    fig_lbl="05 — Omnichannel measurement",
    fig_h2="One model,<br>every platform.",
    fig_p1="I set up an omnichannel, multitouch measurement framework, with shared definitions and "
           "data flowing into a single model, instead of a thousand dashboards telling different "
           "stories.",
    fig_p2="Proprietary software produces editorial plans "
           "matched to what the sales funnel actually needs built: every piece of content and every "
           "euro answers to a specific stage, and measurement comes back on the same scheme.",
    fig_legend="planned weight per stage",
    fig_plan="editorial plan ↗",
    fig_note="Figure: illustrative structure — client figures withheld",
    speak_lbl="06 — Speaking &amp; teaching",
    speak_h2="Available for<br>conferences and lectures.",
    speak_p="I speak at public conferences, keynotes and panels, and teach university courses and "
            "in-house workshops, in English, Italian or French. The recurring subjects are AI adoption inside "
            "organisations, data strategy, and data-driven marketing — treated as operational "
            "problems with real examples, not as industry overviews.",
    speak_topics=["AI adoption in organisations", "Agents &amp; automation", "Governance and the AI Act",
                  "Data strategy &amp; science", "Data-driven marketing", "Decision models"],
    speak_rows=[("Apr — May 2026", "AI agents and AI tools for business productivity",
                 "A series of three seminars with the Milan Monza Brianza Lodi Chamber of Commerce, "
                 "Formaper and Microsoft. First date 4 May 2026, 15:00–18:00, Microsoft House, Viale "
                 "Pasubio 21, Milan: AI assistants and custom agents, prompt engineering for SMEs, "
                 "automation tooling, closing with a hands-on workshop. Free, limited seating.", "https://www.formaper.it/servizi-per-le-imprese/formazione-impresa-digitale/agenti-ai-produttivita-aziendale-evento-cciaa-microsoft/"),
                ("Since 2022", "Decisional Models for Data-Driven Marketing",
                 "Contract course, IULM — taught every academic year since 2022.", "https://iulm.coursecatalogue.cineca.it/corsi/2025/487/insegnamenti/2026/1992_22102_7871/2025/1992?schemaid=1499"),
                ("2025/26", "Statistics — first module",
                 "Università Cattolica, BSc in Business and Finance.", "https://www.unicatt.it/corsi/triennale/business-and-finance-brescia.html"),
                ("2025/26", "Artificial intelligence",
                 "Università Cattolica, master's in Communication for the Creative Industries, Milan.", "https://www.unicatt.it/corsi/master-universitari/milano/comunicazione-per-le-industrie-creative.html"),
                ("2025", "Statistics and AI",
                 "Milan Monza Brianza Lodi Chamber of Commerce — Data Analyst &amp; AI Explorer course."),
                ("2013 — 2017", "Machine learning for audio · digital signal processing",
                 "Visiting professor, Université de Franche-Comté / Conservatoire du Pays de "
                 "Montbéliard, France. Music technology and AI at the Conservatoire, focused on "
                 "machine learning for audio analysis. Four years."),
                ("Ongoing", "Executive workshops on AI adoption and governance",
                 "Private sessions for leadership teams, on request.")],
    speak_cta="Speaking and teaching enquiries →",
    eng_lbl="07 — Working together",
    engs=[("Set-up sprint", "Four to six weeks",
           "Instrument, connect, automate. At the end the team has one agreed set of numbers, the "
           "reports arrive on their own, and the first two or three automations are live and "
           "documented."),
          ("Embedded", "Days per month",
           "Working inside the team on a standing basis: keeping the stack honest, extending the "
           "automations, running the measurement cadence, and driving AI into workflows as the team "
           "becomes ready for it."),
          ("Advisory", "Monthly or equity",
           "Lighter-touch work for founders and leadership. Regular sessions where we revisit the "
           "decisions made, I check what vendors claim, and I cost the feasibility before the "
           "spending starts. Retainer or, early-stage, "
           "partly equity."),
          ("Technical collaboration", "Shape to be agreed",
           "For any project worth building. If the idea is interesting and there is room to do it "
           "properly, we find the form: collaboration between peers, research, a shared prototype, "
           "an open-source contribution. Tell me what you have in mind.")],
    cta_h2="Start with the report<br>nobody trusts.",
    cta_p="It is usually the fastest way in. The first conversation covers what the team measures "
          "today, where the manual work goes, and what could be automated or answered by AI within a "
          "month. If what you need is an agency or a development shop, I will say so.",
    cta_link="About, CV and contact →",
    foot_pages="Pages", foot_caps="What I do", foot_studio="Iside Systems SRLS",
    foot_sdi="e-invoicing code",
    foot_colophon="Iside Systems SRLS — VAT 14733480967",
    p_title="Projects — Iside Systems",
    p_desc="Project index: AI systems, analytics and growth, research and strategy. Iside Systems, Alessandro Saccoia.",
    p_kicker="Project index",
    p_h1="Experience in systems, measurement and decisions.",
    p_lede="Roles held, not projects sold. Each entry states the position — founder, CTO, head of "
           "function, research engineer — because what matters here is the range of problems "
           "addressed.",
    p_filters=[("all","All"),("ai","AI systems"),("analytics","Analytics &amp; growth"),
               ("product","Products &amp; open source"),("creative","Interactive &amp; audio"),
               ("research","Research"),("strategy","Strategy")],
    p_count="entries shown",
    p_note="Entries marked ↗ link to the project repository or its official page.",
    a_title="About &amp; contact — Iside Systems",
    a_desc="Alessandro Saccoia — data strategy, AI adoption, marketing and growth operations, teaching. CV and contact.",
    portrait_file="img/alessandro.jpg",
    portrait_alt="Alessandro Saccoia",
    portrait_cap="Alessandro Saccoia — Milan",
    a_kicker="About",
    a_h1="Iside Systems is the practice of Alessandro Saccoia.",
    privacy_link="Privacy policy",
    privacy_updated="Last updated",
    a_lede="Technologist, contract professor, co-founder. Years of experience in measurement, data, "
           "tooling and automation — across research institutes, ad-tech, telecoms, media "
           "measurement, and now my own companies.",
    a_p=["Iside Systems is how that work is sold: data strategy and science, AI adoption, and the "
         "marketing and growth operations that hold both together. Neither an agency nor a software "
         "house. I build and prototype what the operations layer needs, and when something outgrows "
         "that, it belongs with your team or a partner.",
         "Currently co-founder of Thembi, an EU policy intelligence platform; running marketing at "
         "Mentor Ripetizioni, where the infrastructure is built in-house; and contract professor at "
         "IULM."],
    a_cur="01 — Current", a_prev="02 — Previously", a_cred="03 — Education, credentials, teaching",
    a_speak="04 — Speaking &amp; teaching", a_contact="05 — Contact",
    a_cred_cards=[("Education", "Computer science, Università degli Studi di Milano."),
                  ("Certification", "AI and Law. AI Governance. AWS Certified Cloud Engineer. Training in transformative AI and AI safety."),
                  ("Teaching", "IULM — Decisional Models for Data-Driven Marketing, since 2022/23. "
                               "Università Cattolica — Statistics (Business and Finance) and "
                               "Artificial Intelligence (master's in Communication for the Creative "
                               "Industries, Milan). Université de Franche-Comté / Conservatoire du "
                               "Pays de Montbéliard — visiting professor 2013–2017. Milan Chamber of "
                               "Commerce and Formaper — AI for business."),
                  ("Languages", "Italian, English and French — lectures, conferences and materials in all "
                                "three. The French comes from four years teaching in France, at the "
                                "Université de Franche-Comté. Venues in Italy and abroad.")],
    a_contact_h2="Start with the problem,<br>not the technology.",
    a_contact_p="Useful first messages describe what the team measures today, where the manual work "
                "goes, and which decision keeps getting made on a feeling. One conversation is "
                "usually enough to say what is fixable within a month. If what you need is an agency "
                "or a development shop, I will tell you.",
    a_studio="Studio", a_direct="Direct",
    f_name="Name", f_email="Email", f_org="Organisation", f_topic="What is this about",
    f_msg="Message", f_send="Send enquiry",
    f_topics=["Data strategy &amp; science", "AI adoption", "Marketing &amp; growth operations",
              "Speaking or teaching", "Advisory", "Something else"],
    f_req="Name, email and message are required.",
    f_ok="Message sent. I will reply within a few days.",
    f_sending="Sending…",
    f_fallback="Direct sending unavailable. Opening your mail client with the message ready.",
    f_hp="Leave this field empty",
    f_done_title="Message sent.",
    f_done_lead="I will reply within a few days, usually sooner. If you want to add anything in the "
                "meantime, write directly to {mail}.",
    f_done_reply="I will reply to",
    f_done_again="Send another message",
    elsewhere="Elsewhere",
    cs_title="Case studies — Iside Systems",
    cs_desc="Three recent engagements: AI adoption inside the business units of a consulting firm, "
            "James — the marketing operations platform for an online education company — and "
            "putting a startup's infrastructure on solid ground.",
    cs_kicker="Case studies",
    cs_h1="My ways of getting data and AI inside an organisation.",
    cs_lede="Three recent engagements, one client each: the first starts from people and their "
            "processes, the second from measurement tooling, the third from the infrastructure "
            "holding everything else up.",
    mini_cta=["Something similar on your desk? Get in touch →",
              "If this is the piece you are missing, get in touch →",
              "First conversation, no commitment — get in touch →",
              "Wondering how it applies to you? Get in touch →"],
    cs_card_cta="Read the case",
    cs_home_lbl="04 — Case studies",
    cs_home_h2="Three different<br>ways in.",
    cs_home_p="Training that ends up inside the processes, measurement that holds the various platforms "
              "together, infrastructure that absorbs growth. Three recent engagements, told in "
              "full.",
    cs_home_more="All case studies →",
    cs_back="Back to case studies",
    cs_other="The other case studies",
    cs_fig_out="FUNNEL|PLAN|CALENDAR|SOV",
    cs_fig_src="META|TIKTOK|ADS SEARCH|ADS DISPLAY|CRM · EMAIL|REFERRAL",
    cs_cta_h2="Three different doors<br>into the same problem.",
    cs_cta_p="Three different ways in: people, measurement, infrastructure. The first step is "
             "working out which of the three matches the problem you have right now.",
    cs_cta_link="Get in touch →",
    cs_cases=[dict(
        slug="ai-adoption",
        n="01", lbl="AI adoption — consulting and training firm",
        card="A programme that starts in the room and ends inside the processes: progressive "
             "seminars to build the shared language, then workshops with each business unit to map "
             "the real "
             "work, find the low-hanging fruit, and design agents that respect the methods already "
             "in use.",
        h2="From the classroom<br>into the processes.",
        ctx=["AI was already inside the company, through the back door. Everyone used whatever "
             "tool they preferred, on their own terms, with no shared answer to the "
             "two questions that stop everybody — where does our data end up, and who is "
             "responsible for the output.",
             "The risks were organisational. Skills drifting apart, know-how leaving without "
             "anyone noticing, and usage staying at the level of personal curiosity instead of "
             "becoming organisational capability."],
        fig="training",
        steps=[("Foundations", "How the tools actually work",
                "A non-technical mental model: how models generate content, the difference between "
                "generation, search and knowledge, extracting data from documents and images, the "
                "role of context, and why they get things wrong."),
               ("Risk", "Informed use and risk",
                "What happens to the data: input, processing, output, where it lives. GDPR and the "
                "AI Act framed practically, protecting know-how, the risks of leakage and of "
                "misusing output."),
               ("Automation", "Productivity and automation",
                "From single task to process: recurring patterns, deterministic automation, an "
                "introduction to agents, and above all when to automate and when not to."),
               ("Workshops", "With each business unit",
                "This is where the programme stops being training and becomes analysis. Dedicated "
                "sessions with every business unit to understand how the work actually happens: "
                "which steps repeat, where time is lost, which controls are non-negotiable. The "
                "low-hanging fruit falls out of that — what can be improved immediately, without "
                "rewriting how people work."),
               ("Design", "Agents shaped around existing methods",
                "The agents come out of the mapping and follow the methods the organisation "
                "already has, instead of asking it to adapt to them. A tool built that way gets "
                "adopted; one that imposes its own gets worked around inside a month."),
               ("Over time", "Short recurring briefs",
                "Brief, regular pieces built on seminar feedback and on observed usage: summarising "
                "long documents, extracting structured data, deep research, regulatory updates.")],
        out="By the end people do the same things better and faster, and the organisation can do "
            "things it could not. The seminars build the "
            "shared language, "
            "the business-unit workshops find where to actually intervene, the agents consolidate "
            "the gain, and the recurring briefs stop the whole thing fading after a month.",
        chips=["Progressive seminars", "Workshops per business unit", "Process mapping",
               "Low-hanging fruit", "Agents on existing methods", "GDPR and the AI Act"]),
    dict(
        slug="james",
        n="02", lbl="James — marketing operations for an online education company",
        card="Meta, TikTok, Google Ads Search and Display, plus the CRM initiatives on the "
             "existing base: different platforms, different dashboards, no shared numbers. James holds "
             "ingestion, the funnel model, planning and measurement in one place: the editorial "
             "plan comes out of the funnel stages instead of being written separately.",
        date="10 August 2026",
        h2="Many marketing platforms,<br>one version<br>of the numbers.",
        ctx=["Meta, Google, the site, the CRM: every platform with its own dashboard and its own "
             "definition of a conversion. The editorial plan lived in one spreadsheet, the budget "
             "in another, and neither talked to actual spend.",
             "Rather than buy yet another tool I built James: a platform holding ingestion, the "
             "funnel model, planning and measurement together. It is client-independent and reusable "
             "by design."],
        fig="james",
        steps=[("Ingestion", "One warehouse",
                "Data arrives from the ad and analytics platforms and is collected in one place, "
                "deduplicated by natural key, so repeated syncs do not create duplicates."),
               ("Model", "Configurable funnel",
                "Stages and KPIs are defined from the interface: source metric, aggregation, ratios "
                "between metrics, multipliers, entity level. Each stage can be tied to the real "
                "campaigns."),
               ("Planning", "Plan against spend",
                "Budget plans break the period down by line, as a percentage or an amount, and the "
                "comparison with real spend is automatic. Lines that are operational effort rather "
                "than media budget stay out of the totals."),
               ("Execution", "Calendar and cadence",
                "Every channel carries an expected cadence — minimum and maximum outputs per "
                "period — and a declared role in the funnel. Calendar items carry channel, owner, "
                "linked campaign and a link to the published post."),
               ("Channels", "Paid, search and social",
                "The model covers the whole mix: Meta, TikTok, Google Ads Search and Google Ads "
                "Display. Each channel comes in with its own spend and its own role in the funnel "
                "— search captures existing demand, display and social build it — and is measured "
                "with the same definitions as the others."),
               ("Installed base", "CRM, email and referral",
                "Alongside acquisition sit the initiatives on the existing customer base: email "
                "campaigns to win back inactive customers, and referral programmes. They live in "
                "the same model as paid, so a channel's cost per acquisition can be compared with "
                "the cost of a reactivation instead of sitting in a separate spreadsheet."),
               ("Context", "Tags, events, competition",
                "A multi-dimensional taxonomy with expected shares per dimension, events annotated "
                "directly on the charts, and monthly competitor traffic imported to compare your "
                "own share against the market's.")],
        out="Planning and measurement now use the same model. The editorial plan comes out of "
            "the funnel stages instead of being "
            "written separately, and at month end “what did we spend it on” has a single answer.",
        chips=["Meta", "TikTok", "Google Ads Search", "Google Ads Display", "CRM &amp; email",
               "Referral", "Configurable funnel", "Plan vs spend", "Editorial calendar",
               "Share of voice"]),
    dict(
        slug="cloud-scale",
        n="03", lbl="Infrastructure and governance — education startup",
        date="2026",
        card="A platform that worked, grown faster than the environment hosting it. Migration onto "
             "infrastructure that absorbs growth, a controlled development process, and an "
             "assessment covering data, the AI Act and terms of use.",
        h2="Making what<br>already works<br>hold up.",
        ctx=["The product was there and had been built pragmatically: a live platform, real "
             "users, AI features already in production. What did not hold was the environment "
             "underneath — designed to launch, not to absorb growing traffic and concurrent users.",
             "The risk in these situations arrives later than today's outage. It shows up when "
             "every increase in usage forces a redesign, while nobody can say where the data goes "
             "or on what terms the service is provided."],
        fig="cloud",
        steps=[("Infrastructure", "Migration onto something that scales",
                "Exporting the platform from its existing environment and configuring application, "
                "database, access, backups and deployment properly. The goal is absorbing "
                "growth without redesigning the system at every jump in usage."),
               ("Observability", "Monitoring from day one",
                "Monitoring set up before the first incident. Knowing how the system is doing is "
                "as much part of the infrastructure as the servers."),
               ("Process", "Faster development, better controlled",
                "Organising the environment and the development process — repository, review, "
                "coding assistants — to move faster along a documented, traceable path."),
               ("Assessment", "Data, AI and external vendors",
                "A technical and organisational review of the AI features and data flows: what "
                "leaves the perimeter, towards which providers, and what that implies for GDPR, "
                "the AI Act and security."),
               ("Terms", "Conditions of use and licensing",
                "Terms of use and licensing follow from the assessment, matching how the platform "
                "actually works. Ordinary matters are handled in-house; legal review is kept for "
                "the questions that deserve it.")],
        out="From outside nothing shows. No new features, no redesign. What changes is the "
            "trajectory — the platform can grow without being rebuilt, the team "
            "ships faster with more control, and the questions about data and terms have a written "
            "answer before anyone turns up to ask them.",
        chips=["Cloud migration", "Backups and deployment", "Monitoring", "Development process",
               "GDPR and the AI Act", "Terms of use"])],
    cookie_title="Cookies.",
    cookie_text="This site uses measurement cookies to see which pages get read. No advertising, no "
                "profiling sold on to anyone. If you refuse, the site works exactly the same.",
    cookie_accept="Accept",
    cookie_reject="Refuse",
)

# ---------------------------------------------------------------- lab pages
# Small dedicated pages for the two instruments, linked only from the project
# index. Kept out of the nav and the sitemap on purpose.
LABS = {
"moire": dict(
    shot="img/moire.jpg", demo="lab/moire/index.html",
    it=dict(kicker="Lab", title="Moire",
        lede="Generatore di pattern moiré con sintesi audio-video sincronizzata. Le figure che "
             "vedete e quello che sentite sono guidati dagli stessi parametri.",
        body=["Quattro famiglie di pattern — linee, griglia, cerchi, radiale — sovrapposte con uno "
              "sfasamento d'angolo regolabile, da cui nasce l'interferenza moiré. Densità, "
              "angolo, scala e velocità si controllano in tempo reale.",
              "La parte audio è una sintesi FM agganciata agli stessi controlli, quindi cambiare la "
              "densità visiva sposta il timbro. Non è una sonificazione aggiunta dopo, i due "
              "motori condividono lo stato."],
        cols=[("Interazione", ["Pattern: linee, griglia, cerchi, radiale", "Densità e sfasamento angolare",
                               "Scala e velocità", "Tutto in tempo reale"]),
              ("Tecnica", ["Canvas 2D", "Web Audio API, sintesi FM", "Moduli ES, nessuna dipendenza",
                           "Gira interamente nel browser"])],
        cta="Apri lo strumento", note="Meglio con l'audio acceso. Su mobile serve un tocco per avviare il suono.",
        back="Torna ai progetti"),
    en=dict(kicker="Lab", title="Moire",
        lede="A moiré pattern generator with synchronised audio-visual synthesis. What you see and "
             "what you hear are driven by the same parameters.",
        body=["Four pattern families — lines, grid, circles, radial — overlaid with an adjustable "
              "angular offset, which is where the moiré interference comes from. Density, angle, "
              "scale and speed are all live controls.",
              "The audio side is FM synthesis wired to those same controls, so changing the visual "
              "density moves the timbre. It is not sonification bolted on afterwards, since both "
              "engines share one state."],
        cols=[("Interaction", ["Patterns: lines, grid, circles, radial", "Density and angular offset",
                               "Scale and speed", "Everything live"]),
              ("Technical", ["Canvas 2D", "Web Audio API, FM synthesis", "ES modules, no dependencies",
                             "Runs entirely in the browser"])],
        cta="Open the instrument", note="Better with sound on. Mobile needs one tap to start audio.",
        back="Back to projects")),
"algosynth": dict(
    shot="img/algosynth.jpg", demo={"it": "/algosynth", "en": "/algosynth/en"},
    it=dict(kicker="Lab", title="AlgoSynth",
        lede="Sequencer algoritmico ispirato ad Acroyear degli Autechre. I pattern non si "
             "disegnano nota per nota, si generano e poi si piegano.",
        body=["Generazione di pattern ritmici e melodici con controllo dello swing, song mode "
              "multitraccia e uscita MIDI via Web MIDI verso qualunque strumento collegato.",
              "L'idea presa da Acroyear è che il materiale nasca da regole invece che dalla mano. "
              "Si imposta un processo, lo si ascolta, si interviene sui parametri mentre suona."],
        cols=[("Interazione", ["Generazione algoritmica dei pattern", "Controllo dello swing",
                               "Song mode multitraccia", "Parametri modificabili durante l'esecuzione"]),
              ("Tecnica", ["Web MIDI API", "Uscita verso hardware esterno", "Interamente nel browser"])],
        cta="Apri lo strumento", note="Solo desktop, larghezza minima 900 px. Serve un tap su Play "
        "per far partire l'audio.",
        back="Torna ai progetti"),
    en=dict(kicker="Lab", title="AlgoSynth",
        lede="An algorithmic sequencer inspired by Autechre's Acroyear. Patterns are not drawn note "
             "by note, they are generated and then bent.",
        body=["Rhythmic and melodic pattern generation with swing control, multi-track song mode, "
              "and MIDI output over Web MIDI to any connected instrument.",
              "The idea taken from Acroyear is that the material comes from rules rather than the "
              "hand. You set a process running, listen, and work the parameters while it plays."],
        cols=[("Interaction", ["Algorithmic pattern generation", "Swing control", "Multi-track song mode",
                               "Parameters editable while playing"]),
              ("Technical", ["Web MIDI API", "Output to external hardware", "Entirely in the browser"])],
        cta="Open the instrument", note="Desktop only, minimum width 900 px. One tap on Play starts "
        "the audio.",
        back="Back to projects")),
}


# ---------------------------------------------------------------- helpers
def chips(items):
    return "".join(f'<span class="chip">{i}</span>' for i in items)

SITE = "https://www.isidesystems.com"          # cambia qui se cambia il dominio
GTM  = "GTM-584NQHC3"
# no trailing slash: vercel.json sets trailingSlash false, so "/en/" answers 308
PATHS = {"home":      ("", "en"),
         "cases":     ("case-study.html", "en/case-studies.html"),
         "case-ai-adoption": ("case-ai-adoption.html", "en/case-ai-adoption.html"),
         "case-james":       ("case-james.html", "en/case-james.html"),
         "case-cloud-scale": ("case-cloud-scale.html", "en/case-cloud-scale.html"),
         "projects":  ("progetti.html", "en/projects.html"),
         "about":     ("chi-sono.html", "en/about.html"),
         "moire":     ("moire.html", "en/moire.html"),
         "algosynth": ("algosynth.html", "en/algosynth.html"),
         "privacy":   ("privacy.html", "en/privacy.html"),
         "blog":      ("blog", "en/blog"),
         "metodo":    ("metodologia.html", "en/methodology.html")}
for _post_it, _post_en in zip(B.published(), B.published("en")):
    _paths = (f"blog/{_post_it['slug']}", f"en/blog/{_post_en['slug']}")
    PATHS[f"post-{_post_it['slug']}"] = _paths
    PATHS[f"post-{_post_en['slug']}"] = _paths


def head(L, title, desc, asset, alt_href, self_page, og_image=None):
    it_path, en_path = PATHS[self_page]
    lang = L["lang"]
    url = SITE + "/" + (it_path if lang == "it" else en_path)
    og_locale = "it_IT" if lang == "it" else "en_GB"
    og_alt = "en_GB" if lang == "it" else "it_IT"
    img = SITE + (og_image or "/assets/img/og-image.png")
    person = ("Alessandro Saccoia — strategia dei dati, AI Adoption, operations di marketing"
              if lang == "it" else
              "Alessandro Saccoia — data strategy, AI adoption, marketing operations")
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<!-- Consent Mode: everything denied until the visitor says otherwise -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
var _c="denied",_g="granted";
try{{
  var _v=localStorage.getItem("iside-consent");
  if(_v==="granted")_c="granted";
  if(_v==="denied")_g="denied";      // a refusal travels with the visitor everywhere
}}catch(e){{}}
// Where consent is legally required, everything waits for the banner. Elsewhere
// the default is granted — otherwise every region reports a 0% consent rate.
var _eea=['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT',
 'LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH'];
gtag('consent','default',{{
  ad_storage:_c, ad_user_data:_c, ad_personalization:_c, analytics_storage:_c,
  functionality_storage:'granted', security_storage:'granted', wait_for_update:500,
  region:_eea
}});
gtag('consent','default',{{
  ad_storage:_g, ad_user_data:_g, ad_personalization:_g, analytics_storage:_g,
  functionality_storage:'granted', security_storage:'granted'
}});
</script>

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM}');</script>
<!-- End Google Tag Manager -->

<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Alessandro Saccoia">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="alternate" type="application/rss+xml" title="Iside Systems — Blog" href="{SITE}/feed.xml">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="it" href="{SITE}/{it_path}">
<link rel="alternate" hreflang="en" href="{SITE}/{en_path}">
<link rel="alternate" hreflang="x-default" href="{SITE}/">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Iside Systems">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_alt}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:secure_url" content="{img}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Iside Systems — {person}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<meta name="twitter:image:alt" content="Iside Systems — {person}">

<link rel="icon" href="{asset}img/mark.svg" type="image/svg+xml">
<link rel="icon" href="{asset}img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{asset}img/apple-touch-icon.png">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#0e0e11">

<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"ProfessionalService","@id":"{SITE}/#studio","name":"Iside Systems SRLS",
 "url":"{SITE}/","email":"alessandro@iside.systems","vatID":"IT14733480967",
 "image":"{img}","description":"{desc}",
 "address":{{"@type":"PostalAddress","streetAddress":"Via Tortona 12","postalCode":"20144",
   "addressLocality":"Milano","addressCountry":"IT"}},
 "areaServed":"Europe","founder":{{"@id":"{SITE}/#alessandro"}},
 "knowsLanguage":["it","en","fr"]}},
{{"@type":"Person","@id":"{SITE}/#alessandro","name":"Alessandro Saccoia",
 "jobTitle":"Data strategy, AI adoption, marketing and growth operations",
 "email":"alessandro@iside.systems","worksFor":{{"@id":"{SITE}/#studio"}},
 "knowsLanguage":["it","en","fr"],
 "address":{{"@type":"PostalAddress","addressLocality":"Milano","addressCountry":"IT"}},
 "alumniOf":"Universita degli Studi di Milano",
 "sameAs":["https://www.alessandrosaccoia.com/","https://github.com/alesaccoia",
   "https://www.linkedin.com/in/alesaccoia/"]}},
{{"@type":"WebSite","@id":"{SITE}/#site","url":"{SITE}/","name":"Iside Systems",
 "inLanguage":"{lang}","publisher":{{"@id":"{SITE}/#studio"}}}}
]}}
</script>

<script>document.documentElement.classList.add("js");try{{document.documentElement.setAttribute("data-theme",localStorage.getItem("iside-theme")||"dark")}}catch(e){{document.documentElement.setAttribute("data-theme","dark")}}</script>
<link rel="stylesheet" href="{asset}site.css">
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""


def header(L, asset, home, projects, about, current, alt_href, cases="case-study.html"):
    # /blog and /blog/<slug> are served without a trailing slash, so relative
    # links there resolve against the root: those pages ask for absolute paths
    if asset.startswith("/"):
        blog_href = "/en/blog" if L["lang"] == "en" else "/blog"
        metodo_href = "/en/methodology.html" if L["lang"] == "en" else "/metodologia.html"
    else:
        depth = asset.count("../")
        blog_href = ("../" * depth) + "blog" if depth else "blog"
        metodo_href = ("methodology.html" if L["lang"] == "en"
                       else ("../" * depth) + "metodologia.html")
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    n = L["nav"]
    return f"""<header class="site">
  <div class="navrow">
    <a class="brand" href="{home}">
      <span class="glyph"></span>
      <span><b>Iside Systems</b><span>{L['brand_sub']}</span></span>
    </a>
    <button id="navToggle" type="button" aria-expanded="false" aria-controls="mainnav"
            aria-label="{L['nav_open']}"><span></span><span></span><span></span></button>
    <nav class="main" id="mainnav">
      {a(home, n[0], 'home')}
      {a(cases, n[3], 'cases')}
      {a(metodo_href, n[5], 'metodo')}
      {a(projects, n[1], 'projects')}
      {a(blog_href, n[4], 'blog')}
      {a(about, n[2], 'about')}
      <span class="langsw"><a href="#" aria-current="true">{L['lang'].upper()}</a>/<a href="{alt_href}">{L['other_label']}</a></span>
      <button id="themeBtn" type="button">Dark</button>
    </nav>
  </div>
  <div id="navScrim" hidden></div>
</header>
"""

def newsbar(L, about):
    items = ""
    for entry in L["news"]:
        w, t = entry[0], entry[1]
        # entries with their own link are already relative to the current folder
        href = entry[2] if len(entry) > 2 else f"{about}#speaking"
        items += f'<span class="item"><time>{w}</time><a href="{href}">{t}</a></span>' 
    return f'<div class="newsbar"><span class="tag">{L["news_label"]}</span>{items}</div>\n'

def footer(L, home, projects, about, asset):
    # privacy.html resolves inside the current folder, so the English pages
    # reach en/privacy.html and the Italian ones the root file — except where
    # the page is served without a trailing slash and needs absolute paths
    privacy_href = "privacy.html"
    cases_href = "case-study.html" if L["lang"] == "it" else "case-studies.html"
    if asset.startswith("/"):
        privacy_href = "/en/privacy.html" if L["lang"] == "en" else "/privacy.html"
        cases_href = "/case-study.html" if L["lang"] == "it" else "/en/case-studies.html"
    n = L["nav"]
    caps = [c[0].replace("<br>", " ") for c in L["caps"]]
    caplinks = "".join(f'<a href="{home}#capabilities">{c}</a>' for c in caps)
    return f"""<footer class="site">
  <div class="col">
    <b>{L['foot_studio']}</b>
    <span>Via Tortona 12<br>20144 Milano</span>
    <a href="mailto:alessandro@iside.systems">alessandro@iside.systems</a>
    <a href="mailto:iside.systems.srls@pec.it">iside.systems.srls@pec.it</a>
    <a href="https://www.linkedin.com/in/alesaccoia/" rel="me noopener" target="_blank">LinkedIn</a>
    <span>P.IVA 14733480967</span>
    <span>{L['foot_sdi']} KRRH6B9</span>
  </div>
  <div class="col">
    <b>{L['foot_pages']}</b>
    <a href="{home}">{n[0]}</a>
    <a href="{projects}">{n[1]}</a>
    <a href="{about}">{n[2]}</a>
    <a href="{cases_href}">{n[3]}</a>
  </div>
  <div class="col">
    <b>{L['foot_caps']}</b>
    {caplinks}
  </div>
  <div class="colophon">
    <span>{L['foot_colophon']}</span>
    <a href="{privacy_href}">{L['privacy_link']}</a>
    <span>IT · EN · FR</span>
  </div>
</footer>

<div id="cookiebar" hidden>
  <p><b>{L['cookie_title']}</b> {L['cookie_text']}</p>
  <div class="acts">
    <button type="button" data-consent="denied">{L['cookie_reject']}</button>
    <button type="button" data-consent="granted" class="primary">{L['cookie_accept']}</button>
  </div>
</div>

<script src="{asset}site.js"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- pages
def page_home(L, asset, home, projects, about, alt_href, cases="case-study.html"):
    # the English home sits one level down, so root-level pages need the hop
    root = "../" if asset.startswith("../") else ""
    metodo_href = "methodology.html" if L["lang"] == "en" else "metodologia.html"
    blog_band = ""
    blog_rows = "".join(
        f'<a class="bpost" href="{root}blog/{p["slug"]}">'
        f'<span class="d">{p["human_date"]}</span>'
        f'<span class="t">{p["title"]}</span>'
        f'<span class="k">{p["tags"][0]}</span>'
        f'<span class="go">\u2192</span></a>' for p in B.published()[:3])
    if blog_rows:
        # with nothing published the band would be a heading over a void
        blog_band = f"""
<section class="pad rule blogband" style="padding-top:clamp(50px,8vh,96px);padding-bottom:clamp(50px,8vh,96px)">
  <div class="lbl">{L['blog_lbl']}</div>
  <div class="cols2" style="align-items:end">
    <div class="rv"><h2>{L['blog_h2']}</h2></div>
    <div class="rv"><p style="margin-top:20px"><a class="ambtn" href="{root}blog">{L['blog_more']}<span class="go">\u2192</span></a></p></div>
  </div>
  <div class="bposts rv">{blog_rows}</div>
</section>
"""
    caps_html = ""
    for i, (h3, body, tags) in enumerate(L["caps"], 1):
        caps_html += f"""
  <article class="cap rv">
    <div class="n">/0{i}</div>
    <div><h3>{h3}</h3></div>
    <div>
      <p>{body}</p>
    </div>
  </article>
"""
    tiles = ""
    for pr in [x for x in PROJECTS if x.get("featured")][:3]:
        name, role, body, tags = pr[L["lang"]]
        tiles += f"""    <div class="tile">
      <canvas class="thumb" data-seed="{pr['seed']}"></canvas>
      <div class="top"><h4>{name}</h4><span class="meta">{pr['year']}</span></div>
      <p>{body}</p>
      <div class="tags">{chips(tags)}</div>
    </div>
"""
    engs = "".join(f"""    <div class="tile">
      <div class="top"><h4>{t}</h4><span class="meta">{w}</span></div>
      <p>{b}</p>
    </div>
""" for t, w, b in L["engs"])

    speak_rows = ""
    for row in L["speak_rows"]:
        w, t, d = row[0], row[1], row[2]
        u = row[3] if len(row) > 3 else None
        title = f'<a href="{u}" target="_blank" rel="noopener">{t} <span class="ext">↗</span></a>' if u else t
        speak_rows += f"""    <div class="speakrow"><div class="when">{w}</div>
      <div><b>{title}</b><i>{d}</i></div></div>
"""

    pos_ps = ""
    for i, para in enumerate(L["pos_p"]):
        style = ' style="margin-top:1.2em"' if i else ''
        pos_ps += '<p class="dim"%s>%s</p>' % (style, para)

    return (head(L, L["title"], L["desc"], asset, alt_href, "home")
            + header(L, asset, home, projects, about, "home", alt_href, cases)
            + f"""<a class="amstrip" href="/ai-maturity">
  <span class="tag">{L['am_lbl']}</span>
  <span class="say">{L['am_h2']}</span>
  <span class="sub">{L['am_p']}</span>
  <span class="go">{L['am_cta']} →</span>
</a>

<section class="hero">
  <div class="inner">
    <div>
      <h1 style="margin-top:18px">{L['h1']}</h1>
      <p class="lede sub dim">{L['lede']}</p>
    </div>
    <div class="figwrap"><canvas id="figure"></canvas></div>
  </div>
</section>
"""
            + newsbar(L, about)
            + f"""

<section class="pad" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['pos_lbl']}</div>
  <div class="cols2">
    <div class="rv"><h2>{L['pos_h2']}</h2></div>
    <div class="rv">{pos_ps}</div>
  </div>
  {mini_cta(L, about, 0)}
</section>

<section class="mband rv">
  <div class="inner">
    <div>
      <div class="lbl">{L['m_lbl']}</div>
      <h2>{L['m_h2']}</h2>
    </div>
    <div>
      <p>{L['m_p']}</p>
      <div class="steps">{"".join(f"<span>{x}</span>" for x in L["m_steps"])}</div>
      <p style="margin-top:24px"><a class="ambtn" href="{metodo_href}">{L['m_cta']}<span class="go">\u2192</span></a></p>
    </div>
  </div>
</section>

<section class="caps rule" id="capabilities">
  <div class="lbl">{L['cap_lbl']}</div>
{caps_html}  {mini_cta(L, about, 1)}
</section>

<section class="pad rule" style="padding-top:clamp(50px,8vh,90px);padding-bottom:clamp(50px,8vh,90px)">
  <div class="lbl">{L['sect_lbl']}</div>
  <div class="cols2">
    <div class="rv"><h2>{L['sect_h2']}</h2></div>
    <div class="rv">
      <p class="dim">{L['sect_p']}</p>
    </div>
  </div>
</section>

<section class="pad rule" id="cases" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['cs_home_lbl']}</div>
  <div class="cols2" style="align-items:end">
    <div class="rv"><h2>{L['cs_home_h2']}</h2></div>
    <div class="rv"><p class="dim">{L['cs_home_p']}</p></div>
  </div>
  <div class="csrows rv">{case_rows(L)}</div>
  <p style="margin-top:26px"><a class="meta" href="{cases}" style="color:var(--acc);text-decoration:none">{L['cs_home_more']}</a></p>
</section>
{blog_band}
<section class="pad rule" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['proj_lbl']}</div>
  <div class="grid3 rv" data-cols="3">
{tiles}  </div>
  <p style="margin-top:26px"><a class="meta" href="{projects}" style="color:var(--acc);text-decoration:none">{L['proj_more']}</a></p>
</section>

<section class="pad rule" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['fig_lbl']}</div>
  <div class="cols2" style="align-items:start">
    <div class="rv">
      <h2>{L['fig_h2']}</h2>
      <p class="dim" style="margin-top:20px">{L['fig_p1']}</p>
      <p class="dim" style="margin-top:1.2em">{L['fig_p2']}</p>
      <p class="meta" style="margin-top:20px">{L['fig_note']}</p>
    </div>
    <div class="figbox rv"><canvas class="fig" id="matrix" data-legend="{L['fig_legend']}" data-plan="{L['fig_plan']}"></canvas></div>
  </div>
  {mini_cta(L, about, 3)}
</section>

<section class="pad rule" id="speaking" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['speak_lbl']}</div>
  <div class="cols2" style="align-items:start">
    <div class="rv">
      <h2>{L['speak_h2']}</h2>
      <p class="dim" style="margin-top:20px">{L['speak_p']}</p>
      <div class="facts" style="margin-top:22px">{chips(L['speak_topics'])}</div>
      <p style="margin-top:26px"><a class="meta" href="{about}#contact" style="color:var(--acc);text-decoration:none">{L['speak_cta']}</a></p>
    </div>
    <div class="rv"><div class="speaklist">
{speak_rows}    </div></div>
  </div>
</section>

<section class="pad rule" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(56px,9vh,110px)">
  <div class="lbl">{L['eng_lbl']}</div>
  <div class="grid3 rv" data-cols="4">
{engs}  </div>
</section>

<section class="pad rule" style="padding-top:clamp(60px,10vh,120px);padding-bottom:clamp(60px,10vh,120px)">
  <h2 class="rv">{L['cta_h2']}</h2>
  <p class="lede dim rv" style="margin-top:22px">{L['cta_p']}</p>
  <p style="margin-top:30px"><a class="meta" href="{about}" style="color:var(--acc);text-decoration:none">{L['cta_link']}</a></p>
</section>

""" + footer(L, home, projects, about, asset))


def page_projects(L, asset, home, projects, about, alt_href, cases="case-study.html"):
    fl = "".join(f'<button class="chip" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>'
                 for k, v in L["p_filters"])
    tiles = ""
    for pr in PROJECTS:
        name, role, body, tags = pr[L["lang"]]
        url = pr.get("url")
        internal = isinstance(url, dict)
        if internal:
            url = url[L["lang"]]
        tag = "a" if url else "div"
        attrs = (f' href="{url}"' if internal
                 else f' href="{url}" target="_blank" rel="noopener"') if url else ""
        arrow = "" if internal or not url else ' <span class="ext">↗</span>'
        arrow = ' <span class="ext">→</span>' if internal else arrow
        tiles += f"""    <{tag} class="tile" data-cat="{pr['cat']}"{attrs}>
      <canvas class="thumb" data-seed="{pr['seed']}"></canvas>
      <div class="top"><h4>{name}{arrow}</h4><span class="meta">{pr['year']}</span></div>
      <p class="meta">{role}</p>
      <p>{body}</p>
      <div class="tags">{chips(tags)}</div>
    </{tag}>
"""
    return (head(L, L["p_title"], L["p_desc"], asset, alt_href, "projects")
            + header(L, asset, home, projects, about, "projects", alt_href, cases)
            + newsbar(L, about)
            + f"""
<section class="pad" style="padding-top:clamp(46px,7vh,90px);padding-bottom:clamp(30px,5vh,54px)">
  <p class="meta">{L['p_kicker']}</p>
  <h1 style="margin-top:16px;max-width:18ch">{L['p_h1']}</h1>
  <p class="lede dim" style="margin-top:22px">{L['p_lede']}</p>
</section>

<section class="pad" style="padding-bottom:clamp(60px,10vh,120px)">
  <div class="filters">{fl}</div>
  <p class="meta" style="margin-bottom:22px"><span id="pcount">00</span> {L['p_count']}</p>
  <div class="grid3">
{tiles}  </div>
  <p class="meta" style="margin-top:30px">{L['p_note']}</p>
  {mini_cta(L, about, 1)}
</section>

""" + footer(L, home, projects, about, asset))


def page_about(L, asset, home, projects, about, alt_href, cases="case-study.html"):
    cur = [("02/2025 →", "Iside Systems SRLS",
            "Fondatore. Strategia dei dati, AI Adoption, operations di marketing e crescita, advisory."
            if L["lang"] == "it" else
            "Founder. Data strategy, AI adoption, marketing and growth operations, advisory."),
           ("10/2024 →", "Thembi",
            "Co-fondatore. Piattaforma di policy intelligence europea — prodotto, backend, sistemi AI."
            if L["lang"] == "it" else
            "Co-founder. EU policy intelligence platform — product, backend and AI systems."),
           ("2026 →", "Mentor Ripetizioni",
            "Responsabile marketing. Modello di crescita, infrastruttura interna, tutor AI."
            if L["lang"] == "it" else
            "Head of marketing. Growth model, in-house infrastructure, AI tutor."),
           ("2022/23 →", "IULM",
            "Professore a contratto — Modelli decisionali per il marketing data-driven, master in AI for Business and Society."
            if L["lang"] == "it" else
            "Contract professor — Decisional Models for Data-Driven Marketing, master's in AI for Business and Society.")]
    it = L["lang"] == "it"
    prev = [("05/2023 — 11/2024", "IULM AI Lab, Milano" if it else "IULM AI Lab, Milan",
             "Chief technology officer."),
            ("04/2022 — 04/2023", "Nielsen, Milano" if it else "Nielsen, Milan",
             "Senior manager, marketing effectiveness. Performance measurement e marketing "
             "effectiveness per Sud Europa ed EMEA." if it else
             "Senior manager, marketing effectiveness. Performance measurement and marketing "
             "effectiveness across Southern Europe and EMEA."),
            ("01/2021 — 04/2022", "Vodafone Business, Milano" if it else "Vodafone Business, Milan",
             "Product manager di Vodafone Analytics, il prodotto di analisi territoriale e martech "
             "costruito sui big data telco: design, raccolta dei requisiti e gestione operativa dei "
             "clienti in esercizio." if it else
             "Product manager of Vodafone Analytics, their territorial-analysis and martech product "
             "built on telco big data: design, requirement gathering and operations management for "
             "in-life clients."),
            ("10/2018 — 11/2020", "Beintoo, Milano" if it else "Beintoo, Milan",
             "Head of data science. Ricerca su business intelligence e trasformazione digitale "
             "omnichannel; analytics avanzata e big data per ad-tech e market intelligence." if it else
             "Head of data science. Research in business intelligence and omni-channel digital "
             "transformation; advanced analytics and big-data tooling for ad-tech and market "
             "intelligence."),
            ("05/2017 — 05/2018", "Mogees Ltd, Londra" if it else "Mogees Ltd, London",
             "Project manager, data science. Analisi audio, elaborazione statistica del segnale e "
             "machine learning; prototipazione rapida di app mobile, tool a riga di comando e "
             "software embedded." if it else
             "Project manager, data science. Audio analysis, statistical signal processing and "
             "machine learning; rapid prototyping of mobile apps, command-line tools and embedded "
             "software."),
            ("04/2012 — 05/2016", "Dinahmoe AB, Stoccolma" if it else "Dinahmoe AB, Stockholm",
             "Direttore tecnico. Esperienze audio interattive premiate per HBO, Nike e Google; più "
             "FWA Awards, con agenzie come BBH, Stink Digital e Acne Production." if it else
             "Technical director. Award-winning interactive audio experiences for HBO, Nike and "
             "Google; multiple FWA Awards, with agencies including BBH, Stink Digital and Acne "
             "Production."),
            ("06/2010 — 11/2011", "IRCAM, Parigi" if it else "IRCAM, Paris",
             "Machine learning engineer nel gruppo Analysis/Synthesis: music information retrieval "
             "e descrittori audio." if it else
             "Machine learning engineer in the Analysis/Synthesis group: music information retrieval "
             "and audio descriptors."),
            ("10/2009 — 05/2010", "IK Multimedia",
             "DSP engineer. Sviluppo C++ sulla linea di plugin audio." if it else
             "DSP engineer. C++ development across the company's audio plugin range."),
            ("10/2007 — 09/2009", "Softailor",
             "Web developer. Sviluppo web e software gestionale." if it else
             "Web developer. Web development and corporate software.")]

    def rows(items):
        return "".join(f"""    <div class="cvrow"><div class="yr">{y}</div>
      <div><b>{n}</b><i>{d}</i></div></div>
""" for y, n, d in items)

    cred = "".join(f"""    <div class="tile"><div class="top"><h4>{t}</h4></div><p>{b}</p></div>
""" for t, b in L["a_cred_cards"])

    speak_rows = ""
    for row in L["speak_rows"]:
        w, t, d = row[0], row[1], row[2]
        u = row[3] if len(row) > 3 else None
        title = f'<a href="{u}" target="_blank" rel="noopener">{t} <span class="ext">↗</span></a>' if u else t
        speak_rows += f"""    <div class="speakrow"><div class="when">{w}</div>
      <div><b>{title}</b><i>{d}</i></div></div>
"""

    opts = "".join(f"          <option>{o}</option>\n" for o in L["f_topics"])

    return (head(L, L["a_title"], L["a_desc"], asset, alt_href, "about")
            + header(L, asset, home, projects, about, "about", alt_href, cases)
            + newsbar(L, about)
            + f"""
<section class="pad" style="padding-top:clamp(46px,7vh,90px);padding-bottom:clamp(46px,8vh,90px)">
  <p class="meta">{L['a_kicker']}</p>
  <h1 style="margin-top:16px;max-width:17ch">{L['a_h1']}</h1>
  <div class="aboutintro rv">
    <figure class="portrait">
      <img src="{asset}{L['portrait_file']}" alt="{L['portrait_alt']}" width="426" height="640" loading="lazy">
      <figcaption class="meta">{L['portrait_cap']}</figcaption>
    </figure>
    <div class="abouttext">
      <p class="lede">{L['a_lede']}</p>
      <p class="dim">{L['a_p'][0]}</p>
      <p class="dim">{L['a_p'][1]}</p>
    </div>
  </div>
</section>

<section class="pad rule" style="padding-top:clamp(50px,8vh,90px)">
  <div class="lbl">{L['a_cur']}</div>
  <div class="cv rv">
{rows(cur)}  </div>
</section>

<section class="pad" style="padding-top:clamp(50px,8vh,90px)">
  <div class="lbl">{L['a_prev']}</div>
  <div class="cv rv">
{rows(prev)}  </div>
</section>

<section class="pad" style="padding-top:clamp(50px,8vh,90px);padding-bottom:clamp(50px,8vh,90px)">
  <div class="lbl">{L['a_cred']}</div>
  <div class="grid3 rv" data-cols="4">
{cred}  </div>
</section>

<section class="pad rule" id="speaking" style="padding-top:clamp(50px,8vh,90px);padding-bottom:clamp(50px,8vh,90px)">
  <div class="lbl">{L['a_speak']}</div>
  <div class="cols2" style="align-items:start">
    <div class="rv">
      <h2>{L['speak_h2']}</h2>
      <p class="dim" style="margin-top:20px">{L['speak_p']}</p>
      <div class="facts" style="margin-top:22px">{chips(L['speak_topics'])}</div>
    </div>
    <div class="rv"><div class="speaklist">
{speak_rows}    </div></div>
  </div>
</section>

<section class="pad rule" id="contact" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(60px,10vh,120px)">
  <div class="lbl">{L['a_contact']}</div>
  <div class="cols2" style="align-items:start">
    <div class="rv">
      <h2>{L['a_contact_h2']}</h2>
      <p class="dim" style="margin-top:20px">{L['a_contact_p']}</p>
      <div style="margin-top:30px">
        <p class="meta">{L['a_studio']}</p>
        <p style="margin-top:6px">Iside Systems SRLS<br>Via Tortona 12, 20144 Milano<br>
          P.IVA 14733480967<br>{L['foot_sdi']} KRRH6B9<br>
          <a href="mailto:iside.systems.srls@pec.it">iside.systems.srls@pec.it</a></p>
      </div>
      <div style="margin-top:24px">
        <p class="meta">{L['a_direct']}</p>
        <p style="margin-top:6px"><a href="mailto:alessandro@iside.systems">alessandro@iside.systems</a><br>
          <a href="https://www.linkedin.com/in/alesaccoia/" rel="me noopener" target="_blank">linkedin.com/in/alesaccoia</a></p>
      </div>
    </div>

    <form class="contact rv" action="/api/contact" method="post" novalidate
          data-mailto="alessandro@iside.systems"
          data-msg-required="{L['f_req']}" data-msg-ok="{L['f_ok']}"
          data-msg-sending="{L['f_sending']}" data-msg-fallback="{L['f_fallback']}">
      <div class="hp" aria-hidden="true">
        <label for="f-site">{L['f_hp']}</label>
        <input id="f-site" name="website" type="text" tabindex="-1" autocomplete="off">
      </div>
      <div class="field"><label for="f-name">{L['f_name']}</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="f-email">{L['f_email']}</label>
        <input id="f-email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="f-org">{L['f_org']}</label>
        <input id="f-org" name="organisation" type="text" autocomplete="organization"></div>
      <div class="field"><label for="f-topic">{L['f_topic']}</label>
        <select id="f-topic" name="topic">
{opts}        </select></div>
      <div class="field"><label for="f-msg">{L['f_msg']}</label>
        <textarea id="f-msg" name="message" required></textarea></div>
      <button type="submit">{L['f_send']}</button>
      <p class="formnote"></p>
    </form>
    <div class="formdone" hidden
         data-title="{L['f_done_title']}" data-lead="{L['f_done_lead']}"
         data-again="{L['f_done_again']}" data-reply="{L['f_done_reply']}"
         data-l-name="{L['f_name']}" data-l-email="{L['f_email']}"
         data-l-org="{L['f_org']}" data-l-topic="{L['f_topic']}" data-l-msg="{L['f_msg']}"></div>
  </div>
</section>

""" + footer(L, home, projects, about, asset))




# ---------------------------------------------------------------- metodologia
def page_metodo(L, asset, home, projects, about, alt_href, cases):
    lang = L["lang"]
    t = M.LABELS if lang == "it" else M.LABELS_EN
    sections = M.SECTIONS if lang == "it" else M.SECTIONS_EN
    g = M.GATE[lang]
    privacy_href = ("privacy.html" if lang == "en"
                    else ("../" * asset.count("../")) + "privacy.html")
    cfg = json.dumps({"pdf": M.PDF, "file": M.PDF.rsplit("/", 1)[-1], "lang": lang,
                      "sending": g["sending"], "done": g["done"], "fail": g["fail"],
                      "cta": g["cta"]}, ensure_ascii=False)
    # Il modulo sta in un modale: la pagina resta il documento, il download è un gesto.
    modal = f"""
<div class="wmodal" id="wmodal" hidden>
  <div class="wback" data-wclose></div>
  <div class="wpanel" role="dialog" aria-modal="true" aria-labelledby="wmtitle">
    <button class="wx" type="button" data-wclose aria-label="{g['close']}">&#215;</button>
    <div class="lbl">{g['lbl']}</div>
    <h2 id="wmtitle">{g['h']}</h2>
    <p class="dim">{g['p']}</p>
    <form class="wform" id="wform" novalidate>
      <div class="wrow">
        <label>{g['name']}<input name="name" autocomplete="given-name" required></label>
        <label>{g['surname']}<input name="surname" autocomplete="family-name" required></label>
      </div>
      <label>{g['email']}<input name="email" type="email" autocomplete="email" required></label>
      <label>{g['msg']}<textarea name="message" rows="2" placeholder="{g['msg_ph']}"></textarea></label>
      <label class="wcheck"><input type="checkbox" name="optin" value="1">
        <span>{g['consent']}</span></label>
      <input class="wpot" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button type="submit">{g['cta']}<span class="go">&#8594;</span></button>
      <p class="wnote" id="wnote" role="status" aria-live="polite"></p>
      <p class="wfine">{g['privacy']} <a href="{privacy_href}">{g['privacy_link']}</a>.</p>
    </form>
  </div>
</div>
"""
    return (head(L, f'{t["title"]} — Iside Systems', t["lede"], asset, alt_href, "metodo")
            + header(L, asset, home, projects, about, "metodo", alt_href, cases)
            + f"""
<article class="metodo">
<section class="pad" style="padding-top:clamp(46px,7vh,90px);padding-bottom:clamp(28px,5vh,52px)">
  <p class="meta">{t['kicker']}</p>
  <h1 style="margin-top:16px;max-width:17ch">{t['title']}</h1>
  <div class="mintro rv">
    <div class="mtext">
      <p class="lede">{t['sub']}</p>
      <p class="dim">{t['lede']}</p>
      <p class="meta">{t['meta']}</p>
    </div>
    <aside class="wcard">
      <div class="lbl">{g['lbl']}</div>
      <p>{g['card']}</p>
      <button class="ambtn" type="button" id="wopen">{g['open']}<span class="go">&#8594;</span></button>
      <p class="meta">{g['meta']}</p>
    </aside>
  </div>
</section>

<div class="pad mbody">
{M.render(sections, preview=True, more=g['more'], lang=lang)}
</div>
</article>
{modal}
<script>window.WPAPER={cfg};</script>
<script src="{asset}whitepaper.js" defer></script>
"""
            + footer(L, home, projects, about, asset))



# ---------------------------------------------------------------- privacy
# Dated by hand: it marks when the text changed, not when the site was built.
PRIVACY_DATE = {"it": "21 agosto 2026", "en": "21 August 2026"}

PRIVACY = {
"it": dict(
  title="Privacy policy",
  desc="Come Iside Systems SRLS tratta i dati personali di chi visita il sito, scrive dallo studio o usa l’AI Maturity Check.",
  lede="Quali dati raccogliamo, perché, a chi li comunichiamo e come puoi esercitare i tuoi "
       "diritti. Ogni sezione dice anche su quale base giuridica ci appoggiamo.",
  sections=[
   ("Titolare del trattamento", [
     "Iside Systems SRLS, Via Tortona 12, 20144 Milano (Italia). P.IVA 14733480967.",
     "Per qualsiasi questione relativa ai dati personali scrivi a "
     "<a href=\"mailto:alessandro@iside.systems\">alessandro@iside.systems</a> oppure, via PEC, a "
     "<a href=\"mailto:iside.systems.srls@pec.it\">iside.systems.srls@pec.it</a>.",
     "Non abbiamo nominato un responsabile della protezione dei dati (DPO): non ricorre nessuno dei "
     "casi previsti dall’art. 37 del Regolamento (UE) 2016/679 (GDPR)."]),

   ("Navigazione del sito", [
     "Il sito è ospitato da Vercel Inc. I server registrano, per il tempo tecnicamente necessario, "
     "informazioni che i browser trasmettono per loro natura: indirizzo IP, data e ora della "
     "richiesta, pagina richiesta, tipo di browser e sistema operativo. Questi dati servono a "
     "erogare il sito, a diagnosticare malfunzionamenti e a difenderlo da abusi.",
     "Base giuridica: legittimo interesse del titolare a far funzionare e proteggere il sito "
     "(art. 6.1.f GDPR)."]),

   ("Modulo di contatto", [
     "Se ci scrivi dal modulo nella pagina “Chi sono” raccogliamo il nome, l’indirizzo email e "
     "quello che scegli di scrivere nel messaggio, insieme all’eventuale organizzazione e "
     "all’argomento. Li usiamo per risponderti e, se il contatto diventa un progetto, per gestire "
     "il rapporto che ne nasce.",
     "Il messaggio viene recapitato tramite Mailjet (Sinch Email, con sede nell’Unione europea), "
     "che agisce come responsabile del trattamento.",
     "Base giuridica: riscontro a una tua richiesta ed esecuzione di misure precontrattuali "
     "(art. 6.1.b GDPR)."]),

   ("Download del whitepaper", [
     "Per ricevere il whitepaper completo chiediamo nome, cognome e indirizzo email, più "
     "l’eventuale messaggio che scegli di scrivere. Li usiamo per mandarti il PDF e per "
     "risponderti; una copia della richiesta arriva a noi. Anche qui non c’è una banca dati: "
     "la richiesta resta nelle caselle di posta.",
     "La casella di consenso è facoltativa e riguarda solo le comunicazioni successive su questi "
     "temi. Puoi revocarla in qualsiasi momento rispondendo a una delle email o scrivendo a "
     "alessandro@iside.systems, senza che questo tocchi la liceità dell’invio già avvenuto.",
     "Base giuridica: riscontro alla tua richiesta (art. 6.1.b GDPR) per l’invio del documento; "
     "consenso (art. 6.1.a GDPR) per le comunicazioni successive."]),

   ("AI Maturity Check", [
     "Il check si può fare senza registrarsi e senza lasciare alcun dato personale. Le risposte "
     "riguardano l’organizzazione — dimensione, settore, processi, strumenti — non la persona che "
     "le fornisce.",
     "Per costruire la sintesi finale le risposte e i punteggi vengono inviati a OpenAI, L.L.C. "
     "attraverso la sua API, senza nome, cognome o email: quelli te li chiediamo solo dopo, e solo "
     "se vuoi ricevere il report. Le richieste sono inviate con l’opzione di non conservazione e, "
     "secondo le condizioni per le API di OpenAI, non vengono usate per addestrare modelli.",
     "Se al termine compili il modulo, raccogliamo nome, cognome ed email e ti inviamo via email la "
     "mappa con il report; una copia dello stesso report, insieme alle risposte che hai dato, "
     "arriva a noi per poterti rispondere nel merito. Nulla di tutto questo viene salvato in una "
     "banca dati: resta nelle caselle di posta.",
     "Il report è una lettura indicativa costruita a partire dalle tue risposte. Non è una "
     "decisione automatizzata che produce effetti giuridici o incide in modo analogo sulla tua "
     "persona ai sensi dell’art. 22 GDPR.",
     "Base giuridica: esecuzione del servizio che hai richiesto e misure precontrattuali "
     "(art. 6.1.b GDPR)."]),

   ("Misurazione e cookie", [
     "Il sito usa Google Tag Manager e Google Analytics 4 per capire quante persone lo visitano e "
     "quali pagine leggono. Questi strumenti scrivono cookie sul tuo dispositivo.",
     "I cookie tecnici, necessari a far funzionare il sito e a ricordare la tua scelta sui cookie, "
     "vengono usati senza consenso perché senza di essi il sito non funziona. I cookie di "
     "misurazione e quelli pubblicitari vengono attivati solo dopo il tuo consenso, che ti "
     "chiediamo con il banner alla prima visita e che puoi negare o revocare in qualsiasi momento.",
     "Finché non acconsenti, il consenso è impostato su “negato” per tutte le finalità che lo "
     "richiedono (Consent Mode di Google): le richieste che partono verso Google non usano "
     "identificatori pubblicitari.",
     "La tua scelta è conservata nel browser (memoria locale, chiave <code>iside-consent</code>) e "
     "non viene trasmessa a noi. Per revocarla puoi cancellare i dati del sito dalle impostazioni "
     "del browser, e alla visita successiva il banner ricomparirà.",
     "Base giuridica: consenso per la misurazione e la pubblicità (art. 6.1.a GDPR e art. 122 del "
     "Codice privacy); legittimo interesse per i cookie tecnici."]),

   ("Campagne pubblicitarie", [
     "Quando promuoviamo una pagina su Google o LinkedIn, il link può contenere parametri che ci "
     "dicono da quale campagna arriva la visita. Sono informazioni sulla campagna, non su di te.",
     "Se hai acconsentito ai cookie pubblicitari, Google e LinkedIn possono usare i propri "
     "identificatori per misurare i risultati delle campagne secondo le rispettive informative."]),

   ("A chi comunichiamo i dati", [
     "I dati sono trattati dal titolare e dai fornitori che rendono possibile il servizio, "
     "nominati responsabili del trattamento ai sensi dell’art. 28 GDPR: Vercel Inc. (hosting), "
     "Sinch Email / Mailjet (invio delle email), Google Ireland Ltd. (misurazione e pubblicità), "
     "OpenAI, L.L.C. (generazione della sintesi dell’AI Maturity Check), LinkedIn Ireland "
     "Unlimited Company (pubblicità, se attiva).",
     "Non vendiamo e non cediamo i dati a terzi per finalità loro. Possono essere comunicati ad "
     "autorità pubbliche quando la legge lo impone."]),

   ("Trasferimenti fuori dall’Unione europea", [
     "Alcuni fornitori hanno sede negli Stati Uniti. I trasferimenti avvengono sulla base delle "
     "decisioni di adeguatezza applicabili — fra cui l’EU-U.S. Data Privacy Framework, per i "
     "fornitori che vi aderiscono — oppure delle clausole contrattuali standard adottate dalla "
     "Commissione europea, insieme alle misure supplementari previste dai rispettivi contratti."]),

   ("Per quanto tempo li conserviamo", [
     "La corrispondenza e i dati di contatto restano nelle nostre caselle per il tempo necessario a "
     "gestire la richiesta e l’eventuale rapporto che ne segue, e comunque non oltre 24 mesi "
     "dall’ultimo contatto, salvo obblighi di legge (per esempio quelli fiscali) che impongono "
     "termini più lunghi.",
     "I dati di misurazione sono conservati da Google Analytics secondo l’impostazione del "
     "servizio, in forma aggregata nei rapporti.",
     "I log tecnici del server sono conservati per il tempo previsto dal fornitore di hosting."]),

   ("I tuoi diritti", [
     "Puoi chiedere in qualsiasi momento l’accesso ai tuoi dati, la loro rettifica o cancellazione, "
     "la limitazione del trattamento, la portabilità, e puoi opporti al trattamento fondato sul "
     "legittimo interesse (artt. 15-22 GDPR). Se il trattamento si basa sul consenso, puoi "
     "revocarlo in ogni momento, senza che ciò pregiudichi quanto fatto prima della revoca.",
     "Per esercitarli scrivi a <a href=\"mailto:alessandro@iside.systems\">alessandro@iside.systems</a>. "
     "Rispondiamo entro un mese.",
     "Se ritieni che il trattamento violi il Regolamento puoi proporre reclamo al Garante per la "
     "protezione dei dati personali (<a href=\"https://www.garanteprivacy.it\" rel=\"noopener\" "
     "target=\"_blank\">garanteprivacy.it</a>) o all’autorità dello Stato in cui risiedi."]),

   ("Modifiche", [
     "Se cambiano gli strumenti che usiamo, questa pagina cambia con loro. La data qui sotto dice "
     "quando è stata aggiornata l’ultima volta."]),
  ]),

"en": dict(
  title="Privacy policy",
  desc="How Iside Systems SRLS handles the personal data of people who visit the site, write to the practice, or use the AI Maturity Check.",
  lede="What we collect, why, who we share it with, and how you can exercise your rights. Each "
       "section also names the legal basis we rely on.",
  sections=[
   ("Controller", [
     "Iside Systems SRLS, Via Tortona 12, 20144 Milan, Italy. VAT IT14733480967.",
     "For anything concerning personal data, write to "
     "<a href=\"mailto:alessandro@iside.systems\">alessandro@iside.systems</a>.",
     "We have not appointed a Data Protection Officer: none of the cases in Article 37 of "
     "Regulation (EU) 2016/679 (GDPR) applies."]),

   ("Browsing the site", [
     "The site is hosted by Vercel Inc. Its servers record, for as long as technically necessary, "
     "the information browsers send by their nature: IP address, date and time of the request, the "
     "page requested, browser type and operating system. This is used to serve the site, diagnose "
     "faults and defend it from abuse.",
     "Legal basis: our legitimate interest in running and protecting the site (Art. 6.1.f GDPR)."]),

   ("Contact form", [
     "If you write from the form on the About page we collect your name, email address and whatever "
     "you choose to put in the message, along with any organisation and topic. We use it to answer "
     "you and, if the enquiry becomes a project, to manage the engagement that follows.",
     "The message is delivered through Mailjet (Sinch Email, based in the European Union), acting "
     "as a processor.",
     "Legal basis: answering your request and pre-contractual steps (Art. 6.1.b GDPR)."]),

   ("Whitepaper download", [
     "To receive the full whitepaper we ask for a first name, a last name and an email address, "
     "plus whatever you choose to write in the message field. We use them to send you the PDF and "
     "to reply; a copy of the request reaches us. Here too there is no database: the request stays "
     "in the mailboxes.",
     "The consent box is optional and covers only later communications on these subjects. You can "
     "withdraw it at any time by replying to one of the emails or writing to "
     "alessandro@iside.systems, without affecting the lawfulness of what was already sent.",
     "Legal basis: responding to your request (Art. 6.1.b GDPR) for sending the document; consent "
     "(Art. 6.1.a GDPR) for later communications."]),

   ("AI Maturity Check", [
     "The check can be taken without signing up and without leaving any personal data. The answers "
     "describe the organisation — size, sector, processes, tools — not the person giving them.",
     "To produce the closing summary, the answers and the scores are sent to OpenAI, L.L.C. through "
     "its API, without your name or email: we ask for those afterwards, and only if you want the "
     "report. Requests are sent with storage disabled and, under OpenAI's API terms, are not used "
     "to train models.",
     "If you fill in the form at the end, we collect your first name, last name and email and send "
     "you the report by email; a copy of the same report, together with the answers you gave, "
     "reaches us so we can reply on the substance. None of it is written to a database: it stays in "
     "the mailboxes.",
     "The report is an indicative reading built from your answers. It is not an automated decision "
     "producing legal effects or similarly significantly affecting you under Art. 22 GDPR.",
     "Legal basis: providing the service you asked for and pre-contractual steps (Art. 6.1.b GDPR)."]),

   ("Measurement and cookies", [
     "The site uses Google Tag Manager and Google Analytics 4 to understand how many people visit "
     "and which pages they read. These tools write cookies on your device.",
     "Technical cookies, needed to run the site and to remember your cookie choice, are used "
     "without consent because the site does not work without them. Measurement and advertising "
     "cookies are only switched on after you consent, which we ask for with the banner on your "
     "first visit and which you can refuse or withdraw at any time.",
     "Until you consent, consent is set to \"denied\" for every purpose that requires it (Google "
     "Consent Mode): requests to Google carry no advertising identifiers.",
     "Your choice is kept in your browser (local storage, key <code>iside-consent</code>) and is "
     "not sent to us. To withdraw it, clear the site data in your browser settings, and the banner will "
     "appear again on your next visit.",
     "Legal basis: consent for measurement and advertising (Art. 6.1.a GDPR and Art. 122 of the "
     "Italian Privacy Code); legitimate interest for technical cookies."]),

   ("Advertising campaigns", [
     "When we promote a page on Google or LinkedIn, the link may carry parameters telling us which "
     "campaign the visit came from. That is information about the campaign, not about you.",
     "If you have consented to advertising cookies, Google and LinkedIn may use their own "
     "identifiers to measure campaign results under their own privacy notices."]),

   ("Who we share it with", [
     "Data is handled by the controller and by the suppliers that make the service possible, "
     "appointed as processors under Art. 28 GDPR: Vercel Inc. (hosting), Sinch Email / Mailjet "
     "(email delivery), Google Ireland Ltd. (measurement and advertising), OpenAI, L.L.C. "
     "(generating the AI Maturity Check summary), LinkedIn Ireland Unlimited Company (advertising, "
     "where running).",
     "We do not sell or hand data to third parties for their own purposes. It may be disclosed to "
     "public authorities where the law requires it."]),

   ("Transfers outside the European Union", [
     "Some suppliers are based in the United States. Transfers rely on the applicable adequacy "
     "decisions — including the EU-U.S. Data Privacy Framework for suppliers certified under it — "
     "or on the standard contractual clauses adopted by the European Commission, together with the "
     "supplementary measures set out in the respective agreements."]),

   ("How long we keep it", [
     "Correspondence and contact details stay in our mailboxes for as long as it takes to handle "
     "the request and any engagement that follows, and in any case no longer than 24 months from "
     "the last contact, save for legal obligations (tax rules, for instance) that impose longer "
     "terms.",
     "Measurement data is retained by Google Analytics according to the service settings, and "
     "appears in reports in aggregate form.",
     "Server logs are kept for the period set by the hosting provider."]),

   ("Your rights", [
     "You may at any time request access to your data, its rectification or erasure, restriction of "
     "processing, portability, and you may object to processing based on legitimate interest "
     "(Arts. 15-22 GDPR). Where processing is based on consent, you may withdraw it at any time, "
     "without affecting what was done before the withdrawal.",
     "To exercise them, write to <a href=\"mailto:alessandro@iside.systems\">alessandro@iside.systems</a>. "
     "We answer within one month.",
     "If you believe the processing infringes the Regulation you may lodge a complaint with the "
     "Italian data protection authority (<a href=\"https://www.garanteprivacy.it\" rel=\"noopener\" "
     "target=\"_blank\">garanteprivacy.it</a>) or with the authority of the country where you live."]),

   ("Changes", [
     "If the tools we use change, this page changes with them. The date below says when it was "
     "last updated."]),
  ]),
}




# ---------------------------------------------------------------- blog
def page_blog(L, asset, home, projects, about, alt_href, cases):
    t = B.BLOG_LABELS[L["lang"]]
    rows = ""
    for post in B.published(L["lang"]):
        href = f"/en/blog/{post['slug']}" if L["lang"] == "en" else f"/blog/{post['slug']}"
        rows += f"""    <a class="bcard rv" href="{href}">
      <div class="bck"><span class="meta">{post['human_date']}</span>
        <span class="meta">{post['read']} {t['read']}</span></div>
      <div class="bcb">
        <h2>{post['title']}</h2>
        <p>{post['dek']}</p>
        <div class="tags">{B.chips(post['tags'])}</div>
        <span class="go">{t['more']} →</span>
      </div>
    </a>
"""
    note = f'<p class="meta" style="margin-top:22px">{t["note"]}</p>' if L["lang"] == "en" else ""
    if not rows:
        # nothing published yet: say so plainly instead of showing an empty list
        rows = (f'    <div class="bempty rv"><h2>{t["empty_h"]}</h2>'
                f'<p>{t["empty_p"]}</p></div>\n')
        note = ""
    return (head(L, f'{t["title"]} — Iside Systems', t["lede"], asset, alt_href, "blog")
            + header(L, asset, home, projects, about, "blog", alt_href, cases)
            + f"""
<section class="pad blogindex">
  <div class="lbl">{t['kicker']}</div>
  <h1>{t['title']}</h1>
  <p class="lede dim">{t['lede']}</p>
  {note}
  <div class="bcards">
{rows}  </div>
</section>
"""
            + footer(L, home, projects, about, asset))


def page_post(L, asset, home, projects, about, alt_href, cases, post):
    t = B.BLOG_LABELS[L["lang"]]
    url = f"{SITE}/{'en/blog' if L['lang'] == 'en' else 'blog'}/{post['slug']}"
    ld = ('<script type="application/ld+json">'
          '{"@context":"https://schema.org","@type":"BlogPosting",'
          f'"headline":{json.dumps(post["title"], ensure_ascii=False)},'
          f'"description":{json.dumps(post["dek"], ensure_ascii=False)},'
          f'"datePublished":"{post["date"]}","inLanguage":"{L["lang"]}",'
          f'"keywords":{json.dumps(", ".join(post["tags"]), ensure_ascii=False)},'
          f'"mainEntityOfPage":"{url}",'
          '"author":{"@type":"Person","name":"Alessandro Saccoia"},'
          '"publisher":{"@type":"Organization","name":"Iside Systems SRLS"}}'
          "</script>")
    return (head(L, f'{post["title"]} — Iside Systems', post["dek"], asset, alt_href,
                 f"post-{post['slug']}", post.get("og_image"))
            + ld
            + header(L, asset, home, projects, about, "blog", alt_href, cases)
            + f"""
<article class="pad post">
  <div class="lbl">{t['kicker']}</div>
  <h1>{post['title']}</h1>
  <p class="lede dim">{post['dek']}</p>
  <div class="postmeta">
    <span>{t['updated']} {post['human_date']}</span><span>{post['read']} {t['read']}</span>
    <span class="tags">{B.chips(post['tags'])}</span>
  </div>
  <div class="pbody">
{B.render_blocks(post['body'], L['lang'])}
  </div>
  <p class="pback"><a href="/blog">{t['back']}</a></p>
</article>
"""
            + footer(L, home, projects, about, asset))



def page_privacy(L, asset, home, projects, about, alt_href, cases="case-study.html"):
    t = PRIVACY[L["lang"]]
    # same two-column rhythm as the case studies: the heading on the left,
    # the text on the right, across the full width of the page
    body = '  <div class="cssteps legal-steps">\n'
    for heading, paragraphs in t["sections"]:
        body += ('    <section class="csstep rv">'
                 f'<div class="k">{heading}</div>'
                 + "<div>" + "".join(f"<p>{para}</p>" for para in paragraphs) + "</div>"
                 + "</section>\n")
    body += "  </div>\n"
    return (head(L, f'{t["title"]} — Iside Systems', t["desc"], asset, alt_href, "privacy")
            + header(L, asset, home, projects, about, "", alt_href, cases)
            + f"""
<section class="pad legal">
  <div class="lbl">{t["title"]}</div>
  <h1>{t["title"]}</h1>
  <p class="lede dim">{t["lede"]}</p>
{body}  <p class="meta legal-date">{L["privacy_updated"]}: {PRIVACY_DATE[L["lang"]]}</p>
</section>
"""
            + footer(L, home, projects, about, asset))

def page_lab(L, asset, home, projects, about, alt_href, key, cases="case-study.html"):
    lab = LABS[key]
    t = lab[L["lang"]]
    body = "".join(f'<p class="dim" style="margin-top:1.2em">{b}</p>' for b in t["body"])
    cols = "".join(
        f'<div class="rv"><h3>{h}</h3><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
        for h, items in t["cols"])
    # the English pages live one level down, so the demo link needs the hop
    root = "../" if asset.startswith("../") else ""
    # a string demo is a relative path inside the site; a dict is already absolute
    # and carries its own per-language destination
    href = lab["demo"]
    if isinstance(href, dict): href = href[L["lang"]]
    elif href: href = root + href
    demo = (f'<p style="margin-top:30px"><a class="labcta" href="{href}">{t["cta"]}</a></p>'
            if href and t["cta"] else "")
    title = f'{t["title"]} — Iside Systems'
    return (head(L, title, t["lede"], asset, alt_href, key)
            + header(L, asset, home, projects, about, "projects", alt_href, cases)
            + f"""
<section class="labhero">
  <p class="meta">{t['kicker']}</p>
  <h1 style="margin-top:14px">{t['title']}</h1>
  <p class="lede dim" style="margin-top:20px">{t['lede']}</p>
  <img class="labshot" src="{asset}{lab['shot']}" alt="{t['title']}" loading="lazy">
</section>

<section class="pad" style="padding-top:clamp(40px,7vh,80px);padding-bottom:clamp(50px,9vh,110px)">
  <div class="cols2">
    <div class="rv"><p class="dim">{t['body'][0]}</p></div>
    <div class="rv"><p class="dim">{t['body'][1]}</p></div>
  </div>
  <div class="labgrid">{cols}</div>
  {demo}
  <p class="meta" style="margin-top:22px">{t['note']}</p>
  {mini_cta(L, about, 2)}
  <p style="margin-top:34px"><a class="labback" href="{projects}">← {t['back']}</a></p>
</section>

""" + footer(L, home, projects, about, asset))


def mini_cta(L, about, i=0):
    """A quiet one-line prompt, dropped between sections."""
    if i == 1:
        return ('<p style="margin-top:26px"><a class="meta" href="%s#contact" '
                'style="color:var(--acc);text-decoration:none">%s</a></p>'
                % (about, L["mini_cta"][i]))
    return ('<div class="minicta rv"><a href="%s#contact">%s<span class="go">\u2192</span></a></div>'
            % (about, L["mini_cta"][i].replace(" →", "")))


def case_next(L, cases):
    out = ""
    for c in cases:
        out += '<a href="%s"><b>%s</b> %s</a>' % (_case_href(c, L["lang"]), c["n"], c["lbl"])
    return out


def case_rows(L):
    out = ""
    for c in L["cs_cases"]:
        out += ('<a class="csrow" href="%s"><span class="n">%s</span>'
                '<span class="t">%s</span><span class="s">%s</span>'
                '<span class="go">\u2192</span></a>'
                % (_case_href(c, L["lang"]), c["n"], c["h2"].replace("<br>", " "), c["lbl"]))
    return out


def _case_href(c, lang):
    return f"case-{c['slug']}.html"


def page_cases(L, asset, home, projects, about, alt_href, cases):
    """The index: one card per case, each with a live preview of its figure."""
    cards = ""
    for c in L["cs_cases"]:
        cards += f"""
    <a class="cscard rv" href="{_case_href(c, L['lang'])}">
      <canvas class="csfig" id="card-{c['fig']}" data-labels="{'|'.join(k for k, _h, _d in c['steps'])}"
              data-out="{L['cs_fig_out']}" data-src="{L['cs_fig_src']}" data-replay="1"></canvas>
      <div class="b">
        <p class="meta">{c['n']} — {c['lbl']}{" · " + c["date"] if c.get("date") else ""}</p>
        <h2>{c['h2']}</h2>
        <p class="dim">{c['card']}</p>
        <div class="facts">{chips(c['chips'][:4])}</div>
        <span class="csgo">{L['cs_card_cta']} →</span>
      </div>
    </a>
"""
    return (head(L, L["cs_title"], L["cs_desc"], asset, alt_href, "cases")
            + header(L, asset, home, projects, about, "cases", alt_href, cases)
            + newsbar(L, about)
            + f"""
<section class="pad" style="padding-top:clamp(46px,7vh,90px);padding-bottom:clamp(34px,5vh,60px)">
  <p class="meta">{L['cs_kicker']}</p>
  <h1 style="margin-top:16px;max-width:19ch">{L['cs_h1']}</h1>
  <p class="lede dim" style="margin-top:22px">{L['cs_lede']}</p>
</section>

<section class="pad" style="padding-bottom:clamp(56px,9vh,110px)">
  <div class="cscards">{cards}  </div>
</section>

<section class="pad rule" style="padding-top:clamp(56px,9vh,110px);padding-bottom:clamp(60px,10vh,120px)">
  <h2 class="rv">{L['cs_cta_h2']}</h2>
  <p class="lede dim rv" style="margin-top:22px">{L['cs_cta_p']}</p>
  <p style="margin-top:30px"><a class="meta" href="{about}#contact" style="color:var(--acc);text-decoration:none">{L['cs_cta_link']}</a></p>
</section>

""" + footer(L, home, projects, about, asset))


def page_case(L, asset, home, projects, about, alt_href, cases, slug):
    c = next(x for x in L["cs_cases"] if x["slug"] == slug)
    others = [x for x in L["cs_cases"] if x["slug"] != slug]
    steps = "".join(
        f'<div class="csstep rv"><div class="k">{k}</div>'
        f'<div><b>{h}</b><i>{d}</i></div></div>'
        for k, h, d in c["steps"])
    return (head(L, f"{c['lbl']} — Iside Systems", c["card"], asset, alt_href, f"case-{slug}")
            + header(L, asset, home, projects, about, "cases", alt_href, cases)
            + f"""
<section class="labhero">
  <p class="meta">{L['cs_kicker']} · {c['n']}{" · " + c["date"] if c.get("date") else ""}</p>
  <h1 style="margin-top:14px;max-width:18ch">{c['h2']}</h1>
  <p class="lede dim" style="margin-top:20px">{c['lbl']}</p>
</section>

<section class="pad" style="padding-top:clamp(46px,8vh,90px);padding-bottom:clamp(30px,5vh,50px)">
  <div class="cols2" style="align-items:start">
    <div class="rv"><p class="dim">{c['ctx'][0]}</p></div>
    <div class="rv"><p class="dim">{c['ctx'][1]}</p></div>
  </div>
  <div class="facts" style="margin-top:28px">{chips(c['chips'])}</div>
  <div class="figbox rv" style="margin-top:clamp(30px,5vh,60px)">
    <canvas class="fig" id="fig-{c['fig']}" data-labels="{'|'.join(k for k, _h, _d in c['steps'])}" data-out="{L['cs_fig_out']}" data-src="{L['cs_fig_src']}"></canvas>
  </div>
  <div class="cssteps">{steps}</div>
  <p class="lede dim rv" style="margin-top:clamp(30px,5vh,54px)">{c['out']}</p>
  {mini_cta(L, about, 3)}
</section>

<section class="pad rule" style="padding-top:clamp(46px,8vh,90px);padding-bottom:clamp(56px,9vh,110px)">
  <p class="meta">{L['cs_other']}</p>
  <div class="csnext">{case_next(L, others)}</div>
  <p style="margin-top:30px"><a class="labback" href="{cases}">← {L['cs_back']}</a></p>
</section>

""" + footer(L, home, projects, about, asset))


# ---------------------------------------------------------------- write
def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    print("wrote", path)

# ---------------------------------------------------------------- robots + sitemap
def write_seo():
    today = datetime.date.today().isoformat()
    rows = []
    for key in ("home", "cases", "case-ai-adoption", "case-james", "case-cloud-scale",
                "projects", "about", "privacy", "blog", "metodo"):
        it_path, en_path = PATHS[key]
        for path, lang in ((it_path, "it"), (en_path, "en")):
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}/{p}"/>'
                for h, p in (("it", it_path), ("en", en_path), ("x-default", it_path)))
            prio = ("1.0" if key == "home" and lang == "it" else "0.8" if key == "home"
                    else "0.3" if key == "privacy" else "0.7")
            rows.append(
                f'  <url>\n    <loc>{SITE}/{path}</loc>\n    <lastmod>{today}</lastmod>'
                f'\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>'
                f'{alts}\n  </url>')
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
               '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
               + "\n".join(rows) + "\n</urlset>\n")
    posts = "".join(
        f'  <url>\n    <loc>{SITE}/blog/{p["slug"]}</loc>\n'
        f'    <xhtml:link rel="alternate" hreflang="it" href="{SITE}/blog/{p["slug"]}"/>\n'
        f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/blog/{p_en["slug"]}"/>\n'
        f'    <lastmod>{p["date"]}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
        f'  <url>\n    <loc>{SITE}/en/blog/{p_en["slug"]}</loc>\n'
        f'    <xhtml:link rel="alternate" hreflang="it" href="{SITE}/blog/{p["slug"]}"/>\n'
        f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/blog/{p_en["slug"]}"/>\n'
        f'    <lastmod>{p["date"]}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
        for p, p_en in zip(B.published(), B.published("en")))
    sitemap = sitemap.replace("</urlset>", posts + "</urlset>")
    write("sitemap.xml", sitemap)

    # a feed, because a blog without one is a newsletter you cannot leave
    items = "".join(
        f"  <item>\n    <title>{html.escape(p['title'])}</title>\n"
        f"    <link>{SITE}/blog/{p['slug']}</link>\n"
        f"    <guid>{SITE}/blog/{p['slug']}</guid>\n"
        f"    <pubDate>{p['date']}</pubDate>\n"
        + "".join(f"    <category>{html.escape(t)}</category>\n" for t in p["tags"])
        + f"    <description>{html.escape(p['dek'])}</description>\n  </item>\n"
        for p in B.published())
    write("feed.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<rss version="2.0"><channel>\n'
          f"  <title>Iside Systems — Blog</title>\n  <link>{SITE}/blog</link>\n"
          f"  <language>it</language>\n"
          f"  <description>{html.escape(B.BLOG_LABELS['it']['lede'])}</description>\n"
          + items + "</channel></rss>\n")

    write("robots.txt",
          "User-agent: *\n"
          "Allow: /\n"
          "\n"
          f"Sitemap: {SITE}/sitemap.xml\n")


# Italian at the root
write("case-study.html",      page_cases(L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html",
                                         "en/case-studies.html", "case-study.html"))
write("en/case-studies.html", page_cases(L_EN, "../assets/", "index.html", "projects.html", "about.html",
                                         "../case-study.html", "case-studies.html"))
for _slug in ("ai-adoption", "james", "cloud-scale"):
    write(f"case-{_slug}.html",
          page_case(L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html",
                    f"en/case-{_slug}.html", "case-study.html", _slug))
    write(f"en/case-{_slug}.html",
          page_case(L_EN, "../assets/", "index.html", "projects.html", "about.html",
                    f"../case-{_slug}.html", "case-studies.html", _slug))

write("index.html",     page_home    (L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html", "en/index.html"))
write("progetti.html",  page_projects(L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html", "en/projects.html"))
write("chi-sono.html",  page_about   (L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html", "en/about.html"))
write("privacy.html",   page_privacy (L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html", "en/privacy.html"))
write("metodologia.html", page_metodo(L_IT, "assets/", "index.html", "progetti.html",
                                     "chi-sono.html", "en/methodology.html", "case-study.html"))
write("blog/index.html", page_blog(L_IT, "/assets/", "/", "/progetti.html",
                                   "/chi-sono.html", "/en/blog", "/case-study.html"))
# a post that goes back to draft must stop existing as a page, not linger
import shutil as _shutil
_live = {p["slug"] for p in B.published()}
_blogdir = os.path.join(HERE, "blog")
if os.path.isdir(_blogdir):
    for _name in os.listdir(_blogdir):
        _path = os.path.join(_blogdir, _name)
        if os.path.isdir(_path) and _name not in _live:
            _shutil.rmtree(_path)
            print("removed stale", f"blog/{_name}")

for _post in B.published():
    write(f"blog/{_post['slug']}/index.html",
          page_post(L_IT, "/assets/", "/", "/progetti.html",
                    "/chi-sono.html", "/en/blog", "/case-study.html", _post))

_en_blogdir = os.path.join(HERE, "en", "blog")
_en_live = {p["slug"] for p in B.published("en")}
if os.path.isdir(_en_blogdir):
    for _name in os.listdir(_en_blogdir):
        _path = os.path.join(_en_blogdir, _name)
        if os.path.isdir(_path) and _name not in _en_live:
            _shutil.rmtree(_path)
for _post_it, _post in zip(B.published(), B.published("en")):
    write(f"en/blog/{_post['slug']}/index.html",
          page_post(L_EN, "/assets/", "/en", "/en/projects.html",
                    "/en/about.html", f"/blog/{_post_it['slug']}", "/en/case-studies.html", _post))

for key in ("moire", "algosynth"):
    write(f"{key}.html",    page_lab(L_IT, "assets/", "index.html", "progetti.html", "chi-sono.html",
                                     f"en/{key}.html", key))
    write(f"en/{key}.html", page_lab(L_EN, "../assets/", "index.html", "projects.html", "about.html",
                                     f"../{key}.html", key, "case-studies.html"))

# English under /en/
write("en/index.html",    page_home    (L_EN, "../assets/", "index.html", "projects.html", "about.html", "../index.html", "case-studies.html"))
write("en/projects.html", page_projects(L_EN, "../assets/", "index.html", "projects.html", "about.html", "../progetti.html", "case-studies.html"))
write("en/about.html",    page_about   (L_EN, "../assets/", "index.html", "projects.html", "about.html", "../chi-sono.html", "case-studies.html"))
write("en/privacy.html",  page_privacy (L_EN, "../assets/", "index.html", "projects.html", "about.html", "../privacy.html", "case-studies.html"))
write("en/methodology.html", page_metodo(L_EN, "../assets/", "index.html", "projects.html",
                                        "about.html", "../metodologia.html", "case-studies.html"))
write("en/blog/index.html", page_blog(L_EN, "/assets/", "/en", "/en/projects.html",
                                      "/en/about.html", "/blog", "/en/case-studies.html"))

write_seo()
