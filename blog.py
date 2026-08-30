# -*- coding: utf-8 -*-
"""Blog content and rendering.

Kept out of build.py: the posts are long, and the site generator is already a
big file. build.py imports POSTS, figures() and the two page renderers.
"""

BLOG_LABELS = {
    "it": dict(kicker="Blog", title="Note su dati, AI e adozione",
               lede="Quello che imparo mettendo l’AI dentro le organizzazioni: cosa si compra "
                    "davvero, come si governa, e dove i progetti si incagliano.",
               read="min di lettura", back="← Tutti gli articoli", updated="Pubblicato",
               toc="In questa pagina", more="Continua a leggere",
               note="Gli articoli sono in italiano.",
               empty_h="Non ci sono articoli al momento.",
               empty_p="Sto scrivendo. Qui finiranno note su acquisto, governance e adozione "
                       "dell’AI in azienda — quello che imparo sul campo, non quello che si "
                       "legge ovunque."),
    "en": dict(kicker="Blog", title="Notes on data, AI and adoption",
               lede="What I learn putting AI inside organisations: what you are actually buying, "
                    "how to govern it, and where these projects run aground.",
               read="min read", back="← All posts", updated="Published",
               toc="On this page", more="Keep reading",
               note="The posts are written in Italian.",
               empty_h="No posts yet.",
               empty_p="Notes on buying, governing and adopting AI inside companies will land "
                       "here — what I learn on the job, not what is written everywhere else."),
}


# ---------------------------------------------------------------- figures
def fig_planes():
    """One knowledge plane, several execution surfaces."""
    return """
<svg viewBox="0 0 900 400" class="bfig" role="img"
     aria-label="Un solo piano di conoscenza, più superfici di esecuzione">
  <g fill="none" stroke="currentColor" stroke-opacity=".22">
    <rect x="250" y="300" width="400" height="72"/>
    <rect x="60"  y="150" width="220" height="76"/>
    <rect x="340" y="150" width="220" height="76"/>
    <rect x="620" y="150" width="220" height="76"/>
    <rect x="340" y="30"  width="220" height="62"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity=".35">
    <path d="M170 300V226"/><path d="M450 300V226"/><path d="M730 300V226"/>
    <path d="M450 150V92"/>
  </g>
  <g font-family="var(--mono)" font-size="12" letter-spacing="1.4" fill="currentColor">
    <text x="450" y="343" text-anchor="middle" fill="var(--acc)">FONTE DI VERITÀ — SHAREPOINT / M365</text>
    <text x="170" y="194" text-anchor="middle">COPILOT</text>
    <text x="450" y="194" text-anchor="middle">ASSISTENTE A</text>
    <text x="730" y="194" text-anchor="middle">ASSISTENTE B</text>
    <text x="450" y="67"  text-anchor="middle">IDENTITÀ — SSO / SCIM</text>
  </g>
  <g font-family="var(--sans)" font-size="13" fill="currentColor" fill-opacity=".6">
    <text x="450" y="392" text-anchor="middle">i documenti restano dove sono: nessuna copia, nessun indice parallelo</text>
  </g>
</svg>"""


def fig_layers():
    """The behaviour stack, from the constitution down to the person."""
    rows = [("ISTRUZIONI DI ORGANIZZAZIONE", "policy, tono, confidenzialità — poche righe, valide per tutti"),
            ("PLUGIN E SKILL DI REPARTO", "metodo e procedure della business unit, versionati"),
            ("ISTRUZIONI DI PROGETTO", "contesto del cliente o del programma"),
            ("ISTRUZIONI PERSONALI", "ruolo, lingua, formato preferito"),
            ("RECUPERO DAL REPOSITORY", "la conoscenza, letta al momento, con i permessi di chi chiede")]
    out = ['<svg viewBox="0 0 900 430" class="bfig" role="img" aria-label="I livelli del comportamento">']
    y = 20
    for i, (title, sub) in enumerate(rows):
        acc = ' stroke="var(--acc)"' if i == 0 else ' stroke="currentColor" stroke-opacity=".25"'
        out.append(f'<rect x="60" y="{y}" width="780" height="62" fill="none"{acc}/>')
        out.append(f'<text x="84" y="{y+27}" font-family="var(--mono)" font-size="12" '
                   f'letter-spacing="1.4" fill="{"var(--acc)" if i == 0 else "currentColor"}">{title}</text>')
        out.append(f'<text x="84" y="{y+48}" font-family="var(--sans)" font-size="13.5" '
                   f'fill="currentColor" fill-opacity=".6">{sub}</text>')
        if i < len(rows) - 1:
            out.append(f'<path d="M450 {y+62}v20" stroke="currentColor" stroke-opacity=".3"/>')
        y += 82
    out.append("</svg>")
    return "".join(out)


