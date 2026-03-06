#!/usr/bin/env python3
"""
Riscrive le pagine guide/ per le 6 province rimanenti:
Siracusa, Trapani, Ragusa, Agrigento, Enna, Caltanissetta.
3 pagine per provincia: architetto, cila, ristrutturazione-appartamento.
Aggiorna anche dateModified nelle 10 pagine già riscritte.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent


def get_article_parts(html):
    m = re.search(r'<article class="article">(.*?)</article>', html, re.DOTALL)
    if not m:
        return None
    article = m.group(1)

    bc = re.search(r'<div class="breadcrumb">.*?</div>', article, re.DOTALL)
    breadcrumb = bc.group(0) if bc else ''

    h1 = re.search(r'<h1>[^<]+</h1>', article)
    h1_tag = h1.group(0) if h1 else ''

    phone = re.search(r'<div class="phone-cta"[^>]*>.*?</div>', article, re.DOTALL)
    phone_cta = phone.group(0) if phone else ''

    wa = re.search(r'class="btn secondary" href="(https://wa\.me/[^"]+)"', article)
    wa_href = wa.group(1) if wa else 'https://wa.me/393299736697'

    related = re.search(r'<section id="related-links">.*?</section>', article, re.DOTALL)
    related_html = related.group(0) if related else ''

    return {'breadcrumb': breadcrumb, 'h1': h1_tag, 'phone_cta': phone_cta,
            'wa_href': wa_href, 'related': related_html}


def build_article(parts, new_lede, new_content, urgency_title, urgency_body):
    return (
        parts['breadcrumb'] +
        parts['h1'] +
        parts['phone_cta'] +
        f'<p class="lede">{new_lede}</p>' +
        f'<div style="margin-top:14px"><a class="btn" href="/inizia-da-qui/">Inizia da qui</a>'
        f'<a class="btn secondary" href="{parts["wa_href"]}" style="margin-left:10px">WhatsApp</a></div>' +
        new_content +
        f'<div class="notice cta-urgent"><strong>{urgency_title}</strong>'
        f'<p>{urgency_body}</p>'
        f'<p style="margin-top:12px">'
        f'<a class="btn" href="tel:+393299736697" style="font-size:16px">Chiama: +39 329 973 6697</a>'
        f'<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20vorrei%20una%20consulenza." style="margin-left:10px">WhatsApp</a>'
        f'</p>'
        f'<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ 5.0/5 su Houzz e Google · 50+ progetti in Sicilia · 20+ anni esperienza</p>'
        f'</div>' +
        parts['related']
    )


def rewrite_file(rel_path, new_lede, new_content, urgency_title, urgency_body):
    filepath = ROOT / rel_path
    if not filepath.exists():
        print(f"MISSING: {rel_path}")
        return False

    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    parts = get_article_parts(html)
    if not parts:
        print(f"SKIP (no article): {rel_path}")
        return False

    new_article_inner = build_article(parts, new_lede, new_content, urgency_title, urgency_body)

    new_html = re.sub(
        r'<article class="article">.*?</article>',
        '<article class="article">' + new_article_inner + '</article>',
        html,
        flags=re.DOTALL
    )

    # Aggiorna dateModified a oggi
    new_html = re.sub(
        r'"dateModified":\s*"[^"]*"',
        '"dateModified": "2026-03-06T10:00:00+01:00"',
        new_html
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    plain = re.sub(r'<[^>]+>', ' ', new_article_inner)
    plain = re.sub(r'\s+', ' ', plain).strip()
    words = len(plain.split())
    print(f"✅ {Path(rel_path).name} — {words} parole")
    return True


def update_date_only(rel_path):
    """Aggiorna solo dateModified sulle pagine già riscritte."""
    filepath = ROOT / rel_path
    if not filepath.exists():
        return False
    with open(filepath, encoding='utf-8') as f:
        html = f.read()
    new_html = re.sub(
        r'"dateModified":\s*"[^"]*"',
        '"dateModified": "2026-03-06T10:00:00+01:00"',
        html
    )
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"📅 dateModified aggiornato: {Path(rel_path).name}")
        return True
    return False


# ─────────────────────────────────────────────────────────────
# STEP 1: aggiorna dateModified sulle 10 pagine già riscritte
# ─────────────────────────────────────────────────────────────
ALREADY_REWRITTEN = [
    "guide/palermo/architetto-a-palermo-come-impostare-un-progetto-senza-sorprese.html",
    "guide/palermo/cila-a-palermo-quando-serve-e-cosa-cambia-in-cantiere.html",
    "guide/palermo/ristrutturazione-appartamento-a-palermo-tempi-fasi-e-documenti.html",
    "guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html",
    "guide/palermo/direzione-lavori-a-palermo-cosa-controlla-il-direttore-lavori.html",
    "guide/catania/architetto-a-catania-come-impostare-un-progetto-senza-sorprese.html",
    "guide/catania/cila-a-catania-quando-serve-e-cosa-cambia-in-cantiere.html",
    "guide/catania/ristrutturazione-appartamento-a-catania-tempi-fasi-e-documenti.html",
    "guide/messina/architetto-a-messina-come-impostare-un-progetto-senza-sorprese.html",
    "guide/palermo/stima-costi-ristrutturazione-a-palermo-come-leggere-un-preventivo.html",
]

# ─────────────────────────────────────────────────────────────
# STEP 2: 18 nuove pagine per 6 province
# ─────────────────────────────────────────────────────────────

# Info specifiche per ogni provincia
PROVINCE_INFO = {
    "siracusa": {
        "nome": "Siracusa",
        "caratteristiche": "Siracusa ospita uno dei centri storici più ricchi del Mediterraneo: Ortigia, isola barocca riconosciuta patrimonio UNESCO dal 2005. Ogni intervento edilizio nell'isola richiede l'autorizzazione della Soprintendenza di Siracusa. La provincia include anche zone di grande valore paesaggistico come Noto, Avola e la costa degli Iblei.",
        "vincoli": "Vincolo paesaggistico UNESCO su Ortigia, zone costiere tutelate, area del Parco Regionale degli Iblei, territorio ad alta densità di siti archeologici con obbligo di verifica preventiva.",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Siracusa",
        "soprintendenza": "Soprintendenza di Siracusa",
    },
    "trapani": {
        "nome": "Trapani",
        "caratteristiche": "La provincia di Trapani presenta caratteristiche uniche: il vento costante (Tramontana e Scirocco) influenza le scelte costruttive, le saline di Marsala e Paceco sono aree vincolate, e le isole Egadi pongono sfide logistiche importanti per i cantieri.",
        "vincoli": "Saline con vincolo paesaggistico, isole minori (Favignana, Levanzo, Marettimo) con accesso difficoltoso, zona costiera vincolata, riserve naturali regionali estese, centro storico di Erice con vincoli molto stringenti.",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Trapani",
        "soprintendenza": "Soprintendenza di Trapani",
    },
    "ragusa": {
        "nome": "Ragusa",
        "caratteristiche": "Ragusa è una delle città del Val di Noto, patrimonio UNESCO dal 2002 insieme a Noto, Modica, Scicli e altri centri barocchi. La città si sviluppa su due livelli: Ragusa Superiore e Ragusa Ibla (la parte barocca). La pietra iblea, calcarea locale tipica della zona, è il materiale costruttivo storico e il suo utilizzo è spesso prescritto per interventi in centro storico.",
        "vincoli": "Centro storico barocco UNESCO con normativa molto restrittiva, pietra iblea come materiale prescritto per restauri, vincoli paesaggistici sulla costa ragusana (Marina di Ragusa, Punta Secca, Sampieri), riserva naturale orientata di Macaudo.",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Ragusa",
        "soprintendenza": "Soprintendenza di Ragusa",
    },
    "agrigento": {
        "nome": "Agrigento",
        "caratteristiche": "Agrigento ospita la Valle dei Templi, patrimonio UNESCO tra i siti più importanti al mondo per l'archeologia greca. Il vincolo archeologico copre una vasta area intorno alla città. La costa agrigentina include la Scala dei Turchi, area sottoposta a forte tutela paesaggistica.",
        "vincoli": "Vincolo archeologico esteso intorno alla Valle dei Templi, vincolo paesaggistico sulla Scala dei Turchi e sulla costa, terreni argillosi soggetti a rischio frana in molte aree della provincia (area di crisi di Agrigento).",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Agrigento",
        "soprintendenza": "Soprintendenza di Agrigento",
    },
    "enna": {
        "nome": "Enna",
        "caratteristiche": "Enna è la provincia più interna della Sicilia, posizionata sull'altopiano ibleo-ennese a oltre 900 metri di altitudine. Le condizioni climatiche sono molto diverse dalla costa: inverni rigidi con neve, escursioni termiche accentuate. Queste caratteristiche influenzano le scelte costruttive, con maggiore attenzione all'isolamento termico e alle coperture.",
        "vincoli": "Vincoli paesaggistici sul Lago di Pergusa, aree protette nell'entroterra, centri storici di Enna alta e Piazza Armerina con Villa Romana del Casale (UNESCO).",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Enna",
        "soprintendenza": "Soprintendenza di Enna",
    },
    "caltanissetta": {
        "nome": "Caltanissetta",
        "caratteristiche": "Caltanissetta è il capoluogo della provincia più interna della Sicilia occidentale. L'economia della provincia è stata a lungo legata all'industria estrattiva dello zolfo, con conseguenti bonifiche e riconversioni di siti industriali. Le condizioni geologiche di alcune aree richiedono attenzione specifica alle fondazioni.",
        "vincoli": "Aree ex-minerarie con prescrizioni specifiche per le fondazioni, riserva naturale orientata Lago Sfondato, centro storico di Caltanissetta con beni architettonici vincolati.",
        "sismica": "zona sismica 2",
        "sue": "Sportello Unico Edilizia del Comune di Caltanissetta",
        "soprintendenza": "Soprintendenza di Caltanissetta",
    },
}

PAGES = []

for prov_slug, info in PROVINCE_INFO.items():
    nome = info["nome"]
    nome_art = f"a {nome}" if nome[0].lower() not in 'aeiou' else f"ad {nome}"
    sue = info["sue"]
    soprintendenza = info["soprintendenza"]
    vincoli = info["vincoli"]
    caratteristiche = info["caratteristiche"]
    sismica = info["sismica"]

    # ─── ARCHITETTO ───────────────────────────────────────────
    PAGES.append(dict(
        path=f"guide/{prov_slug}/architetto-a-{prov_slug}-come-impostare-un-progetto-senza-sorprese.html",
        lede=f"A {nome} ogni progetto edilizio richiede la conoscenza del territorio locale: vincoli paesaggistici, pratiche comunali e specificità costruttive della provincia. Un architetto esperto del contesto locale riduce ritardi e costi imprevisti.",
        content=f"""
