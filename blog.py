# -*- coding: utf-8 -*-
"""Blog content and rendering.

Kept out of build.py: the posts are long, and the site generator is already a
big file. build.py imports POSTS, figures() and the two page renderers.
"""

BLOG_LABELS = {
    "it": dict(kicker="Blog", title="Appunti",
               lede="Osservazioni, ricerche e cose imparate lavorando.",
               read="min di lettura", back="← Tutti gli articoli", updated="Pubblicato",
               toc="In questa pagina", more="Continua a leggere",
               note="Gli articoli sono in italiano.",
               empty_h="Non ci sono articoli al momento.",
               empty_p="Sto scrivendo. Qui finiranno note su acquisto, governance e adozione "
                       "dell’AI in azienda — quello che imparo sul campo, non quello che si "
                       "legge ovunque."),
    "en": dict(kicker="Blog", title="Notes",
               lede="Observations, research and things learned through the work.",
               read="min read", back="← All posts", updated="Published",
               toc="On this page", more="Keep reading",
               note="Articles are available in English.",
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



def fig_loop():
    """Trace, proposal, human review, skill box — and back into use."""
    return """
<svg viewBox="0 0 900 340" class="bfig" role="img"
     aria-label="Dalle tracce alla skill approvata">
  <g fill="none" stroke="currentColor" stroke-opacity=".28">
    <rect x="20"  y="128" width="200" height="84"/>
    <rect x="290" y="128" width="200" height="84"/>
    <rect x="660" y="24"  width="220" height="84"/>
  </g>
  <rect x="290" y="24" width="200" height="84" fill="none" stroke="var(--acc)"/>
  <rect x="660" y="232" width="220" height="84" fill="none" stroke="currentColor" stroke-opacity=".28"/>
  <g fill="none" stroke="currentColor" stroke-opacity=".4">
    <path d="M220 170h70"/>
    <path d="M390 128V108"/>
    <path d="M490 66h170"/>
    <path d="M770 108v124"/>
  </g>
</svg>"""


def fig_cost():
    """Three relative adaptation costs, labelled in the HTML caption."""
    out = ['<svg viewBox="0 0 900 210" class="bfig" role="img" '
           'aria-label="Tre livelli di adattamento, in ordine di costo">']
    widths = [230, 410, 820]
    y = 30
    for i, w in enumerate(widths):
        acc = ' stroke="var(--acc)"' if i == 2 else ' stroke="currentColor" stroke-opacity=".3"'
        fill = ' fill="var(--acc)" fill-opacity=".12"' if i == 2 else ' fill="none"'
        out.append(f'<rect x="30" y="{y}" width="{w}" height="40"{fill}{acc}/>')
        y += 62
    out.append("</svg>")
    return "".join(out)


FIGURES = {"planes": fig_planes, "layers": fig_layers,
           "retrieval": fig_retrieval, "phases": fig_phases,
           "loop": fig_loop, "cost": fig_cost}


# ---------------------------------------------------------------- posts
# Blocks: ("h2"|"h3"|"p"|"ul"|"ol"|"fig"|"note"|"table", payload)
POSTS = [
dict(
  slug="agente-che-dimentica-ogni-notte",
  date="2026-08-31", human_date="31 agosto 2026", read=12,
  tags=["Agenti AI", "Memoria", "Architettura"],
  og_image="/assets/img/og-adaptive-agents.png",
  hero_image="/assets/img/og-adaptive-agents.png",
  title="Building Adaptive AI Agents: il nuovo corso su DeepLearning.AI",
  dek="Un agente aziendale non dovrebbe ricominciare da capo a ogni chat. Il corso di "
      "DeepLearning.AI sugli agenti adattivi mostra un metodo concreto: raccogliere tracce, "
      "approvare procedure riutilizzabili, strutturare la conoscenza e lasciare i pesi del "
      "modello per ultimi.",
  body=[
   ("p", "Lunedì un agente interno deve rispondere a una richiesta di rimborso spese. Scopre "
         "che la policy valida non è nel PDF allegato ma in una versione pubblicata tre mesi "
         "prima sull'intranet, la trova e risponde bene. Martedì un altro collega fa la stessa "
         "domanda in una chat nuova. L'agente riparte dal PDF sbagliato e qualcuno deve "
         "correggerlo di nuovo."),
   ("p", "Lo scenario viene quasi parola per parola da <i>Building Adaptive AI Agents</i>, il "
         "corso di DeepLearning.AI che parte da un coding agent capace di ripetere lo stesso "
         "errore sui test. Il problema non è limitato al codice: riguarda ciò che un agente "
         "riesce a trattenere fra una conversazione e la successiva, sia che scriva Python, "
         "gestisca rimborsi o prepari una bozza di contratto."),
   ("p", "Senza un modo per trattenere e riusare ciò che ha imparato, l'agente paga ogni giorno "
         "lo stesso costo. Solo che quel costo finisce disperso in centinaia di chat, invece di "
         "comparire in una fattura."),

   ("h2", "Tre livelli, non uno"),
   ("p", "Il corso ordina per costo tre modi per far migliorare un agente. I primi due agiscono "
         "sul contesto che legge prima di rispondere, il <b>token space</b>: procedure "
         "riutilizzabili e una struttura migliore per cercare conoscenza. Il terzo modifica i "
         "pesi del modello, il <b>weight space</b>, e conviene considerarlo solo dopo."),
   ("fig", "cost"),
   ("p", "I primi due livelli si aggiornano in minuti: basta scrivere un file o aggiungere un "
         "nodo a un grafo. Il terzo richiede addestramento e hardware dedicato; inoltre va "
         "rifatto quando cambia la policy sottostante. Per insegnare una nuova regola aziendale, "
         "partire dai pesi del modello significa scegliere il livello più costoso."),

   ("h2", "Dalle tracce alla procedura approvata"),
   ("p", "Il primo livello si chiama <i>skill induction</i>. Si registrano conversazioni, chiamate "
         "a strumenti, errori e correzioni, poi un modello le condensa in una procedura breve: "
         "cosa fare quando torna lo stesso tipo di richiesta."),
   ("fig", "loop"),
   ("p", "La revisione umana decide se quella procedura diventa comportamento. Quando una skill "
         "viene approvata, l'agente la recupera per ogni richiesta simile finché qualcuno non "
         "la modifica. Se passa una skill sbagliata, l'errore si replica a ogni uso."),
   ("note", "Le tracce non sono fonti affidabili per definizione. Un'istruzione sbagliata, o inserita "
            "apposta con un tool call malevolo, può sembrare una skill candidata. La revisione serve "
            "a fermarla prima che venga riutilizzata."),
   ("p", "Ogni skill approvata dovrebbe avere un responsabile e una motivazione scritta, anche "
         "quando viene respinta. Senza quel contesto il sistema non può migliorare la proposta: "
         "può solo ripresentarla."),

   ("h2", "Trovare la conoscenza giusta"),
   ("p", "Il secondo livello riguarda l'organizzazione della conoscenza consultata dall'agente. "
         "Il corso lo mostra su una base di codice, ma la dinamica è comune: quando la base "
         "cresce, trovare il documento da cui partire può richiedere più lavoro che scrivere la "
         "risposta. La ricerca per parole chiave trova il termine cercato e lascia indietro "
         "documenti collegati che non lo contengono."),
   ("p", "La proposta è un grafo di relazioni tra documenti: cosa richiama cosa, cosa si aggiorna "
         "insieme, cosa dipende da cosa. Nel codice sono import, chiamate di funzione e modifiche "
         "nello stesso commit. In azienda sono policy collegate, procedure che cambiano insieme e "
         "contratti riferiti allo stesso fornitore."),
   ("p", "Il recupero avviene in due passaggi. Prima trova il nodo semanticamente più vicino alla "
         "domanda; poi percorre il grafo con un algoritmo di ranking simile a PageRank. Così non "
         "tratta allo stesso modo tutto ciò che è a un passaggio di distanza."),
   ("table", dict(head=["", "Ricerca per parole chiave", "Grafo di conoscenza"], rows=[
      ["Trova ciò che è collegato ma non nominato", "No", "Sì"],
      ["Costo di aggiungere un documento nuovo", "Basso", "Quasi zero"],
      ["Serve deduplicare i quasi-doppioni", "—", "Sì, altrimenti il grafo si sporca"],
      ["Risultato sui compiti multi-hop testati", "Manca il nodo giusto", "Lo trova"]])),
   ("p", "Nei benchmark del corso, il grafo ha ridotto dell'11-18% il tempo sul compito, del "
         "7-36% i passaggi alla prima modifica corretta e del 3-16% i token, su repository "
         "Django e HTTPie. Le percentuali non si trasferiscono automaticamente a un'azienda, ma "
         "spiegano perché un indice piatto smette di bastare quando le relazioni diventano parte "
         "del problema."),
   ("note", "Un grafo richiede manutenzione. Nel test del corso, circa il 4% dei nodi era quasi "
            "duplicato al 96% e andava rimosso prima che il recupero tornasse affidabile. Due copie "
            "della stessa policy in cartelle diverse sono rumore."),

   ("h2", "Quando toccare i pesi del modello"),
   ("p", "Il terzo livello modifica i pesi del modello. Un modello di base ha già assorbito una "
         "quantità enorme di testo; per aggiungere una policy o una conoscenza che cambia spesso, "
         "riscriverne i pesi è di solito più costoso che fornirla come contesto al momento giusto."),
   ("p", "Il fine-tuning ha senso per compiti diversi: rendere affidabile un rifiuto, oppure "
         "adattare formato e tono delle risposte. LoRA, la tecnica più comune, congela i pesi "
         "originali e allena due matrici piccole. Si interviene su circa l'1% dei parametri."),
   ("p", "Se si allenano troppi parametri, si rischia il <i>catastrophic forgetting</i>: il modello "
         "perde parte di ciò che sapeva perché i pesi originali vengono sovrascritti. Il costo "
         "cresce con la dimensione del modello. Nel corso, un adattatore per 600 milioni di "
         "parametri si allena in un'ora; sul modello di frontiera equivalente servirebbero "
         "centinaia o migliaia di ore di calcolo."),
   ("p", "In produzione un instradatore può mandare una richiesta tecnica al modello di base e una "
         "richiesta di tono all'adattatore corrispondente, senza chiedere all'utente di scegliere."),

   ("h2", "Perché questo vale per qualsiasi agente interno"),
   ("p", "Il corso usa coding agent perché lì esistono benchmark pubblici e codice open source. I "
         "tre livelli valgono anche altrove. Un agente che risponde sulle policy HR, prepara "
         "bozze contrattuali o smista ticket ha tracce da cui imparare e documenti che possono "
         "essere organizzati come un grafo."),
   ("p", "Per un agente interno, il punto di partenza è pratico: decidere quali correzioni diventano "
         "procedure riutilizzabili, chi le approva e dove cerca la conoscenza. Il fine-tuning "
         "rimane una scelta specifica per comportamento e formato, non il modo normale per "
         "aggiornare una regola che cambierà fra tre mesi."),
  ]),
dict(
  slug="tutti-odiano-cookie-banner-europa-divisa-soluzione-digital-omnibus",
  date="2026-08-31", human_date="31 agosto 2026", read=15,
  tags=["Privacy", "Advertising", "Regolazione europea"],
  og_image="/assets/img/og-cookie-banner.png",
  hero_image="/assets/img/og-cookie-banner.png",
  title="Tutti odiano i cookie banner. È sulla soluzione che l’Europa si sta dividendo",
  dek="Sul problema c’è un consenso quasi universale. Il conflitto comincia quando bisogna decidere "
      "quali attività possono avvenire senza consenso, chi deve trasmettere le preferenze e quale "
      "modello economico di Internet si vuole proteggere.",
  body=[
   ("p", "Il 19 novembre 2025 la Commissione europea ha presentato il Digital Omnibus, una proposta "
         "che modifica una lunga serie di norme digitali esistenti e che, fra le altre cose, prova a "
         "risolvere uno dei risultati più paradossali della regolazione europea di Internet: per dare "
         "agli utenti maggiore controllo sui propri dati abbiamo costruito un sistema nel quale milioni "
         "di persone rispondono ogni giorno alla stessa domanda, spesso senza leggerla."),
   ("p", "La Commissione lo chiama <i>consent fatigue</i>. E su questo, curiosamente, quasi tutti gli "
         "attori coinvolti sembrano concordare. EDPB ed EDPS considerano necessario intervenire sulla "
         "proliferazione dei cookie banner; l’industria pubblicitaria sostiene che l’attuale sistema "
         "abbia trasformato il consenso in un adempimento ripetitivo; le associazioni dei consumatori "
         "ammettono che esprimere le proprie preferenze sito per sito sia inefficiente; persino le forze "
         "politiche più diffidenti verso la riapertura del GDPR non difendono seriamente lo status quo."),
   ("p", "Il conflitto comincia quando si prova a decidere cosa mettere al suo posto."),
   ("cards", [("Il problema", "<mark>Consent fatigue</mark>: la stessa scelta viene riproposta sito per sito."),
              ("La proposta", "Meno eccezioni da chiedere e preferenze trasmesse in modo <mark>machine-readable</mark>."),
              ("La domanda", "Chi controlla il consenso: l’utente, il publisher o il browser?")]),

   ("h2", "Meno banner, ma come?"),
   ("p", "La proposta della Commissione interviene su due fronti. Con il nuovo articolo 88a del GDPR "
         "allargherebbe alcune eccezioni al consenso per l’accesso alle informazioni memorizzate nel "
         "terminale dell’utente, introducendo fra l’altro un’eccezione per determinate forme di audience "
         "measurement. Con l’articolo 88b permetterebbe invece di esprimere alcune preferenze attraverso "
         "segnali automatizzati e machine-readable: in sostanza, il browser o il sistema operativo "
         "potrebbero comunicare ai siti la scelta dell’utente, evitando di porgli continuamente la stessa "
         "domanda."),
   ("p", "Il consenso continuerebbe a essere la regola generale, ma con meno occasioni nelle quali sarebbe "
         "necessario richiederlo e con la possibilità di rendere persistente la risposta. È il primo "
         "punto, quello delle eccezioni, ad avere conseguenze particolarmente interessanti per "
         "l’advertising."),

   ("h2", "Il confine fra measurement e tracking"),
   ("p", "L’11 febbraio 2026 EDPB ed EDPS hanno pubblicato la propria Joint Opinion sul Digital Omnibus e, "
         "anziché respingere l’impostazione della Commissione, hanno sostenuto esplicitamente l’obiettivo "
         "di ridurre la consent fatigue e hanno accolto favorevolmente l’introduzione di alcune deroghe "
         "limitate. Sull’audience measurement hanno però tracciato un confine molto stretto: la misurazione "
         "dovrebbe produrre <mark>informazioni aggregate e anonime</mark> sull’utilizzo del servizio, senza combinare "
         "quei dati con quelli provenienti da altri servizi, senza riutilizzarli per altri scopi e senza "
         "condividerli con terzi."),
   ("p", "Subito dopo fanno però qualcosa di ancora più interessante. Propongono ai legislatori di prendere "
         "in considerazione una nuova eccezione per il <mark>contextual advertising</mark>, più rispettoso della "
         "privacy del behavioural advertising quando dipende esclusivamente dalla pagina che l’utente sta "
         "visitando o dalla ricerca che sta effettuando in quel momento, senza conservarne o collegarne "
         "l’attività passata e futura."),
   ("p", "EDPB ed EDPS riconoscono anche che una campagna contextual deve comunque essere gestita e misurata: "
         "citano esplicitamente frequency capping, advertising audience measurement e prevenzione delle "
         "click fraud come attività che possono richiedere tracker, e sostengono che questi casi potrebbero "
         "essere inclusi fra quelli che non richiedono consenso, purché l’eccezione sia strettamente "
         "delimitata."),
   ("note", "La posizione non dice che measurement e tracking siano la stessa cosa, ma nemmeno che qualsiasi "
            "cosa venga chiamata “measurement” debba essere automaticamente esentata. Il rischio dipende "
            "da ciò che tecnicamente viene fatto con il dato."),

   ("h2", "La prima frattura: il rischio"),
   ("p", "L’EPP, e in particolare Aura Salla, co-rapporteur del dossier per la commissione ITRE, sostiene un "
         "approccio maggiormente basato sul rischio: ridurre i banner inutili, aumentare la certezza "
         "giuridica e rendere più semplice per le imprese europee utilizzare i dati, senza abbandonare le "
         "garanzie fondamentali. Salla insiste anche su un secondo argomento che ritorna continuamente nel "
         "dibattito: una regolazione mal progettata può finire per rafforzare proprio le grandi piattaforme "
         "americane che l’Europa vorrebbe rendere meno dominanti."),
   ("p", "Nell’ECR la posizione appare ancora più esplicitamente orientata alla proporzionalità. Diego Solier "
         "ha indicato audience measurement, advertising, cybersecurity updates e fraud prevention come "
         "esempi nei quali bisognerebbe evitare che attività relativamente poco intrusive vengano trattate "
         "allo stesso modo del behavioural tracking."),
   ("p", "S&D parte da una preoccupazione diversa. Marina Kaljurand, co-rapporteur LIBE, sostiene anch’essa "
         "un’applicazione risk-based del GDPR, ma insiste sulla necessità di non utilizzare il Digital "
         "Omnibus per indebolire definizioni e protezioni fondamentali, a partire dalla definizione stessa "
         "di personal data. La posizione socialista non è quindi “manteniamo tutti i cookie banner”, ma: "
         "semplifichiamo senza creare, attraverso le eccezioni, nuovi spazi nei quali attività invasive "
         "possano essere riclassificate come innocue."),
   ("p", "Renew occupa una posizione intermedia. Michael McNamara ha parlato della necessità di ottenere una "
         "“genuine simplification” mantenendo però le garanzie sui diritti fondamentali: una posizione meno "
         "nettamente schierata sui singoli strumenti e più concentrata sulla ricerca di un compromesso "
         "tecnicamente funzionante."),
   ("p", "Greens/EFA e The Left sono molto più sospettosi verso l’intero esercizio di semplificazione. I Greens "
         "hanno avvertito fin dall’inizio che riaprire GDPR ed ePrivacy potrebbe trasformarsi in un regalo "
         "alle grandi piattaforme e hanno chiesto soprattutto migliore enforcement delle regole esistenti. "
         "Markéta Gregorová ha comunque sostenuto la necessità di trovare una vera soluzione per eliminare "
         "i cookie banner nella forma attuale: anche qui il dissenso riguarda più il metodo che il problema. "
         "The Left interpreta invece la proposta come un possibile arretramento degli interessi dei "
         "consumatori e della protezione dei dati."),
   ("p", "Persino all’interno delle posizioni più conservatrici o nazionaliste non emerge un’unica linea sui "
         "cookie. Patriots for Europe, per esempio, nel dibattito sul dossier ha concentrato molta attenzione "
         "sulla pseudonimizzazione e sulla certezza giuridica più che su una specifica architettura del "
         "consenso. Parlare semplicemente di “destra contro sinistra” farebbe quindi perdere una parte "
         "importante della storia."),
   ("cards", [("EPP · ECR", "<mark>Proporzionalità e competitività</mark>: distinguere attività poco intrusive dal behavioural tracking."),
              ("S&D · Renew", "Semplificare, ma senza <mark>nuove scappatoie</mark> nelle protezioni fondamentali."),
              ("Greens · The Left", "Più enforcement e cautela: il rischio è fare un <mark>regalo alle piattaforme</mark>.")]),

   ("h2", "La seconda frattura: il potere"),
   ("p", "Fuori dal Parlamento il conflitto diventa ancora più chiaro. IAB Europe accetta l’obiettivo della "
         "Commissione ma sostiene che le eccezioni dell’articolo 88a siano troppo strette. Il suo argomento "
         "è che continuare a richiedere consenso per operazioni operative e a basso rischio non elimina "
         "davvero la consent fatigue; allo stesso tempo si oppone a un sistema di consenso centralizzato "
         "nel browser, perché teme che possa danneggiare l’ecosistema dei contenuti finanziati dalla "
         "pubblicità e aumentare il potere dei grandi intermediari tecnologici."),
   ("p", "Alliance Digitale, l’associazione francese del marketing e dei dati, arriva a una conclusione "
         "affine: considera il meccanismo centralizzato dell’articolo 88b un rischio per proporzionalità, "
         "concorrenza e neutralità tecnologica; chiede invece eccezioni per attività a basso rischio, "
         "fra cui contextual advertising, frequency capping, antifrode e analytics aggregate."),
   ("p", "EuroCommerce sostiene una posizione molto simile: più eccezioni risk-based per trattamenti a basso "
         "rischio, maggiore riconoscimento delle privacy-enhancing technologies, ma niente obbligo "
         "generalizzato di gestire le preferenze attraverso il browser e niente divieto rigido di riproporre "
         "il consenso per sei mesi. Il timore dichiarato è la nascita di nuovi gatekeeper."),
   ("p", "Il problema è intuitivo. Se la preferenza dell’utente viene espressa principalmente attraverso "
         "Chrome o Safari, Google e Apple smettono di essere soltanto produttori di browser e diventano un "
         "<mark>pezzo dell’infrastruttura attraverso cui viene esercitato un diritto giuridico.</mark> La Commissione "
         "vede in questo la possibilità di risolvere finalmente la cookie fatigue; una parte dell’industria "
         "vede invece il rischio di trasferire potere dai publisher a due delle aziende più grandi del mondo."),
   ("p", "BEUC, che rappresenta le organizzazioni europee dei consumatori, guarda la stessa architettura dalla "
         "prospettiva opposta. Accoglie con cautela i browser signal proprio perché potrebbero rendere più "
         "semplice esercitare il consenso, ma chiede che il consenso rimanga il criterio di fondo e che le "
         "eccezioni siano definite con molta maggiore precisione. BEUC è inoltre favorevole alla possibilità "
         "di riconoscere un trattamento specifico al contextual advertising, purché questo non diventi una "
         "scorciatoia per la profilazione."),
   ("p", "EDRi spinge ancora più avanti questa critica. Secondo l’organizzazione, la cookie fatigue non nasce "
         "principalmente dai banner, ma da un modello economico costruito sul tracking, dall’utilizzo di "
         "interfacce manipolative e da un enforcement insufficiente. Eliminare il sintomo senza modificare "
         "gli incentivi economici che hanno prodotto il problema rischierebbe quindi semplicemente di rendere "
         "il tracking meno visibile."),

   ("h2", "Tre conflitti, non uno"),
   ("p", "La Commissione ha prodotto una soluzione apparentemente semplice a un problema sul quale esiste un "
         "consenso quasi universale, ma ha aperto contemporaneamente almeno tre conflitti diversi."),
   ("cards", [("01 — Il rischio", "Quali attività sono abbastanza poco invasive da poter avvenire senza consenso?"),
              ("02 — Il potere", "Chi deve raccogliere e trasmettere le preferenze: il publisher o il browser?"),
              ("03 — Il modello", "Quanto si può limitare il behavioural tracking senza compromettere media e servizi gratuiti?")]),
   ("p", "Anche il Consiglio ha mostrato quanto sia difficile tenere insieme queste domande. In un compromise "
         "text del 17 aprile la presidenza aveva incluso una nuova eccezione per il contextual advertising, "
         "andando nella direzione indicata da EDPB ed EDPS. A giugno, però, gli Stati membri hanno eliminato "
         "dal compromesso alcune delle principali disposizioni sulla semplificazione dei cookie banner, "
         "rinviando sostanzialmente il nodo."),
   ("p", "Al Parlamento il processo è ancora aperto. Il draft report di Salla e Kaljurand è arrivato a giugno; "
         "a luglio sono stati presentati più di mille emendamenti e il prossimo passaggio sarà negoziare i "
         "compromise amendments prima del voto in commissione. Al 31 agosto il fascicolo ufficiale "
         "2025/0360(COD) risulta ancora “Awaiting committee decision”."),

   ("h2", "Cosa cambia per l’ecosistema pubblicitario"),
   ("p", "Per l’ecosistema pubblicitario, il risultato potrebbe essere molto più importante della semplice "
         "scomparsa di qualche banner. Un trattamento normativo più favorevole al contextual advertising "
         "renderebbe economicamente più interessante un advertising che utilizza il contesto della pagina "
         "anziché la storia dell’individuo. Eccezioni chiaramente definite per audience measurement, frequency "
         "capping e antifrode renderebbero possibile separare alcune funzioni operative della pubblicità dal "
         "behavioural profiling."),
   ("p", "Una forte implementazione dei browser signals potrebbe invece ridurre drasticamente il numero di "
         "utenti disponibili per certe forme di tracking, ma contemporaneamente aumentare il potere di browser "
         "e sistemi operativi. Publisher e retailer avrebbero quindi un incentivo ancora maggiore a sviluppare "
         "first-party data e relazioni dirette con gli utenti."),
   ("cards", [("Contextual", "Il valore dell’inserzione dipende dalla pagina, non dalla storia della persona."),
              ("Measurement", "Misurare campagne, frequenza e frodi senza trasformare tutto in profiling."),
              ("First-party", "Publisher e retailer hanno un incentivo più forte a costruire relazioni dirette.")]),
   ("p", "C’è infine un problema di measurement che merita di essere osservato con attenzione, senza attribuire "
         "al legislatore conclusioni che non ha tratto. Il Digital Omnibus non sta proponendo nuovi modelli di "
         "Marketing Effectiveness e non sta dicendo alle aziende di sostituire attribution con incrementality "
         "o Marketing Mix Modeling. Sta però introducendo una distinzione regolatoria molto significativa: "
         "<mark>non tutte le attività necessarie a misurare una campagna richiedono necessariamente di ricostruire "
         "il comportamento di una persona attraverso servizi diversi.</mark>"),
   ("p", "È una distinzione che l’advertising digitale ha avuto poca necessità di fare finché la stessa "
         "infrastruttura tecnica poteva occuparsi contemporaneamente di targeting, tracking, attribution e "
         "measurement. Ora potrebbe essere costretto a farla."),

   ("h2", "Cosa ognuno vuole salvare"),
   ("p", "La cosa più sorprendente del dibattito europeo sui cookie è che nessuno sembra realmente voler salvare "
         "i cookie banner. Ognuno sta cercando invece di salvare qualcosa di diverso dalla loro scomparsa: "
         "EDPB ed EDPS la proporzionalità fra rischio e trattamento; l’industria pubblicitaria la capacità di "
         "finanziare e misurare advertising e contenuti; i publisher il rapporto diretto con il proprio "
         "pubblico; i consumatori il controllo effettivo; Greens e digital-rights organisations l’integrità "
         "delle protezioni esistenti; EPP ed ECR la competitività e la possibilità per le imprese europee di "
         "usare i dati; S&D e Renew un compromesso che semplifichi senza aprire nuove scappatoie."),
   ("p", "E dietro tutti loro rimane una domanda molto più importante di quella che compare sul banner quando "
         "apriamo un sito: non se cliccheremo ancora “Accept all”, ma chi avrà il diritto di osservare cosa "
         "facciamo dopo, per quale scopo e con quale livello di dettaglio."),
   ("h2", "Fonti e documenti"),
   ("ul", ["<a href=\"https://digital-strategy.ec.europa.eu/en/library/digital-omnibus-regulation-proposal\" target=\"_blank\" rel=\"noopener\">Commissione europea — proposta Digital Omnibus</a>",
           "<a href=\"https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025%2F0360%28COD%29\" target=\"_blank\" rel=\"noopener\">Parlamento europeo — fascicolo 2025/0360(COD)</a>",
           "<a href=\"https://www.edpb.europa.eu/system/files/documents/2026-02/edpb_edps_jointopinion_202602_digitalomnibus_en.pdf\" target=\"_blank\" rel=\"noopener\">EDPB e EDPS — Joint Opinion sul Digital Omnibus (11 febbraio 2026)</a>",
           "<a href=\"https://data.consilium.europa.eu/doc/document/WK-5494-2026-INIT/en/pdf\" target=\"_blank\" rel=\"noopener\">Consiglio dell’UE — compromise text della Presidenza (17 aprile 2026)</a>",
           "<a href=\"https://iabeurope.eu/wp-content/uploads/IAB-Europe_Digital-Omnibus_Position-Paper_Feb-2026.pdf\" target=\"_blank\" rel=\"noopener\">IAB Europe — Position Paper sul Digital Omnibus</a>",
           "<a href=\"https://www.alliancedigitale.org/wp-content/uploads/2026/03/2026-03-Alliance-Digitale-Digital-Omnibus-Simplification-Position_FINAL_4943173684542262799.pdf\" target=\"_blank\" rel=\"noopener\">Alliance Digitale — Position Paper sul Digital Omnibus</a>",
           "<a href=\"https://www.eurocommerce.eu/2026/06/position-paper-on-the-digital-omnibus/\" target=\"_blank\" rel=\"noopener\">EuroCommerce — Position Paper sul Digital Omnibus</a>",
           "<a href=\"https://www.beuc.eu/sites/default/files/publications/BEUC-X-2026-011_Protecting_EU_data_and_privacy_rights_in_the_Digital_Omnibus.pdf\" target=\"_blank\" rel=\"noopener\">BEUC — Protecting EU data and privacy rights in the Digital Omnibus</a>",
           "<a href=\"https://edri.org/wp-content/uploads/2026/02/layout-eprivacyOmnibus.pdf\" target=\"_blank\" rel=\"noopener\">EDRi — The Digital Omnibus and ePrivacy</a>"]),
  ]),
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

# English editions are edited as articles in their own right.  Keeping them
# separate from POSTS lets titles, cadence and terminology read naturally.
EN_POSTS = {
"agente-che-dimentica-ogni-notte": dict(
    slug="building-adaptive-ai-agents",
    human_date="31 August 2026", read=10,
    tags=["AI agents", "Memory", "Architecture"],
    title="Building Adaptive AI Agents: DeepLearning.AI's new course",
    dek="An internal agent should not have to start from scratch in every new chat. "
        "DeepLearning.AI's course on adaptive agents lays out a practical method: capture traces, "
        "approve reusable skills, structure knowledge, and leave model weights until last.",
    body=[
      ("p", "On Monday, an internal agent answers an expense claim. It discovers that the valid policy is not in the attached PDF but in a version posted to the intranet three months earlier, finds it and gets the answer right. On Tuesday another colleague asks the same question in a new chat. The agent starts again from the wrong PDF, and someone has to correct it again."),
      ("p", "That scenario comes almost word for word from <i>Building Adaptive AI Agents</i>, DeepLearning.AI's new course. Its example is a coding agent that repeats the same testing mistake, but the problem is broader: what an agent retains between one conversation and the next, whether it writes Python, handles expenses or drafts a contract."),
      ("p", "Without a way to retain and reuse what it learns, the agent pays the same learning cost every day. The cost is just scattered across hundreds of chats instead of appearing on an invoice."),
      ("h2", "Three levels, not one"),
      ("p", "The course ranks three ways of improving an agent by cost. The first two work on the context the agent reads before replying, the <b>token space</b>: reusable procedures and a better structure for finding knowledge. The third changes the model's weights, the <b>weight space</b>, and should come later."),
      ("fig", "cost"),
      ("p", "The first two levels can change in minutes: write a file or add a node to a graph. The third needs training and dedicated hardware, and has to be repeated when the underlying policy changes. Starting with model weights to teach a new company rule means choosing the most expensive layer."),
      ("h2", "From traces to an approved procedure"),
      ("p", "The first level is called <i>skill induction</i>. Conversations, tool calls, errors and corrections are recorded; a model then condenses them into a short procedure for the next time the same kind of request arrives."),
      ("fig", "loop"),
      ("p", "Human review decides whether that procedure becomes behaviour. Once a skill is approved, the agent retrieves it for similar requests until someone changes it. If a bad skill gets through, the mistake is repeated on every use."),
      ("note", "Traces are not reliable sources by default. An incorrect instruction, or one deliberately inserted through a malicious tool call, can look like a candidate skill. Review stops it before it is reused."),
      ("p", "Every approved skill should have an owner and a written rationale, including rejected ones. Without that context the system cannot improve a proposal; it can only submit it again."),
      ("h2", "Finding the right knowledge"),
      ("p", "The second level is the organisation of the knowledge an agent consults. The course shows it on a codebase, but the pattern is familiar: as a knowledge base grows, finding the document to start from can take more work than writing the answer. Keyword search finds the term it was given and leaves out related documents that do not contain it."),
      ("p", "The proposed answer is a graph of relationships between documents: what refers to what, what changes together, what depends on what. In code those links are imports, function calls and changes in the same commit. In a company they are linked policies, procedures that change together and contracts referring to the same supplier."),
      ("p", "Retrieval happens in two steps. It first finds the node semantically closest to the question, then traverses the graph with a ranking algorithm similar to PageRank. That avoids treating everything one hop away as equally relevant."),
      ("table", dict(head=["", "Keyword search", "Knowledge graph"], rows=[["Finds related material that is not named", "No", "Yes"], ["Cost of adding a new document", "Low", "Almost zero"], ["Needs near-duplicates removed", "—", "Yes, or the graph gets noisy"], ["Result on tested multi-hop tasks", "Misses the right node", "Finds it"]])),
      ("p", "In the course benchmarks, the graph cut task time by 11–18%, steps to the first correct change by 7–36%, and tokens by 3–16% on Django and HTTPie repositories. Those percentages do not transfer automatically to a company, but they show why a flat index stops being enough when the relationships are part of the problem."),
      ("note", "A graph needs maintenance. In the course test, around 4% of nodes were 96% near-duplicates and had to be removed before retrieval became reliable again. Two copies of the same policy in different folders are noise."),
      ("h2", "When to touch model weights"),
      ("p", "The third level changes model weights. A base model has already absorbed a vast amount of text; for a policy or piece of knowledge that changes often, rewriting its weights is usually more expensive than supplying it as context at the right time."),
      ("p", "Fine-tuning makes sense for different jobs: making a refusal reliable, or adapting the format and tone of a response. LoRA, the most common technique, freezes the original weights and trains two small matrices. It changes roughly 1% of the parameters."),
      ("p", "Training too many parameters risks <i>catastrophic forgetting</i>: the model loses part of what it knew because its original weights are overwritten. Cost rises with model size. In the course, an adapter for 600 million parameters trains in an hour; the equivalent exercise on a frontier model would take hundreds or thousands of compute hours."),
      ("p", "In production, a router can send a technical request to the base model and a tone-sensitive request to the relevant adapter, without asking the user to choose."),
      ("h2", "Why this applies to any internal agent"),
      ("p", "The course uses coding agents because public benchmarks and open-source code exist there. The three levels apply elsewhere too. An agent answering HR policy questions, drafting contracts or routing support tickets has traces to learn from and documents that can be organised as a graph."),
      ("p", "For an internal agent, the practical starting point is to decide which corrections become reusable procedures, who approves them and where the agent searches for knowledge. Fine-tuning remains a specific choice for behaviour and format, not the normal way to update a rule that will change in three months.")]),
"tutti-odiano-cookie-banner-europa-divisa-soluzione-digital-omnibus": dict(
    human_date="31 August 2026", read=15,
    tags=["Privacy", "Advertising", "European regulation"],
    title="Everyone hates cookie banners. Europe is divided over the solution",
    dek="There is near-universal agreement about the problem. The conflict begins when Europe has to decide which activities can happen without consent, who should transmit preferences, and which economic model of the internet it wants to protect.",
    body=[
      ("p", "On 19 November 2025 the European Commission presented the Digital Omnibus, a proposal that amends a long list of existing digital rules. Among other things, it tries to fix one of the stranger results of European internet regulation: to give users more control over their data, Europe built a system in which millions of people answer the same question every day, often without reading it."),
      ("p", "The Commission calls this <i>consent fatigue</i>. On that point, almost everyone agrees. The EDPB and EDPS want to address the spread of cookie banners; the ad industry says consent has become a repetitive compliance ritual; consumer groups acknowledge that setting preferences site by site is inefficient; even the political groups most wary of reopening the GDPR do not seriously defend the status quo."),
      ("p", "The disagreement starts with what should replace it."),
      ("cards", [("The problem", "<mark>Consent fatigue</mark>: the same choice is repeated site by site."), ("The proposal", "Fewer consent requests and preferences sent in a <mark>machine-readable</mark> form."), ("The question", "Who controls consent: the user, the publisher or the browser?")]),
      ("h2", "Fewer banners, but how?"),
      ("p", "The Commission's proposal works on two fronts. A new Article 88a of the GDPR would broaden some exceptions to consent for access to information stored on a user's device, including certain forms of audience measurement. Article 88b would allow some preferences to be expressed through automated, machine-readable signals: a browser or operating system could tell sites what the user has chosen instead of asking the same question every time."),
      ("p", "Consent would remain the general rule, but it would be requested less often and a response could persist. The exceptions are the part with the most immediate consequences for advertising."),
      ("h2", "The line between measurement and tracking"),
      ("p", "On 11 February 2026 the EDPB and EDPS published their Joint Opinion on the Digital Omnibus. They support the goal of reducing consent fatigue and welcome limited derogations. But they draw a narrow line around audience measurement: it should produce <mark>aggregated and anonymous information</mark> about use of a service, without combining it with data from other services, reusing it for other purposes or sharing it with third parties."),
      ("p", "They also invite legislators to consider a new exception for <mark>contextual advertising</mark>. It is more privacy-friendly than behavioural advertising when it depends only on the page being viewed or the search being made at that moment, without storing or linking past and future activity."),
      ("p", "They recognise that a contextual campaign still has to be operated and measured. Frequency capping, advertising audience measurement and click-fraud prevention may require trackers and could be included in cases that do not require consent, if the exception is tightly drawn."),
      ("note", "Their position does not treat measurement and tracking as the same thing, nor does it exempt anything called “measurement”. The risk depends on what is technically done with the data."),
      ("h2", "The first divide: risk"),
      ("p", "The EPP, and Aura Salla in particular, support a more risk-based approach: remove unnecessary banners, increase legal certainty and make it easier for European businesses to use data without abandoning fundamental safeguards. Salla also repeats a second argument: badly designed regulation can strengthen the large US platforms Europe wants to make less dominant."),
      ("p", "The ECR is even more explicit about proportionality. Diego Solier has cited audience measurement, advertising, cybersecurity updates and fraud prevention as cases where relatively low-intrusion activity should not be treated like behavioural tracking."),
      ("p", "S&D begins from a different concern. Marina Kaljurand also supports risk-based application of the GDPR, but argues that the Digital Omnibus must not weaken core definitions and protections, beginning with the definition of personal data. The point is to simplify without creating exceptions that can reclassify invasive activity as harmless."),
      ("p", "Renew takes a middle position. Michael McNamara has called for genuine simplification while retaining safeguards for fundamental rights, with the emphasis on a technically workable compromise."),
      ("p", "Greens/EFA and The Left are much more suspicious of the exercise. The Greens warn that reopening GDPR and ePrivacy could become a gift to large platforms and call for stronger enforcement of existing rules. Markéta Gregorová still supports finding a real way to remove cookie banners as they work today. The Left sees the proposal as a possible retreat from consumer and data protection."),
      ("p", "There is no single cookie position even among conservative or nationalist groups. Patriots for Europe, for example, has focused more on pseudonymisation and legal certainty than on a particular consent architecture. Calling the story simply left versus right misses too much."),
      ("cards", [("EPP · ECR", "<mark>Proportionality and competitiveness</mark>: distinguish low-intrusion activity from behavioural tracking."), ("S&D · Renew", "Simplify without creating <mark>new loopholes</mark> in fundamental protections."), ("Greens · The Left", "More enforcement and caution: the risk is a <mark>gift to platforms</mark>.")]),
      ("h2", "The second divide: power"),
      ("p", "Outside Parliament the conflict is clearer. IAB Europe accepts the Commission's aim but says the Article 88a exceptions are too narrow. Continuing to ask consent for low-risk operational activity, it argues, will not remove consent fatigue. At the same time, IAB opposes browser-centred consent because it could damage the ad-funded content ecosystem and increase the power of large technology intermediaries."),
      ("p", "Alliance Digitale, the French marketing and data association, reaches a similar conclusion. It sees the Article 88b centralised mechanism as a risk to proportionality, competition and technological neutrality, and instead calls for exceptions for low-risk activities including contextual advertising, frequency capping, anti-fraud and aggregated analytics."),
      ("p", "EuroCommerce makes a similar case: more risk-based exceptions for low-risk processing and more recognition for privacy-enhancing technologies, but no general obligation to manage preferences through the browser and no rigid six-month ban on asking again. Its stated concern is the emergence of new gatekeepers."),
      ("p", "If a user's preference is expressed mainly through Chrome or Safari, Google and Apple stop being only browser makers. They become <mark>part of the infrastructure through which a legal right is exercised.</mark> The Commission sees a way to end cookie fatigue; part of the industry sees power moving from publishers to two of the world's largest companies."),
      ("p", "BEUC, which represents European consumer organisations, sees the same architecture from the other side. It cautiously welcomes browser signals because they could make consent easier to exercise, but wants consent to remain the baseline and the exceptions defined much more precisely. It also supports a specific treatment for contextual advertising, provided it does not become a shortcut to profiling."),
      ("p", "EDRi pushes the criticism further. Cookie fatigue, it argues, does not mainly come from banners but from an economic model built on tracking, manipulative interfaces and weak enforcement. Removing the symptom without changing those incentives could make tracking less visible."),
      ("h2", "Three conflicts, not one"),
      ("p", "The Commission has offered an apparently simple answer to a problem on which there is broad agreement. In doing so, it has opened at least three separate conflicts."),
      ("cards", [("01 — Risk", "Which activities are low-intrusion enough to happen without consent?"), ("02 — Power", "Who should collect and transmit preferences: the publisher or the browser?"), ("03 — The model", "How far can behavioural tracking be limited without undermining free media and services?")]),
      ("p", "The Council has shown how hard it is to hold those questions together. A Presidency compromise text of 17 April included a new exception for contextual advertising, in the direction suggested by the EDPB and EDPS. In June, however, Member States removed several of the main cookie-banner simplification provisions from the compromise, effectively postponing the issue."),
      ("p", "The process in Parliament is still open. Salla and Kaljurand's draft report arrived in June; more than a thousand amendments were tabled in July; the next step is to negotiate compromise amendments before the committee vote. On 31 August, the official 2025/0360(COD) file was still listed as “Awaiting committee decision”."),
      ("h2", "What changes for the advertising ecosystem"),
      ("p", "For advertising, the result could matter far more than the disappearance of a few banners. A more favourable legal treatment for contextual advertising would make ads based on the page, rather than an individual's history, more economically attractive. Clear exceptions for audience measurement, frequency capping and anti-fraud could separate operational advertising functions from behavioural profiling."),
      ("p", "Strong browser signals could sharply reduce the number of people available for some forms of tracking while increasing the power of browsers and operating systems. Publishers and retailers would have an even stronger incentive to develop first-party data and direct relationships with users."),
      ("cards", [("Contextual", "The value of an ad comes from the page, not a person's history."), ("Measurement", "Measure campaigns, frequency and fraud without turning everything into profiling."), ("First-party", "Publishers and retailers have a stronger incentive to build direct relationships.")]),
      ("p", "There is also a measurement question worth watching without attributing conclusions to the legislator that it has not drawn. The Digital Omnibus does not propose new marketing-effectiveness models or tell companies to replace attribution with incrementality or marketing mix modelling. It does introduce an important regulatory distinction: <mark>not every activity needed to measure a campaign requires reconstructing a person's behaviour across services.</mark>"),
      ("p", "Digital advertising has had little reason to make that distinction while the same technical infrastructure could handle targeting, tracking, attribution and measurement. It may now have to."),
      ("h2", "What everyone is trying to save"),
      ("p", "No one in this debate really wants to preserve cookie banners. The EDPB and EDPS want proportion between risk and processing; the ad industry wants to fund and measure advertising and content; publishers want a direct relationship with their audience; consumers want real control; Greens and digital-rights organisations want existing protections kept intact; EPP and ECR want competitiveness and room for European businesses to use data; S&D and Renew want simplification without new escape routes."),
      ("p", "The question behind the banner is who gets to observe what we do next, for what purpose and at what level of detail."),
      ("h2", "Sources and documents"),
      ("ul", ["<a href=\"https://digital-strategy.ec.europa.eu/en/library/digital-omnibus-regulation-proposal\" target=\"_blank\" rel=\"noopener\">European Commission — Digital Omnibus proposal</a>", "<a href=\"https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025%2F0360%28COD%29\" target=\"_blank\" rel=\"noopener\">European Parliament — file 2025/0360(COD)</a>", "<a href=\"https://www.edpb.europa.eu/system/files/documents/2026-02/edpb_edps_jointopinion_202602_digitalomnibus_en.pdf\" target=\"_blank\" rel=\"noopener\">EDPB and EDPS — Joint Opinion (11 February 2026)</a>", "<a href=\"https://data.consilium.europa.eu/doc/document/WK-5494-2026-INIT/en/pdf\" target=\"_blank\" rel=\"noopener\">Council of the EU — Presidency compromise text (17 April 2026)</a>", "<a href=\"https://iabeurope.eu/wp-content/uploads/IAB-Europe_Digital-Omnibus_Position-Paper_Feb-2026.pdf\" target=\"_blank\" rel=\"noopener\">IAB Europe — position paper</a>", "<a href=\"https://www.alliancedigitale.org/wp-content/uploads/2026/03/2026-03-Alliance-Digitale-Digital-Omnibus-Simplification-Position_FINAL_4943173684542262799.pdf\" target=\"_blank\" rel=\"noopener\">Alliance Digitale — position paper</a>", "<a href=\"https://www.eurocommerce.eu/2026/06/position-paper-on-the-digital-omnibus/\" target=\"_blank\" rel=\"noopener\">EuroCommerce — position paper</a>", "<a href=\"https://www.beuc.eu/sites/default/files/publications/BEUC-X-2026-011_Protecting_EU_data_and_privacy_rights_in_the_Digital_Omnibus.pdf\" target=\"_blank\" rel=\"noopener\">BEUC — protecting EU data and privacy rights</a>", "<a href=\"https://edri.org/wp-content/uploads/2026/02/layout-eprivacyOmnibus.pdf\" target=\"_blank\" rel=\"noopener\">EDRi — The Digital Omnibus and ePrivacy</a>"])])
}


def published(lang="it"):
    """The posts that actually reach the site. Drafts stay in this file — they
    are written, not published — and produce no page, no feed entry, no link."""
    posts = [p for p in POSTS if not p.get("draft")]
    if lang == "it":
        return posts
    return [{**p, **EN_POSTS[p["slug"]]} for p in posts]


def _anchor(text):
    return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")


def _render_one(kind, payload, lang="it"):
    """One block, at whatever heading level it turns out to sit inside."""
    if kind == "h3":
        return f"<h3>{payload}</h3>"
    if kind == "p":
        return f"<p>{payload}</p>"
    if kind in ("ul", "ol"):
        items = "".join(f"<li>{i}</li>" for i in payload)
        return f"<{kind}>{items}</{kind}>"
    if kind == "fig":
        if payload == "cost":
            labels = (["<b>Skill</b> Rewrite a procedure", "<b>Knowledge graph</b> Add nodes and edges", "<b>Fine-tuning</b> Retrain part of the model"]
                      if lang == "en" else ["<b>Skill</b> Riscrivere una procedura", "<b>Grafo di conoscenza</b> Aggiungere nodi e archi", "<b>Fine-tuning</b> Riaddestrare parte del modello"])
            return ('<figure class="bfigwrap bfig-cost">' + FIGURES[payload]() +
                    '<figcaption class="bfiglegend">' + ''.join(f'<span>{label}</span>' for label in labels) + '</figcaption></figure>')
        if payload == "loop":
            steps = (["<b>01 · Traces</b><span>Tool calls, errors and corrections</span>",
                      "<b>02 · Candidate</b><span>A model distils a proposed skill</span>",
                      "<b>03 · Human review</b><span>Approve or reject it before reuse</span>",
                      "<b>04 · Reuse</b><span>The approved skill is retrieved for similar work</span>"]
                     if lang == "en" else ["<b>01 · Tracce</b><span>Tool call, errori e correzioni</span>",
                      "<b>02 · Candidata</b><span>Un modello distilla una skill proposta</span>",
                      "<b>03 · Revisione umana</b><span>Approvare o respingere prima del riuso</span>",
                      "<b>04 · Riuso</b><span>La skill approvata torna nelle richieste simili</span>"])
            return '<div class="bflow">' + ''.join(f'<div>{step}</div>' for step in steps) + '</div>'
        return f'<figure class="bfigwrap">{FIGURES[payload]()}</figure>'
    if kind == "note":
        return f'<aside class="bnote">{payload}</aside>'
    if kind == "cards":
        cards = "".join(f'<section class="bcallout"><span>{title}</span><p>{text}</p></section>'
                        for title, text in payload)
        return f'<div class="bgrid">{cards}</div>'
    if kind == "table":
        head = "".join(f"<th>{h}</th>" for h in payload["head"])
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
                       for r in payload["rows"])
        return (f'<div class="btable"><table><thead><tr>{head}</tr></thead>'
                f"<tbody>{rows}</tbody></table></div>")
    return ""


# ---------------------------------------------------------------- rendering
# Every h2 opens a two-column section — a numbered label on the left, sticky
# on wide screens, the heading and its body on the right — the same rhythm
# as the section grid on the methodology page. Anything before the first h2
# is the lead-in and stays a single column, like a magazine standfirst.
def render_blocks(blocks, lang="it"):
    intro, sections = [], []
    for kind, payload in blocks:
        if kind == "h2":
            sections.append((payload, []))
        elif sections:
            sections[-1][1].append((kind, payload))
        else:
            intro.append((kind, payload))

    out = ["".join(_render_one(k, v, lang) for k, v in intro)] if intro else []
    for i, (title, body) in enumerate(sections, 1):
        anchor = _anchor(title)
        inner = "".join(_render_one(k, v, lang) for k, v in body)
        out.append(
            f'<section class="bsec rv" id="{anchor}">'
            f'<div class="bhead"><span class="n">{i:02d}</span><h2>{title}</h2></div>'
            f'<div class="bcol">{inner}</div>'
            f"</section>"
        )
    return "\n".join(out)


def chips(tags):
    return "".join(f'<span class="chip">{t}</span>' for t in tags)