def fig_retrieval():
    """Indexed copy versus live read."""
    return """
<svg viewBox="0 0 900 320" class="bfig" role="img" aria-label="Indice sincronizzato contro lettura dal vivo">
  <g fill="none" stroke="currentColor" stroke-opacity=".25">
    <rect x="60" y="40" width="360" height="230"/>
    <rect x="480" y="40" width="360" height="230"/>
    <rect x="96" y="86" width="120" height="46"/>
    <rect x="264" y="86" width="120" height="46"/>
    <rect x="516" y="86" width="120" height="46"/>
    <rect x="684" y="86" width="120" height="46"/>
    <rect x="180" y="196" width="120" height="46"/>
    <rect x="600" y="196" width="120" height="46"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-opacity=".35">
    <path d="M156 132v30h84v34"/><path d="M324 132v30h-84v34"/>
    <path d="M576 132v64h84"/><path d="M744 132v64h-84"/>
  </g>
  <g font-family="var(--mono)" font-size="11.5" letter-spacing="1.2" fill="currentColor">
    <text x="156" y="114" text-anchor="middle">DOCUMENTI</text>
    <text x="324" y="114" text-anchor="middle">INDICE</text>
    <text x="240" y="224" text-anchor="middle">RISPOSTA</text>
    <text x="576" y="114" text-anchor="middle">DOCUMENTI</text>
    <text x="744" y="114" text-anchor="middle">PERMESSI</text>
    <text x="660" y="224" text-anchor="middle">RISPOSTA</text>
    <text x="240" y="68" text-anchor="middle" fill="var(--acc)">SINCRONIZZATO</text>
    <text x="660" y="68" text-anchor="middle" fill="var(--acc)">DAL VIVO</text>
  </g>
  <g font-family="var(--sans)" font-size="13" fill="currentColor" fill-opacity=".6">
    <text x="240" y="300" text-anchor="middle">veloce, ambito disegnabile — ma è una copia</text>
    <text x="660" y="300" text-anchor="middle">sempre aggiornato — ambito = permessi</text>
  </g>
</svg>"""


def fig_phases():
    """Four phases, one quarter."""
    phases = [("01", "FONDAMENTA", "identità, retention, istruzioni"),
              ("02", "PILOTA", "un reparto, tre flussi, metriche"),
              ("03", "DISTRIBUZIONE", "plugin per gruppo, formazione"),
              ("04", "ESERCIZIO", "revisione skill, costi, permessi")]
    out = ['<svg viewBox="0 0 900 240" class="bfig" role="img" aria-label="Quattro fasi di adozione">',
           '<path d="M60 120H840" stroke="currentColor" stroke-opacity=".25"/>',
           '<path d="M60 120H255" stroke="var(--acc)" stroke-width="2"/>']
    for i, (n, name, sub) in enumerate(phases):
        x = 60 + i * 260
        out.append(f'<circle cx="{x}" cy="120" r="6" fill="{"var(--acc)" if i == 0 else "currentColor"}" '
                   f'fill-opacity="{1 if i == 0 else .45}"/>')
        out.append(f'<text x="{x}" y="90" font-family="var(--mono)" font-size="12" letter-spacing="1.4" '
                   f'fill="var(--acc)">{n}</text>')
        out.append(f'<text x="{x}" y="156" font-family="var(--mono)" font-size="12.5" '
                   f'letter-spacing="1.4" fill="currentColor">{name}</text>')
        out.append(f'<text x="{x}" y="180" font-family="var(--sans)" font-size="13.5" '
                   f'fill="currentColor" fill-opacity=".6">{sub}</text>')
    out.append("</svg>")
    return "".join(out)