<h2>Perché serve un architetto esperto {nome_art}</h2>
<p>{caratteristiche}</p>
<p>Un architetto abilitato è obbligatorio per qualsiasi pratica edilizia al Comune di {nome} o nei comuni della provincia: CILA, SCIA o Permesso di Costruire. Il professionista assevera la conformità delle opere alle norme tecniche, al Piano Regolatore e ai vincoli specifici.</p>

<h2>Vincoli specifici della provincia di {nome}</h2>
<p>{vincoli}</p>
<p>Prima di avviare qualsiasi progetto è indispensabile verificare se l'immobile ricade in una di queste aree protette. L'assenza di questa verifica può bloccare il cantiere dopo l'avvio o invalidare le pratiche già depositate.</p>

<h2>CILA, SCIA o Permesso di Costruire {nome_art}</h2>
<ul>
<li><strong>CILA</strong>: manutenzione straordinaria interna senza modifiche strutturali. Efficacia immediata dopo il deposito al {sue}</li>
<li><strong>SCIA</strong>: ristrutturazione con modifiche di prospetto o distribuzione rilevante. 30 giorni di attesa (silenzio-assenso)</li>
<li><strong>Permesso di Costruire</strong>: ampliamenti, sopraelevazioni, interventi strutturali. Tempi medi: 60–120 giorni</li>
</ul>
<p>In presenza di vincoli paesaggistici o storici, ogni pratica esterna richiede l'autorizzazione aggiuntiva della {soprintendenza}, con ulteriori 30–60 giorni di iter.</p>

<h2>La direzione lavori {nome_art}</h2>
<p>La direzione lavori è obbligatoria per legge ogni volta che si deposita una pratica edilizia. Il direttore lavori controlla la conformità delle opere al progetto approvato, gestisce le varianti in corso d'opera e certifica gli stati di avanzamento lavori. Senza DL nominato la pratica è invalida e il rogito viene bloccato. Studio 4e offre progettazione e direzione lavori come servizio integrato in tutta la provincia di {nome}.</p>

<h2>Il rilievo come primo passo obbligatorio</h2>
<p>Prima di qualsiasi progetto il rilievo metrico e la verifica dello stato legittimo dell'immobile sono indispensabili. A {nome}, come in tutta la Sicilia, la discrepanza tra planimetria catastale e stato reale è frequente negli edifici pre-1980. Questa verifica va completata prima di progettare, per evitare di lavorare su dati sbagliati e scoprire irregolarità a cantiere aperto.</p>

<h2>Documenti da raccogliere prima di iniziare</h2>
<ul>
<li>Atto di provenienza dell'immobile</li>
<li>Planimetria catastale aggiornata</li>
<li>Titoli edilizi originali (concessione, licenza, eventuale condono)</li>
<li>Certificato di agibilità o abitabilità</li>
<li>Regolamento condominiale (se applicabile)</li>
</ul>
<p>Studio 4e effettua le visure necessarie se alcuni documenti non sono disponibili, prima di avviare la progettazione.</p>
""",
        urgency_title=f"Hai un progetto a {nome}?",
        urgency_body=f"Studio 4e segue pratiche edilizie, ristrutturazioni e sanatorie {nome_art} e in tutta la Sicilia da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso.",
    ))

    # ─── CILA ─────────────────────────────────────────────────
    PAGES.append(dict(
        path=f"guide/{prov_slug}/cila-a-{prov_slug}-quando-serve-e-cosa-cambia-in-cantiere.html",
        lede=f"La CILA {nome_art} copre gli interventi di manutenzione straordinaria che non modificano volumi, strutture o destinazione d'uso. Il cantiere può aprire il giorno del deposito, ma classificare male l'intervento blocca i lavori e crea problemi al rogito.",
        content=f"""