FIGURES = {"planes": fig_planes, "layers": fig_layers,
           "retrieval": fig_retrieval, "phases": fig_phases}


# ---------------------------------------------------------------- posts
# Blocks: ("h2"|"h3"|"p"|"ul"|"ol"|"fig"|"note"|"table", payload)
POSTS = [
dict(
  draft=True,
  slug="cosa-si-compra-davvero",
  date="2026-08-26", human_date="26 agosto 2026", read=14,
  tags=["AI adoption", "Enterprise", "Governance"],
  title="Comprare AI in azienda: cosa stai acquistando davvero",
  dek="Le licenze si confrontano in mezz’ora. Quello che decide se il progetto reggerà "
      "sono quattro cose che nessuno guarda in fase di acquisto: dove stanno i dati, chi "
      "sono gli utenti, come entra la conoscenza, e chi risponde quando qualcosa va storto.",
  body=[
   ("p", "Quando un’azienda decide di “prendere l’AI”, la conversazione parte quasi sempre dal "
         "prezzo per utente e finisce in un confronto fra due schede tecniche. È la parte facile, "
         "ed è anche quella che conta meno. Le due o tre piattaforme enterprise serie oggi si "
         "somigliano molto su ciò che si vede: chattano bene, leggono documenti, eseguono compiti "
         "in autonomia, hanno un pannello di amministrazione. Si somigliano molto meno su ciò che "
         "non si vede in demo."),
   ("p", "Stai comprando un <mark>piano di controllo</mark> che si appoggia ai tuoi sistemi di "
         "identità, ai tuoi documenti e ai tuoi processi. Se quel piano è coerente, l’assistente "
         "diventa utile in poche settimane. Se non lo è, hai comprato centoventi abbonamenti che "
         "le persone useranno per riscrivere le email."),

   ("h2", "Le quattro domande che decidono l’acquisto"),
   ("p", "In un capitolato le metterei prima di ogni funzionalità: una funzione mancante si "
         "aggiunge, una scelta su dove vivono i dati si cambia solo rifacendo il progetto."),
   ("ol", ["<b>Dove vivono i dati, e dove avviene l’inferenza.</b> Sono due cose diverse: una "
           "piattaforma può conservare le conversazioni in Europa e calcolarle altrove. Se sei "
           "in un settore regolato, o se il tuo ufficio legale ha già sofferto su questo, è la "
           "prima domanda e non l’ultima.",
           "<b>Per quanto tempo restano.</b> Le finestre minime di conservazione variano "
           "sensibilmente fra i fornitori, e non sempre si possono portare a zero. Una "
           "conservazione breve riduce l’esposizione ma toglie memoria e contesto: è un "
           "compromesso, non un interruttore di sicurezza.",
           "<b>Chi sono gli utenti.</b> Federazione con il tuo identity provider e "
           "provisioning automatico non sono un dettaglio IT: senza, dopo sei mesi hai account "
           "attivi di persone che hanno lasciato l’azienda. In diversi listini il provisioning "
           "automatico compare solo nel piano più alto, con una soglia minima di postazioni.",
           "<b>Come entra la conoscenza aziendale.</b> È il punto su cui si gioca la differenza "
           "fra un giocattolo e uno strumento di lavoro, e merita il resto di questo articolo."]),
   ("note", "Nessuna di queste quattro risposte è stabile: cambiano ogni pochi mesi, in tutte le "
            "direzioni. Chiedile per iscritto al fornitore, con una data, e rifai la verifica "
            "prima del rinnovo."),

   ("h2", "Un solo piano di conoscenza, più superfici di esecuzione"),
   ("p", "L’errore architetturale più costoso che vedo è replicare la conoscenza dentro lo "
         "strumento: caricare i documenti nell’assistente, creare una base dati parallela, "
         "duplicare le procedure in un progetto. Funziona per due mesi. Poi le versioni "
         "divergono, e nessuno sa più quale sia quella buona — con l’aggravante che ora anche "
         "l’AI cita quella sbagliata, con sicurezza."),
   ("p", "L’impostazione che regge è l’opposto: <b>una sola fonte di verità</b>, dove i documenti "
         "già stanno, e più superfici che la leggono. Il repository aziendale resta il posto in "
         "cui si scrive; gli assistenti sono modi diversi di interrogarlo."),
   ("fig", "planes"),
   ("p", "Questo ha una conseguenza pratica importante: non devi scegliere un solo assistente per "
         "sempre. Se la conoscenza sta in un posto solo e i permessi sono quelli aziendali, "
         "cambiare superficie — o usarne due in parallelo per compiti diversi — costa poco. È "
         "l’unica forma di indipendenza dal fornitore realistica in questo mercato."),

   ("h2", "Indicizzato o dal vivo: due modi di leggere, due rischi diversi"),
   ("p", "Le piattaforme accedono ai documenti in due modi, e la differenza non è tecnica: cambia "
         "cosa puoi promettere al tuo ufficio compliance."),
   ("fig", "retrieval"),
   ("table", dict(head=["", "Indice sincronizzato", "Lettura dal vivo"],
     rows=[["Freschezza", "dipende dal ciclo di sincronizzazione", "sempre l’ultima versione"],
           ["Ambito", "selezionabile: siti e cartelle scelti dall’amministratore",
            "tutto ciò che l’utente è autorizzato a vedere"],
           ["Copia dei dati", "sì, un indice esiste da qualche parte", "no, nessuna copia persistente"],
           ["Tracciabilità", "buona: sai cosa è stato indicizzato", "più difficile: la ricerca è ampia per costruzione"],
           ["Domanda da fare", "chi possiede l’indice e per quanto vive?",
            "posso restringerlo a un perimetro, o solo ai permessi?"]])),
   ("p", "Nessuno dei due è “più sicuro”. L’indice è un perimetro che puoi disegnare; la lettura "
         "dal vivo è un perimetro che hai già — quello dei permessi — e che quasi nessuno ha "
         "davvero sotto controllo."),

   ("h2", "L’igiene dei permessi diventa improvvisamente un problema"),
   ("p", "In ogni organizzazione esistono documenti che una persona <i>potrebbe</i> tecnicamente "
         "aprire ma che non ha mai aperto, perché nessuno sa che esistono e la ricerca interna "
         "non li ha mai restituiti. L’AI li trova in tre secondi, e li cita."),
   ("p", "È il rispetto letterale dei permessi che avevi già, non una falla dello strumento. "
         "Il giorno in cui accende l’assistente, però, l’azienda scopre quanti "
         "<b>ereditati per sbaglio</b> ci sono nel repository. Per questo un progetto di adozione "
         "serio contiene sempre una revisione dei permessi <i>prima</i> del rilascio, non dopo il "
         "primo incidente."),
   ("ul", ["Cartelle con ereditarietà interrotta e permessi più larghi del previsto.",
           "Link di condivisione “chiunque abbia il link”, creati anni fa e mai scaduti.",
           "Archivi di progetti chiusi che nessuno ha mai riclassificato.",
           "Account di persone uscite ancora presenti nei gruppi."]),

   ("h2", "Il comportamento si governa a livelli, non a prompt"),
   ("p", "La seconda metà di quello che compri è il modo in cui l’assistente si comporta. Qui la "
         "tentazione è distribuire un documento con “le regole aziendali” e sperare che qualcuno "
         "lo incolli nelle conversazioni. Non succede."),
   ("p", "Le piattaforme enterprise offrono ormai una gerarchia, e conviene usarla per quello che "
         "è: uno strato costituzionale corto e stabile in cima, il metodo di reparto in mezzo, il "
         "contesto di progetto sotto, le preferenze personali in fondo."),
   ("fig", "layers"),
   ("p", "<mark>In cima va solo ciò che vale per tutti e cambia raramente.</mark> "
         "Le istruzioni di organizzazione hanno un limite di caratteri stretto — poche migliaia — "
         "ed è un bene: obbliga a scrivere principi, non manuali. Il metodo dettagliato sta nel "
         "livello sotto, dove può essere versionato e assegnato a chi serve."),

   ("h2", "Come si compra, in pratica"),
   ("p", "Una matrice decisionale con pesi espliciti è noiosa e funziona. La compilo con il "
         "cliente prima di vedere qualsiasi demo: dopo una demo ben fatta i pesi cambiano da "
         "soli, e non per ragioni difendibili."),
   ("table", dict(head=["Criterio", "Peso", "La domanda vera"],
     rows=[["Residenza e trattamento dei dati", "15%", "Dove stanno, dove si calcola, chi può accedervi"],
           ["Integrazione con il repository esistente", "15%", "Ambito selezionabile o solo permessi utente?"],
           ["Identità e provisioning", "10%", "Federazione e disattivazione automatica in che piano?"],
           ["Conservazione e audit", "10%", "Minimi, log esportabili, integrazione con il SIEM"],
           ["Capacità agentiche", "10%", "Compiti pianificati, azioni sui sistemi, con quali credenziali"],
           ["Ecosistema di estensioni", "10%", "Si possono versionare e assegnare per gruppo?"],
           ["Qualità sui vostri compiti", "10%", "Test su documenti veri, non su benchmark"],
           ["Esperienza d’uso", "5%", "Le persone lo aprirebbero di loro iniziativa?"],
           ["Costo e soglie", "10%", "Minimi di postazioni, scaglioni, cosa succede a 12 mesi"],
           ["Supporto e traiettoria", "5%", "Cosa è promesso, per quando, e per iscritto"]])),

   ("h2", "Quattro fasi, un trimestre"),
   ("fig", "phases"),
   ("ol", ["<b>Fondamenta.</b> Federazione dell’identità, gruppi, conservazione, chiavi se "
           "servono, istruzioni di organizzazione scritte e approvate. Nessun utente finale "
           "ancora. Due settimane se l’IT è disponibile.",
           "<b>Pilota.</b> Un reparto, tre flussi di lavoro scelti perché fanno male ogni "
           "settimana, cinque-dieci persone che li conoscono. Si misura tempo risparmiato e "
           "qualità, non entusiasmo.",
           "<b>Distribuzione.</b> Quello che ha funzionato nel pilota diventa procedura "
           "assegnata al gruppo giusto. Formazione breve e ripetuta, non un webinar da due ore.",
           "<b>Esercizio.</b> Revisione periodica delle procedure create dalle persone, dei "
           "costi, dei permessi. È la fase che nessuno pianifica ed è l’unica che dura."]),

   ("h2", "Gli errori che vedo più spesso"),
   ("ul", ["<b>Comprare per tutti al primo giorno.</b> Centoventi licenze accese insieme "
           "producono venti utenti veri e cento delusi. Meglio venti licenze e una lista d’attesa.",
           "<b>Far scrivere le regole all’ufficio sbagliato.</b> Se le istruzioni aziendali le "
           "scrive solo il legale, l’assistente diventa un disclaimer. Se le scrive solo il "
           "reparto tecnico, nessuno le rispetta.",
           "<b>Confondere distribuzione e sicurezza.</b> Assegnare un’estensione a un gruppo "
           "serve a far trovare le cose, non a impedire accessi: il confine di sicurezza restano "
           "i permessi del repository.",
           "<b>Misurare l’adozione con il numero di licenze attive.</b> Misura invece quanti "
           "processi sono cambiati: è un numero più piccolo e molto più vero."]),

   ("h2", "Da dove partire lunedì"),
   ("p", "Prima di ogni altra cosa, apri il repository e guarda i permessi: cartelle con "
         "ereditarietà interrotta, link pubblici mai scaduti, gruppi con dentro chi ha lasciato "
         "l’azienda. È una settimana di lavoro noioso e mette al riparo dall’unico incidente che "
         "in questi progetti si ricorda per anni. Poi scrivi le due pagine di istruzioni "
         "aziendali, scegli tre processi che fanno male ogni settimana, e comincia da lì."),
  ]),

dict(
  draft=True,
  slug="ecosistema-non-abbonamento",
  date="2026-08-26", human_date="26 agosto 2026", read=9,
  tags=["Architettura", "Skill", "Knowledge"],
  title="Un ecosistema, non un abbonamento",
  dek="Istruzioni di organizzazione, procedure versionate, contesto di progetto e una "
      "convenzione documentale che dice all’AI dove guardare. Come si costruisce lo strato "
      "aziendale sopra una piattaforma che non hai scritto tu.",
  body=[
   ("p", "Una licenza dà accesso a un modello. Perché quel modello lavori <i>come lavora la tua "
         "azienda</i> servono quattro oggetti, e nessuno dei quattro è un prompt lungo."),

   ("h2", "1. Istruzioni di organizzazione: la costituzione, non il manuale"),
   ("p", "Poche migliaia di caratteri, presenti in ogni conversazione di ogni persona. Vanno "
         "trattate come una costituzione: principi che cambiano raramente e che valgono per "
         "tutti. Chi siamo, come si scrive qui dentro, cosa non esce mai da qui, quando bisogna "
         "andare a leggere le fonti interne invece di rispondere a memoria, come si distingue un "
         "dato certo da una deduzione."),
   ("p", "La metodologia di un reparto, gli elenchi di template e i casi particolari stanno "
         "altrove: occupano lo spazio di tutti per servire pochi."),

   ("h2", "2. Procedure versionate, assegnate a chi servono"),
   ("p", "Il metodo di lavoro sta un livello sotto, in unità che si possono scrivere, rivedere e "
         "distribuire: come si prepara una proposta, come si controlla la qualità di un "
         "deliverable, come si struttura una ricerca. Le piattaforme serie oggi permettono di "
         "raggrupparle e assegnarle per gruppo — richieste, preinstallate, disponibili o "
         "nascoste — e di sincronizzarle da un repository di codice."),
   ("p", "Se le procedure vivono in un repository hanno una storia, una revisione e un rilascio. "
         "Se vivono in un documento condiviso, dopo tre mesi ne esistono quattro versioni e due "
         "sono sbagliate."),
   ("note", "Assegnare per gruppo è distribuzione, non sicurezza. Serve a far trovare la cosa "
            "giusta alla persona giusta; non impedisce a nessuno di leggere ciò che i permessi "
            "del repository gli consentono già."),

   ("h2", "3. Contesto di progetto, senza duplicare la conoscenza"),
   ("p", "Ogni progetto o cliente merita il proprio spazio persistente: istruzioni specifiche, "
         "memoria, conversazioni condivise fra chi ci lavora. La tentazione è caricarci dentro "
         "anche i documenti. Non farlo, se non per il minimo indispensabile: il progetto "
         "descrive <i>come si lavora qui</i>, la conoscenza resta nel repository e viene letta "
         "quando serve."),

   ("h2", "4. Una convenzione che dice all’AI dove guardare"),
   ("p", "In ogni spazio documentale importante, che sia un reparto, un programma o un cliente, "
         "un file breve con lo stesso nome ovunque, che non contiene la conoscenza ma la "
         "<b>mappa</b>. Costa mezza giornata e cambia la qualità delle risposte più di qualsiasi "
         "altra cosa in questo elenco."),
   ("ul", ["di cosa si occupa questo spazio, in tre righe;",
           "quali sono le fonti autorevoli e quali invece sono bozze da ignorare;",
           "il glossario dei termini e degli acronimi che qui significano qualcosa di preciso;",
           "i vincoli noti: cosa non si può dire, cosa va sempre citato;",
           "dove stanno i template e i deliverable finiti."]),
   ("p", "Poi una procedura aziendale che dice all’assistente di cercare quel file prima di "
         "mettersi a leggere tutto. Il guadagno non è teorico: invece di far scorrere duecento "
         "documenti, gli dai la mappa semantica del posto in cui è appena entrato. È la "
         "differenza fra un nuovo assunto lasciato davanti a un archivio e un nuovo assunto con "
         "mezz’ora di affiancamento."),

   ("h2", "Il livello personale, deliberatamente debole"),
   ("p", "Le preferenze individuali servono: ruolo, lingua, quanto sintetico deve essere "
         "l’output. Ma se in quel livello finisce il metodo aziendale, hai centoventi metodologie "
         "leggermente diverse e nessuna che si possa aggiornare. Tienilo povero apposta."),

   ("h2", "Cosa ne esce"),
   ("p", "La conoscenza sta in un posto, il comportamento in un altro, e l’assistente è la "
         "superficie che li mette insieme. Quando fra un anno cambierai idea sul fornitore, e "
         "probabilmente la cambierai, riscriverai le procedure e non l’azienda."),
  ]),

dict(
  draft=True,
  slug="prima-di-accendere",
  date="2026-08-26", human_date="26 agosto 2026", read=6,
  tags=["Governance", "Sicurezza", "Checklist"],
  title="Undici cose da sistemare prima di accendere l’AI in azienda",
  dek="Una lista corta, in ordine di quanto fa male sbagliarla. Serve a evitare che il primo "
      "mese di adozione diventi il primo mese di incidenti.",
  body=[
   ("p", "Questa lista nasce da progetti veri e va usata come si usa una checklist di volo: si "
         "legge tutta, anche le voci ovvie, e si spunta prima di partire."),
   ("ol", ["<b>Revisione dei permessi del repository.</b> Ereditarietà interrotte, link pubblici "
           "mai scaduti, archivi mai riclassificati. È la voce che produce il rischio più "
           "grande e la meno divertente da fare.",
           "<b>Disattivazione degli account.</b> Verifica che chi lascia l’azienda perda "
           "l’accesso automaticamente, non con un ticket.",
           "<b>Politica di conservazione decisa e scritta.</b> Con la data in cui è stata "
           "decisa e chi l’ha approvata.",
           "<b>Residenza dei dati verificata per iscritto</b>, distinguendo archiviazione e "
           "calcolo.",
           "<b>Istruzioni di organizzazione approvate</b> da legale, sicurezza e da chi il "
           "lavoro lo fa davvero.",
           "<b>Classificazione minima delle informazioni.</b> Anche solo tre livelli, purché "
           "esistano e siano riconoscibili in un nome di cartella.",
           "<b>Regola sulle fonti esterne.</b> Se e quando l’assistente può cercare sul web, e "
           "cosa non può mai uscire nella query.",
           "<b>Registro di chi può creare procedure</b> condivise, e chi le rivede prima che "
           "diventino aziendali.",
           "<b>Log esportabili verso i vostri sistemi</b>, provati una volta davvero, non solo "
           "documentati.",
           "<b>Un canale per segnalare risposte sbagliate</b>, con qualcuno che le legge. Senza, "
           "gli errori diventano leggende interne.",
           "<b>Tre metriche decise prima</b> di partire: quanto tempo, su quale processo, "
           "misurato come."]),
   ("note", "Se dovessi tenerne solo tre: permessi, conservazione, e il canale per segnalare gli "
            "errori. Le altre otto si recuperano; queste tre no."),
  ]),
]