<h2>Interventi che richiedono la CILA {nome_art}</h2>
<p>La CILA (Comunicazione di Inizio Lavori Asseverata) si applica agli interventi di manutenzione straordinaria che non modificano volumi, superfici, strutture portanti o destinazione d'uso. Rientrano nella CILA: spostamento o aggiunta di servizi igienici con tracciatura di pareti non portanti, rifacimento completo degli impianti elettrici e idraulici, sostituzione di pavimenti con modifica del massetto, apertura o chiusura di porte interne, installazione di sistemi di climatizzazione. Non serve per manutenzione ordinaria: tinteggiatura, sostituzione serramenti della stessa misura, riparazioni puntuali senza modifica planimetrica.</p>

<h2>Cosa NON si può fare con una CILA (serve SCIA o Permesso)</h2>
<ul>
<li><strong>Modifiche di prospetto</strong> (apertura/chiusura finestre esterne, modifica facciata): serve SCIA</li>
<li><strong>Cambio di destinazione d'uso</strong>: serve SCIA o Permesso di Costruire</li>
<li><strong>Interventi su strutture portanti</strong> (travi, pilastri, solai): serve SCIA strutturale con progetto</li>
<li><strong>Ampliamenti di superficie o volume</strong>: serve Permesso di Costruire</li>
</ul>
<p>{vincoli} In presenza di questi vincoli, anche interventi apparentemente minori possono richiedere autorizzazioni aggiuntive prima di depositare la CILA.</p>

<h2>Documenti necessari per la CILA {nome_art}</h2>
<ol>
<li>Asseverazione del tecnico abilitato (architetto o ingegnere) sulla conformità dell'intervento</li>
<li>Elaborati grafici: planimetria stato attuale e di progetto</li>
<li>Relazione tecnica descrittiva delle opere</li>
<li>Documentazione fotografica dello stato ante-intervento</li>
<li>Planimetria catastale aggiornata ed estratto catastale</li>
<li>Titolo di proprietà o altro diritto sull'immobile</li>
<li>Delibera condominiale (solo se l'intervento tocca parti comuni)</li>
</ol>

<h2>Tempi e procedura al {sue}</h2>
<p>Il {sue} riceve le pratiche in modalità telematica. Dopo il deposito la ricevuta viene rilasciata entro 1–3 giorni lavorativi. La CILA è ad efficacia immediata: i lavori possono iniziare il giorno del deposito. Il Comune ha 30 giorni per richiedere integrazioni. In caso di richiesta di integrazione i lavori devono essere sospesi. Studio 4e prepara le pratiche in modo completo per ridurre le richieste di integrazione al minimo.</p>

<h2>La CILA di fine lavori: obbligatoria e spesso dimenticata</h2>
<p>Al termine dei lavori va depositata la CILA di fine lavori, che chiude formalmente la pratica. Se sono sorte varianti rispetto al progetto originale, vanno documentate nella relazione finale. Senza chiusura della CILA la pratica rimane aperta e blocca il rogito in caso di vendita, successione o richiesta di mutuo.</p>

<h2>Errori frequenti nelle CILA {nome_art}</h2>
<ul>
<li>Usare la CILA per interventi che richiedono SCIA: il Comune può sospendere i lavori</li>
<li>Non nominare il direttore lavori: la pratica diventa invalida</li>
<li>Non depositare la CILA di fine lavori: pratica aperta = rogito bloccato</li>
<li>Planimetria catastale non aggiornata allo stato ante-intervento</li>
<li>Non verificare i vincoli paesaggistici o storici prima del deposito</li>
</ul>
""",
        urgency_title=f"CILA o pratica bloccata {nome_art}?",
        urgency_body=f"Studio 4e gestisce CILA, SCIA e pratiche edilizie {nome_art} e in tutta la provincia. <strong>Consulenza telefonica gratuita</strong> per valutare il tuo caso.",
    ))

    # ─── RISTRUTTURAZIONE APPARTAMENTO ───────────────────────
    PAGES.append(dict(
        path=f"guide/{prov_slug}/ristrutturazione-appartamento-a-{prov_slug}-tempi-fasi-e-documenti.html",
        lede=f"Ristrutturare un appartamento {nome_art} richiede in media 4–8 mesi dal sopralluogo all'abitabilità. I ritardi nascono quasi sempre da rilievo impreciso, documenti catastali non aggiornati e preventivi senza capitolato dettagliato.",
        content=f"""
<h2>Le 4 fasi di una ristrutturazione {nome_art}</h2>
<ol>
<li><strong>Analisi preliminare (2–4 settimane)</strong>: rilievo metrico, verifica dello stato legittimo urbanistico-catastale, ricognizione degli impianti, analisi dei vincoli specifici del territorio di {nome}</li>
<li><strong>Progettazione e pratiche edilizie (4–8 settimane)</strong>: elaborati grafici, capitolato tecnico con computo metrico, deposito CILA o SCIA al {sue}, eventuali autorizzazioni aggiuntive (Soprintendenza se in zona vincolata)</li>
<li><strong>Cantiere (8–20 settimane a seconda dell'ampiezza)</strong>: demolizioni, impianti, strutture, finiture nella sequenza corretta (impianti prima delle finiture)</li>
<li><strong>Chiusura (2–3 settimane)</strong>: deposito fine lavori al {sue}, variazione catastale DOCFA se necessaria, conformità impianti</li>
</ol>

<h2>Documenti da raccogliere prima di iniziare</h2>
<ul>
<li>Atto di provenienza dell'immobile</li>
<li>Planimetria catastale attuale (da confrontare con lo stato reale)</li>
<li>Titoli edilizi originali: concessione, licenza edilizia, eventuali condoni</li>
<li>Certificato di agibilità o abitabilità</li>
<li>Schema degli impianti esistenti (se disponibile)</li>
<li>Regolamento condominiale (soprattutto per modifiche di facciata o strutture)</li>
</ul>
<p>A {nome}, come in tutta la Sicilia, la difformità tra planimetria catastale e stato reale è frequente negli edifici pre-1980. Va regolarizzata prima del rogito.</p>

<h2>Quanto costa ristrutturare {nome_art} nel 2026</h2>
<ul>
<li><strong>Ristrutturazione leggera</strong> (finiture, parziali impianti, bagno): 430–700 €/mq</li>
<li><strong>Ristrutturazione media</strong> (bagni, cucina, impianti completi, pavimenti): 700–1.100 €/mq</li>
<li><strong>Ristrutturazione pesante</strong> (strutture, impianti totali, finiture premium): 1.100–1.800 €/mq</li>
</ul>
<p>In zone con vincoli paesaggistici o storici il costo aumenta del 15–25% per maggiori prescrizioni tecniche e difficoltà logistiche di cantiere.</p>

<h2>Vincoli specifici di {nome} da verificare</h2>
<p>{vincoli}</p>
<p>Prima di qualsiasi progetto è fondamentale verificare se l'immobile ricade in una di queste aree. Studio 4e effettua la verifica dei vincoli come prima operazione, prima di avviare qualsiasi progettazione.</p>

<h2>Come scegliere un'impresa {nome_art}</h2>
<p>Elementi da verificare prima di firmare un contratto:</p>
<ul>
<li>DURC aggiornato (Documento Unico di Regolarità Contributiva)</li>
<li>Iscrizione alla Camera di Commercio con codice ATECO edilizio pertinente</li>
<li>Referenze verificabili su lavori simili completati negli ultimi 2 anni nella provincia di {nome}</li>
<li>Disponibilità a firmare un capitolato dettagliato voce per voce (non preventivi "a corpo")</li>
</ul>
<p>Non affidarsi mai a chi propone di lavorare senza pratiche o di "sistemare i documenti dopo i lavori".</p>

<h2>La direzione lavori: obbligatoria e utile</h2>
<p>La direzione lavori è obbligatoria per legge quando si deposita una pratica edilizia. Il direttore lavori verifica la conformità delle opere al progetto, controlla la qualità dell'esecuzione, gestisce le varianti e certifica gli stati di avanzamento. Studio 4e offre progettazione e direzione lavori come servizio integrato: la stessa persona che ha progettato segue il cantiere {nome_art} fino alla consegna.</p>
""",
        urgency_title=f"Ristrutturazione {nome_art}: hai bisogno di un tecnico?",
        urgency_body=f"Studio 4e segue ristrutturazioni, pratiche edilizie e direzione lavori {nome_art} e in tutta la Sicilia. <strong>Prima consulenza telefonica gratuita</strong>.",
    ))


# ─────────────────────────────────────────────────────────────
# ESECUZIONE
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("📅 Aggiornamento dateModified pagine già riscritte...\n")
    for path in ALREADY_REWRITTEN:
        update_date_only(path)

    print(f"\n🚀 Riscrittura {len(PAGES)} pagine per le 6 province rimanenti...\n")
    ok = 0
    for page in PAGES:
        result = rewrite_file(
            page["path"],
            page["lede"],
            page["content"],
            page["urgency_title"],
            page["urgency_body"],
        )
        if result:
            ok += 1

    print(f"\n✅ Completato: {ok}/{len(PAGES)} pagine riscritte")
    print(f"📊 Totale pagine di qualità nel sito: {ok + len(ALREADY_REWRITTEN)} pagine")