def published():
    """The posts that actually reach the site. Drafts stay in this file — they
    are written, not published — and produce no page, no feed entry, no link."""
    return [p for p in POSTS if not p.get("draft")]


# ---------------------------------------------------------------- rendering
def render_blocks(blocks):
    out = []
    for kind, payload in blocks:
        if kind in ("h2", "h3"):
            anchor = "".join(c.lower() if c.isalnum() else "-" for c in payload).strip("-")
            out.append(f'<{kind} id="{anchor}">{payload}</{kind}>')
        elif kind == "p":
            out.append(f"<p>{payload}</p>")
        elif kind in ("ul", "ol"):
            items = "".join(f"<li>{i}</li>" for i in payload)
            out.append(f"<{kind}>{items}</{kind}>")
        elif kind == "fig":
            out.append(f'<figure class="bfigwrap">{FIGURES[payload]()}</figure>')
        elif kind == "note":
            out.append(f'<aside class="bnote">{payload}</aside>')
        elif kind == "table":
            head = "".join(f"<th>{h}</th>" for h in payload["head"])
            rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                           for r in payload["rows"])
            out.append(f'<div class="btable"><table><thead><tr>{head}</tr></thead>'
                       f"<tbody>{rows}</tbody></table></div>")
    return "\n".join(out)


def toc(blocks):
    items = []
    for kind, payload in blocks:
        if kind == "h2":
            anchor = "".join(c.lower() if c.isalnum() else "-" for c in payload).strip("-")
            items.append(f'<a href="#{anchor}">{payload}</a>')
    return "".join(items)


def chips(tags):
    return "".join(f'<span class="chip">{t}</span>' for t in tags)
