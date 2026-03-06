#!/usr/bin/env python3
"""
Riscrive:
1. barriere-architettoniche per tutte le 9 province
2. Pagine mancanti Messina: cila, ristrutturazione-appartamento, sanatoria, direzione-lavori
3. Pagine mancanti Catania: sanatoria, direzione-lavori, stima-costi-ristrutturazione
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

PROVINCE_INFO = {
    'palermo': {
        'nome': 'Palermo', 'sue': 'Sportello Unico Edilizia del Comune di Palermo',
        'soprintendenza': 'Soprintendenza di Palermo',
        'vincoli_ba': 'Il centro storico di Palermo — uno dei più estesi d\'Europa — presenta edifici a struttura muraria storica dove l\'installazione di ascensori interni richiede l\'autorizzazione della Soprintendenza di Palermo. Le abitazioni nei quartieri Kalsa, Ballarò, Albergheria, Capo e Vucciria devono rispettare i vincoli del Piano Regolatore Particolareggiato Esecutivo del centro storico.',
        'sismica': 'zona sismica 2',
    },
    'catania': {
        'nome': 'Catania', 'sue': 'Sportello Unico Edilizia del Comune di Catania',
        'soprintendenza': 'Soprintendenza di Catania',
        'vincoli_ba': 'A Catania la zona sismica 2 e la struttura in pietra lavica degli edifici storici richiedono verifiche strutturali specifiche prima di qualsiasi intervento su pareti portanti. Il centro storico barocco ha vincoli di tutela che limitano le modifiche di prospetto (rampe esterne, piattaforme elevatrici visibili dalla strada).',
        'sismica': 'zona sismica 2',
    },
    'messina': {
        'nome': 'Messina', 'sue': 'Sportello Unico Edilizia del Comune di Messina',
        'soprintendenza': 'Soprintendenza di Messina',
        'vincoli_ba': 'Messina è classificata in zona sismica 1 — la più alta in Italia. Qualsiasi intervento sulle strutture portanti (apertura di porte allargate per sedie a rotelle, installazione di vani ascensore) deve essere corredato da progetto strutturale a firma di ingegnere abilitato e depositato al Genio Civile. La ricostruzione post-terremoto del 1908 ha creato uno stock edilizio omogeneo con caratteristiche strutturali ripetitive, che semplifica le verifiche ma richiede competenza specifica.',
        'sismica': 'zona sismica 1',
    },
    'siracusa': {
        'nome': 'Siracusa', 'sue': 'Sportello Unico Edilizia del Comune di Siracusa',
        'soprintendenza': 'Soprintendenza di Siracusa',
        'vincoli_ba': 'A Ortigia, l\'isola patrimonio UNESCO, ogni modifica esterna — incluse rampe, maniglioni e piattaforme elevatrici — richiede l\'autorizzazione paesaggistica della Soprintendenza di Siracusa. Gli edifici storici di Ortigia hanno spesso scalinate monumentali di accesso che non possono essere modificate: in questi casi si ricorre a soluzioni alternative come le pedane elevatrici a pavimento o i servoscala nascosti.',
        'sismica': 'zona sismica 2',
    },
    'trapani': {
        'nome': 'Trapani', 'sue': 'Sportello Unico Edilizia del Comune di Trapani',
        'soprintendenza': 'Soprintendenza di Trapani',
        'vincoli_ba': 'Il centro storico di Trapani e il borgo di Erice hanno normative molto restrittive sulle modifiche esterne. La presenza delle saline (area vincolata) e la posizione costiera di molte abitazioni comportano verifiche aggiuntive sull\'impermeabilizzazione delle rampe e sul materiale delle superfici antiscivolo, esposti all\'umidità salina.',
        'sismica': 'zona sismica 2',
    },
    'ragusa': {
        'nome': 'Ragusa', 'sue': 'Sportello Unico Edilizia del Comune di Ragusa',
        'soprintendenza': 'Soprintendenza di Ragusa',
        'vincoli_ba': 'Ragusa Ibla — la città barocca UNESCO — si sviluppa su un altipiano roccioso raggiungibile principalmente attraverso scalinate storiche. L\'eliminazione delle barriere architettoniche in questi contesti richiede soluzioni creative: ascensori panoramici, funicolare urbana (già esistente), percorsi alternativi. Ogni intervento esterno richiede autorizzazione dalla Soprintendenza di Ragusa con il vincolo di non alterare il profilo storico del centro.',
        'sismica': 'zona sismica 2',
    },
    'agrigento': {
        'nome': 'Agrigento', 'sue': 'Sportello Unico Edilizia del Comune di Agrigento',
        'soprintendenza': 'Soprintendenza di Agrigento',
        'vincoli_ba': 'La vicinanza alla Valle dei Templi impone vincoli arqueologici che limitano le fondazioni profonde (necessarie per alcuni tipi di ascensori) nelle zone circostanti. Il centro storico di Agrigento ha caratteristiche simili agli altri centri storici siciliani, con edifici plurifamiliari a struttura muraria dove l\'ampliamento delle porte comporta verifiche strutturali.',
        'sismica': 'zona sismica 2',
    },
    'enna': {
        'nome': 'Enna', 'sue': 'Sportello Unico Edilizia del Comune di Enna',
        'soprintendenza': 'Soprintendenza di Enna',
        'vincoli_ba': 'Enna alta, il centro storico, si sviluppa su un pianoro a 931 metri di altitudine con edifici prevalentemente in pietra calcarea locale. Le condizioni climatiche — inverni rigidi con neve — impongono attenzione ai materiali delle rampe esterne (superfici antiscivolo certificate per gelo) e all\'impermeabilizzazione degli impianti elevatori.',
        'sismica': 'zona sismica 2',
    },
    'caltanissetta': {
        'nome': 'Caltanissetta', 'sue': 'Sportello Unico Edilizia del Comune di Caltanissetta',
        'soprintendenza': 'Soprintendenza di Caltanissetta',
        'vincoli_ba': 'Il centro storico di Caltanissetta ha un patrimonio di edifici Liberty e novecenteschi in buono stato strutturale, che si prestano relativamente bene agli interventi di eliminazione barriere. Le aree ex-minerarie della provincia richiedono invece verifiche geologiche specifiche prima di fondazioni per ascensori.',
        'sismica': 'zona sismica 2',
    },
}

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
        f'<p style="font-size:13px; opacity:0.8; margin-top:8px">⭐ Studio 4e · Arch. Fabio Costanzo e Arch. Maria Rosaria Piazza · Palermo, dal 1996</p>'
        f'</div>' +
        parts['related']
    )

def rewrite_file(rel_path, new_lede, new_content, urgency_title, urgency_body, meta_desc=None):
    filepath = ROOT / rel_path
    if not filepath.exists():
        print(f'  MISSING: {rel_path}')
        return False

    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    parts = get_article_parts(html)
    if not parts:
        print(f'  SKIP (no article): {rel_path}')
        return False

    new_article_inner = build_article(parts, new_lede, new_content, urgency_title, urgency_body)

    new_html = re.sub(
        r'<article class="article">.*?</article>',
        '<article class="article">' + new_article_inner + '</article>',
        html, flags=re.DOTALL
    )

    new_html = re.sub(
        r'"dateModified":\s*"[^"]*"',
        '"dateModified": "2026-03-06T10:00:00+01:00"',
        new_html
    )

    if meta_desc:
        new_html = re.sub(
            r'<meta content="[^"]*" name="description"/>',
            f'<meta content="{meta_desc}" name="description"/>',
            new_html
        )

    # Add author schema if not already present
    if 'Fabio Costanzo' not in new_html:
        author_schema = '<script data-architetti-sicilia="1" type="application/ld+json">{"@context": "https://schema.org", "@type": "Person", "name": "Fabio Costanzo", "jobTitle": "Architetto", "worksFor": {"@type": "Organization", "name": "Studio 4e", "url": "https://www.studio4e.it/"}, "url": "https://architettisicilia.it/studio-4e/chi-e-studio-4e.html"}</script>'
        new_html = new_html.replace('</head>', author_schema + '</head>', 1)
        byline = '<p class="byline" style="font-size:13px; color:#888; margin-top:6px; margin-bottom:0">A cura di <a href="/studio-4e/chi-e-studio-4e.html" style="color:#7a1d52">Arch. Fabio Costanzo</a>, Studio 4e · Aggiornato: marzo 2026</p>'
        h1_m = re.search(r'(<h1>[^<]+</h1>)', new_html)
        if h1_m:
            new_html = new_html.replace(h1_m.group(0), h1_m.group(0) + byline, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    plain = re.sub(r'<[^>]+>', ' ', new_article_inner)
    words = len(re.sub(r'\s+', ' ', plain).strip().split())
    print(f'  ✅ {Path(rel_path).name} — {words} parole')
    return True


# ═══════════════════════════════════════════════════════════
# SEZIONE 1: BARRIERE ARCHITETTONICHE (9 province)
# ═══════════════════════════════════════════════════════════

def rewrite_barriere(prov_slug, info):
    nome = info['nome']
    nome_art = f'a {nome}' if nome[0].lower() not in 'aeiou' else f'ad {nome}'
    sue = info['sue']
    vincoli_ba = info['vincoli_ba']
    sismica = info['sismica']

    lede = f'Eliminare le barriere architettoniche {nome_art} richiede pratiche edilizie specifiche, rispetto delle norme tecniche (L.13/89 e DM 236/89) e, in molti casi, autorizzazioni aggiuntive per edifici vincolati o in condominio.'

    content = f"""
<h2>Cosa si intende per barriere architettoniche</h2>
<p>La legge 13/1989 (cosiddetta "legge Canevari") e il DM 236/89 definiscono le specifiche tecniche per l'eliminazione delle barriere architettoniche negli edifici privati. Le barriere riguardano: gradini e dislivelli senza rampa, porte troppo strette (&lt;75 cm netti), assenza di ascensore in edifici con più di 3 piani fuori terra, bagni non adatti a persone con disabilità motoria, parcheggi senza spazi riservati.</p>
<p>Gli interventi di eliminazione barriere si dividono in:</p>
<ul>
<li><strong>Interventi interni all'unità</strong> (allargamento porte, adeguamento bagno, installazione maniglioni): di norma rientrano nella CILA, a meno che non tocchino strutture portanti</li>
<li><strong>Interventi sulle parti comuni</strong> (ascensori, rampe condominiali, piattaforme elevatrici): richiedono delibera assembleare con maggioranza di 1/3 dei condomini (art. 1120 c.c.) e pratica edilizia al {sue}</li>
<li><strong>Interventi su esterni vincolati</strong>: richiedono autorizzazione paesaggistica aggiuntiva</li>
</ul>

<h2>Specificità {nome_art}</h2>
<p>{vincoli_ba}</p>
<p>Prima di progettare qualsiasi intervento è fondamentale verificare: la classificazione sismica ({sismica}), la presenza di vincoli paesaggistici o storici sull'immobile, e lo stato del regolamento condominiale.</p>

<h2>Specifiche tecniche obbligatorie (DM 236/89)</h2>
<ul>
<li><strong>Porte</strong>: luce netta minima 75 cm (80 cm per le porte bagno accessibile)</li>
<li><strong>Corridoi</strong>: larghezza minima 100 cm; 120 cm se previsto l'uso di carrozzina</li>
<li><strong>Rampe</strong>: pendenza massima 8% (5% preferibile); larghezza minima 90 cm; maniglioni su entrambi i lati</li>
<li><strong>Ascensori</strong>: cabina minima 130×95 cm; pianerottolo di attesa 150×150 cm davanti alla porta</li>
<li><strong>Bagni accessibili</strong>: spazio laterale al WC 80 cm; doccia a pavimento con sedile ribaltabile; maniglioni di supporto</li>
</ul>

<h2>Le detrazioni fiscali 2026</h2>
<p>Gli interventi di eliminazione barriere architettoniche beneficiano di una <strong>detrazione IRPEF del 75%</strong> (introdotta dalla Legge di Bilancio 2022), in 5 rate annuali. Il massimale di spesa agevolabile dipende dal tipo di immobile:</p>
<ul>
<li>Edificio unifamiliare: massimale 50.000 €</li>
<li>Unità in condominio (su parti comuni): massimale 40.000 € per unità immobiliare (fino a 8 unità) o 30.000 € per le unità aggiuntive</li>
</ul>
<p>È richiesta la conformità alle specifiche tecniche del DM 236/89 per accedere alla detrazione. Studio 4e verifica la conformità come parte del progetto, per garantire l'accesso al beneficio fiscale.</p>

<h2>Installazione ascensore in condominio {nome_art}</h2>
<p>L'installazione di un ascensore in un condominio richiede:</p>
<ol>
<li>Verifica tecnica di fattibilità (spazio disponibile nel vano scale, struttura portante)</li>
<li>Delibera assembleare: sufficiente la maggioranza di 1/3 dei condomini e 1/3 del valore dell'edificio (art. 1120 c.c. novellato)</li>
<li>Progetto architettonico e strutturale</li>
<li>Pratica edilizia al {sue} (di norma SCIA)</li>
<li>Eventuale autorizzazione Soprintendenza se l'edificio è in zona vincolata</li>
<li>Collaudo e certificazione CE dell'impianto elevatore</li>
</ol>
<p>I tempi medi per un ascensore condominiale {nome_art} vanno da 4 a 8 mesi (pratiche + cantiere). Il costo indicativo di un ascensore in un edificio di 4 piani varia tra 25.000 e 55.000 € a seconda della tipologia.</p>

<h2>Bagno accessibile: cosa si può fare senza demolire</h2>
<p>In molti casi l'adeguamento del bagno per l'accessibilità non richiede la demolizione completa. Le soluzioni praticabili senza grandi opere strutturali includono: sostituzione della vasca con box doccia a livello pavimento, installazione di maniglioni fissi (tassellabili su muro portante senza pratica), sostituzione della porta con modello scorrevole o pieghevole per guadagnare spazio laterale. Quando invece si modificano le pendenze del massetto o si sposta la parete non portante del bagno, serve la CILA.</p>
"""

    urgency_title = f'Progetto di accessibilità {nome_art}?'
    urgency_body = f'Studio 4e progetta interventi di eliminazione barriere {nome_art} e verifica l\'accesso alle detrazioni fiscali 75%. <strong>Consulenza telefonica gratuita</strong>.'
    meta_desc = f'Barriere architettoniche {nome_art}: quali interventi richiedono pratica edilizia, detrazioni fiscali 75%, ascensori condominiali e adeguamento bagno. Guida tecnica 2026.'

    return rewrite_file(
        f'guide/{prov_slug}/barriere-architettoniche-a-{prov_slug}-interventi-e-requisiti-essenziali.html',
        lede, content, urgency_title, urgency_body, meta_desc
    )


# ═══════════════════════════════════════════════════════════
# SEZIONE 2: PAGINE MANCANTI MESSINA
# ═══════════════════════════════════════════════════════════

def rewrite_messina_cila():
    return rewrite_file(
        'guide/messina/cila-a-messina-quando-serve-e-cosa-cambia-in-cantiere.html',
        'La CILA a Messina copre la manutenzione straordinaria interna senza modifiche strutturali. Messina è in zona sismica 1: qualsiasi intervento che tocchi strutture portanti richiede SCIA con progetto strutturale, non CILA.',
        new_content="""
<h2>Cosa copre la CILA a Messina</h2>
<p>La CILA (Comunicazione di Inizio Lavori Asseverata) a Messina si applica alla manutenzione straordinaria che non modifica volumi, strutture portanti o destinazione d'uso. Esempi: rifacimento degli impianti elettrici e idraulici, spostamento di pareti non portanti, sostituzione pavimenti con modifica massetto, adeguamento bagno senza toccare strutture, installazione climatizzatori.</p>
<p><strong>Attenzione alla zona sismica 1</strong>: Messina è classificata zona sismica 1, la più alta in Italia. Questo significa che qualsiasi intervento su elementi strutturali — anche apparentemente minori come l'apertura di un vano porta in una parete portante — richiede un progetto strutturale firmato da ingegnere abilitato, depositato al Genio Civile, e una SCIA invece della CILA. La classificazione sismica è più restrittiva rispetto alle altre province siciliane (zone 2).</p>

<h2>Interventi che a Messina richiedono SCIA o Permesso (non CILA)</h2>
<ul>
<li><strong>Qualsiasi modifica a strutture portanti</strong>: zona sismica 1 rende obbligatorio il progetto strutturale e il deposito al Genio Civile</li>
<li><strong>Modifiche di prospetto</strong>: apertura/chiusura finestre, modifica facciata</li>
<li><strong>Cambio destinazione d'uso</strong></li>
<li><strong>Interventi su edifici vincolati</strong>: richiedono autorizzazione aggiuntiva della Soprintendenza di Messina</li>
</ul>

<h2>Documenti per la CILA a Messina</h2>
<ol>
<li>Asseverazione del tecnico abilitato (architetto o ingegnere)</li>
<li>Planimetria stato attuale e di progetto</li>
<li>Relazione tecnica descrittiva</li>
<li>Documentazione fotografica ante-intervento</li>
<li>Planimetria catastale aggiornata</li>
<li>Titolo di proprietà o altro diritto sull'immobile</li>
<li>Delibera condominiale (se l'intervento tocca parti comuni)</li>
</ol>

<h2>Procedura allo Sportello Unico Edilizia di Messina</h2>
<p>La CILA si deposita telematicamente allo Sportello Unico Edilizia del Comune di Messina. Efficacia immediata: i lavori possono iniziare il giorno del deposito. Il Comune ha 30 giorni per richiedere integrazioni. La CILA di fine lavori (obbligatoria) va depositata al termine del cantiere per chiudere formalmente la pratica.</p>

<h2>Errori tipici nelle CILA a Messina</h2>
<ul>
<li>Usare la CILA per interventi che toccano strutture portanti: in zona sismica 1 è un errore grave, con possibile sospensione lavori e sanzioni</li>
<li>Non verificare se la parete da spostare è portante (frequente negli edifici post-1908 in calcestruzzo armato)</li>
<li>Non depositare la CILA di fine lavori: la pratica rimane aperta e blocca rogito e mutuo</li>
</ul>
""",
        urgency_title='CILA o pratica edilizia a Messina?',
        urgency_body='Studio 4e gestisce CILA, SCIA e pratiche edilizie a Messina e in tutta la provincia, con conoscenza specifica della normativa sismica zona 1. <strong>Consulenza gratuita</strong>.',
        meta_desc='CILA a Messina: zona sismica 1, quando serve davvero, errori che bloccano i lavori e come NON confonderla con la SCIA strutturale. Guida tecnica 2026.',
    )

def rewrite_messina_ristrutturazione():
    return rewrite_file(
        'guide/messina/ristrutturazione-appartamento-a-messina-tempi-fasi-e-documenti.html',
        'Ristrutturare un appartamento a Messina richiede attenzione alla zona sismica 1: ogni modifica strutturale necessita di progetto ingegneristico depositato al Genio Civile. I tempi medi sono 5–9 mesi dal sopralluogo alla consegna.',
        new_content="""
<h2>Le 4 fasi operative a Messina</h2>
<ol>
<li><strong>Analisi preliminare (2–4 settimane)</strong>: rilievo metrico, verifica stato legittimo, mappatura impianti esistenti, verifica zona sismica e tipo strutturale dell'edificio (muratura, c.a., prefabbricato)</li>
<li><strong>Progettazione e pratiche (4–10 settimane)</strong>: elaborati architettonici, progetto strutturale se necessario (obbligatorio per qualsiasi modifica alla struttura), deposito al Genio Civile di Messina, CILA o SCIA allo Sportello Unico Edilizia</li>
<li><strong>Cantiere (8–20 settimane)</strong>: sequenza demolizioni → impianti → strutture (se previste) → finiture</li>
<li><strong>Chiusura (2–3 settimane)</strong>: fine lavori, eventuale variazione catastale DOCFA, conformità impianti</li>
</ol>

<h2>La zona sismica 1: impatto pratico sulla ristrutturazione</h2>
<p>Messina è l'unica provincia siciliana classificata in zona sismica 1. Questo comporta:</p>
<ul>
<li>Qualsiasi modifica a strutture portanti (travi, pilastri, pareti in c.a. o muratura portante) richiede <strong>progetto strutturale</strong> a firma di ingegnere abilitato</li>
<li>Il progetto strutturale va depositato al <strong>Genio Civile di Messina</strong> prima dell'inizio lavori</li>
<li>Il costo del progetto strutturale incide del 5–10% sul costo totale della ristrutturazione</li>
<li>I tempi si allungano di 3–6 settimane rispetto a province in zona sismica 2</li>
</ul>
<p>Studio 4e coordina progettazione architettonica e strutturale in un unico processo, per evitare conflitti tra i due progetti e ridurre i tempi complessivi.</p>

<h2>Documenti necessari a Messina</h2>
<ul>
<li>Atto di provenienza dell'immobile</li>
<li>Planimetria catastale (da confrontare con stato reale)</li>
<li>Titoli edilizi originali (concessione, licenza, eventuali condoni)</li>
<li>Certificato di agibilità o abitabilità</li>
<li>Certificato di collaudo statico (per edifici in c.a. post-1971)</li>
</ul>

<h2>Costi indicativi a Messina nel 2026</h2>
<ul>
<li><strong>Ristrutturazione leggera</strong> (finiture, impianti parziali): 450–720 €/mq</li>
<li><strong>Ristrutturazione media</strong> (bagni, cucina, impianti completi): 720–1.100 €/mq</li>
<li><strong>Ristrutturazione con interventi strutturali</strong>: 1.100–1.900 €/mq (include progetto strutturale e deposito al Genio Civile)</li>
</ul>

<h2>Scegliere l'impresa a Messina</h2>
<p>Per interventi strutturali in zona sismica 1, verificare che l'impresa abbia: DURC aggiornato, iscrizione alla CCIAA con codici ATECO edilizi, referenze su lavori simili in zona sismica verificabili. Non affidarsi a chi propone di fare lavori strutturali senza progetto depositato al Genio Civile.</p>
""",
        urgency_title='Ristrutturazione a Messina: hai bisogno di un tecnico?',
        urgency_body='Studio 4e coordina ristrutturazioni a Messina con progettazione architettonica e strutturale integrata. Conoscenza diretta della normativa sismica zona 1. <strong>Consulenza gratuita</strong>.',
        meta_desc='Ristrutturazione appartamento a Messina: zona sismica 1, progetto strutturale obbligatorio, costi 2026 e 4 fasi operative. Guida tecnica Studio 4e.',
    )

def rewrite_messina_sanatoria():
    return rewrite_file(
        'guide/messina/sanatoria-edilizia-a-messina-cosa-si-puo-regolarizzare-davvero.html',
        'La sanatoria edilizia a Messina segue le regole nazionali del Testo Unico Edilizia e la normativa regionale siciliana. Il principio del "doppio conforme" vale anche qui: l\'abuso deve essere conforme sia alle norme vigenti oggi sia a quelle vigenti al momento dell\'abuso.',
        new_content="""
<h2>Cos'è il doppio conforme e perché è fondamentale</h2>
<p>L'accertamento di conformità (art. 36 DPR 380/2001) — comunemente detto "sanatoria" — richiede il cosiddetto <strong>doppio conforme</strong>: l'intervento abusivo deve essere conforme alle norme urbanistiche ed edilizie vigenti sia al momento della realizzazione sia al momento della domanda. Se anche una sola delle due condizioni non è soddisfatta, la sanatoria non è possibile per quella normativa nazionale. La Sicilia ha normative regionali aggiuntive (LR 37/85, LR 17/94) che in alcuni casi ampliano le possibilità.</p>

<h2>Cosa si può sanare a Messina</h2>
<p>Sono sanabili, in presenza di doppio conforme:</p>
<ul>
<li>Difformità interne (pareti spostate, bagni aggiunti, tramezzi non dichiarati)</li>
<li>Piccoli ampliamenti in zona non vincolata, se conformi al PRG vigente</li>
<li>Cambio di destinazione d'uso conforme alle NTA del Piano Regolatore</li>
<li>Opere edilizie minori realizzate senza titolo ma conformi alla disciplina vigente</li>
</ul>

<h2>Cosa NON si può sanare a Messina</h2>
<ul>
<li>Abusi in zone vincolate (paesaggistici, sismici, idrogeologici) senza autorizzazione specifica</li>
<li>Interventi strutturali in zona sismica 1 realizzati senza progetto depositato al Genio Civile: questi non sono sanabili attraverso la semplice sanatoria edilizia, ma richiedono una procedura diversa</li>
<li>Ampliamenti in zone agricole non conformi alle NTA</li>
<li>Sopraelevazioni non conformi alle distanze dai confini</li>
</ul>

<h2>Sanatoria e zona sismica 1 a Messina: la particolarità</h2>
<p>Messina è zona sismica 1. Gli interventi strutturali realizzati senza deposito al Genio Civile non possono essere sanati semplicemente attraverso l'accertamento di conformità ex art. 36. Richiedono una procedura separata di <strong>verifica sismica</strong> e, in molti casi, la demolizione e ricostruzione dell'opera non conforme. Questo è il punto più critico e spesso sottovalutato nelle sanatorie a Messina.</p>

<h2>Iter pratico della sanatoria a Messina</h2>
<ol>
<li>Rilievo dello stato di fatto con documentazione fotografica</li>
<li>Confronto con planimetria catastale e titoli edilizi originali</li>
<li>Verifica del doppio conforme rispetto al PRG e alle NTA vigenti</li>
<li>Verifica sismica se l'abuso riguarda strutture portanti</li>
<li>Domanda di accertamento di conformità allo Sportello Unico di Messina</li>
<li>Pagamento oblazione (calcolata in base al tipo di abuso)</li>
<li>Aggiornamento catastale DOCFA</li>
</ol>
<p>I tempi medi per una sanatoria a Messina vanno da 3 a 12 mesi a seconda della complessità e del carico di lavoro degli uffici.</p>
""",
        urgency_title='Sanatoria a Messina: valuta il tuo caso',
        urgency_body='Studio 4e gestisce accertamenti di conformità e sanatorie a Messina, con esperienza specifica sulla normativa sismica zona 1. <strong>Consulenza telefonica gratuita</strong>.',
        meta_desc='Sanatoria edilizia a Messina: doppio conforme, cosa non è sanabile in zona sismica 1 e iter pratico 2026. Guida tecnica Studio 4e.',
    )

def rewrite_messina_dl():
    return rewrite_file(
        'guide/messina/direzione-lavori-a-messina-cosa-controlla-il-direttore-lavori.html',
        'La direzione lavori è obbligatoria per legge a Messina ogni volta che si deposita una pratica edilizia. In zona sismica 1 il direttore lavori ha responsabilità specifiche anche sul rispetto del progetto strutturale depositato al Genio Civile.',
        new_content="""
<h2>Cos'è la direzione lavori e perché è obbligatoria</h2>
<p>Il direttore dei lavori (DL) è il professionista abilitato che verifica la conformità delle opere eseguite al progetto approvato. È obbligatorio per legge ogni volta che viene depositata una pratica edilizia (CILA, SCIA, Permesso di Costruire). Senza DL nominato la pratica è invalida e il collaudo finale non può avvenire.</p>
<p>Il DL non è il capocantiere (che è un dipendente dell'impresa): il DL è un professionista indipendente che tutela il committente, non l'impresa.</p>

<h2>Responsabilità specifiche del DL a Messina (zona sismica 1)</h2>
<p>A Messina, in zona sismica 1, il direttore lavori ha responsabilità ampliate rispetto alle province in zone sismiche inferiori:</p>
<ul>
<li>Verifica che gli interventi strutturali corrispondano esattamente al progetto depositato al Genio Civile</li>
<li>Controlla la qualità dei materiali strutturali (certificazioni degli acciai, caratteristiche del cls)</li>
<li>Redige la relazione di fine lavori da presentare al Genio Civile per il collaudo statico</li>
<li>In caso di varianti strutturali in corso d'opera, gestisce la variante con nuovo deposito al Genio Civile</li>
</ul>
<p>Queste responsabilità aggiuntive rendono ancora più importante scegliere un DL con esperienza specifica in zona sismica a Messina.</p>

<h2>Cosa controlla il DL in cantiere</h2>
<ul>
<li><strong>Conformità al progetto</strong>: misure, quote, posizione delle pareti, dimensioni delle aperture</li>
<li><strong>Qualità esecutiva</strong>: posa delle impermeabilizzazioni, giunzioni degli impianti, corretta esecuzione dei massetti</li>
<li><strong>Gestione delle varianti</strong>: se in cantiere emerge la necessità di una modifica, il DL la formalizza con una perizia di variante o, se sostanziale, con una nuova pratica</li>
<li><strong>Stati di avanzamento lavori (SAL)</strong>: certifica le fasi di avanzamento per l'erogazione dei pagamenti all'impresa o per accedere ai bonus fiscali</li>
</ul>

<h2>DL e bonus fiscali a Messina</h2>
<p>Per accedere alle detrazioni fiscali (ristrutturazione 50%, barriere 75%), il DL firma le asseverazioni di conformità e i SAL richiesti. Senza la firma del DL l'Agenzia delle Entrate può revocare le detrazioni già fruite.</p>

<h2>Direzione lavori integrata: il vantaggio di Studio 4e</h2>
<p>Studio 4e offre progettazione e direzione lavori come servizio integrato: il professionista che ha progettato segue il cantiere fino alla consegna. Questo elimina il rischio di incomprensioni tra progettista e DL e garantisce continuità nella gestione delle varianti.</p>
""",
        urgency_title='Direzione lavori a Messina: hai bisogno di un professionista?',
        urgency_body='Studio 4e fornisce direzione lavori a Messina con esperienza specifica in zona sismica 1. Progettazione e DL come servizio integrato. <strong>Consulenza gratuita</strong>.',
        meta_desc='Direzione lavori a Messina: responsabilità specifiche in zona sismica 1, cosa controlla il DL e perché è obbligatorio. Guida tecnica Studio 4e 2026.',
    )


# ═══════════════════════════════════════════════════════════
# SEZIONE 3: PAGINE MANCANTI CATANIA
# ═══════════════════════════════════════════════════════════

def rewrite_catania_sanatoria():
    return rewrite_file(
        'guide/catania/sanatoria-edilizia-a-catania-cosa-si-puo-regolarizzare-davvero.html',
        'La sanatoria edilizia a Catania richiede il doppio conforme: l\'abuso deve essere conforme alle norme sia al momento della realizzazione sia oggi. La zona sismica 2 e la vicinanza all\'Etna aggiungono vincoli specifici.',
        new_content="""
<h2>Il doppio conforme a Catania</h2>
<p>L'accertamento di conformità (art. 36 DPR 380/2001) richiede che l'intervento abusivo sia conforme alle norme urbanistiche vigenti sia al momento dell'abuso sia oggi. A Catania questo significa verificare la conformità al Piano Regolatore vigente al momento dell'abuso (che a Catania ha avuto diverse revisioni) e alle NTA attuali.</p>

<h2>Il vincolo del Parco dell'Etna e le zone sismiche</h2>
<p>Una parte significativa del territorio provinciale di Catania ricade nel Parco dell'Etna o in aree vincolate paesaggisticamente. In queste zone:</p>
<ul>
<li>Il doppio conforme è ancora più difficile da dimostrare (le norme di tutela sono cambiate nel tempo)</li>
<li>Gli abusi su prospetti o in zone di espansione vincolata sono generalmente non sanabili</li>
<li>Interventi strutturali senza progetto antisismico depositato: richiedono verifica specifica prima di avviare la sanatoria</li>
</ul>
<p>La pietra lavica e la struttura geologica catanese comportano rischi di subsidenza in alcune aree (zona di Misterbianco, Paternò) che vanno verificati prima di qualsiasi pratica.</p>

<h2>Cosa si può sanare a Catania</h2>
<ul>
<li>Difformità interne all'unità (pareti, tramezzi, bagni) conformi al PRG</li>
<li>Piccoli ampliamenti in zone non vincolate, conformi agli indici edilizi vigenti</li>
<li>Cambio di destinazione d'uso conforme alle NTA</li>
<li>Opere minori senza titolo ma conformi alla disciplina vigente</li>
</ul>

<h2>Cosa NON si può sanare a Catania</h2>
<ul>
<li>Abusi in zona Parco dell'Etna (zone A e B di tutela assoluta)</li>
<li>Interventi in zone a rischio idrogeologico o frana</li>
<li>Strutture abusive che non rispettano le norme sismiche (zona 2): richiedono verifica specifica</li>
<li>Ampliamenti non conformi agli indici edilizi delle NTA</li>
</ul>

<h2>Iter pratico della sanatoria a Catania</h2>
<ol>
<li>Rilievo accurato dello stato di fatto</li>
<li>Verifica del doppio conforme rispetto al PRG e alle NTA di Catania</li>
<li>Verifica sismica se l'abuso riguarda strutture portanti</li>
<li>Verifica assenza vincoli paesaggistici (Parco Etna, fascia costiera)</li>
<li>Domanda allo Sportello Unico Edilizia del Comune di Catania</li>
<li>Pagamento oblazione</li>
<li>Aggiornamento catastale DOCFA</li>
</ol>
<p>I tempi medi a Catania: 4–14 mesi a seconda della complessità e del carico degli uffici comunali.</p>
""",
        urgency_title='Sanatoria a Catania: valutiamo il tuo caso',
        urgency_body='Studio 4e gestisce accertamenti di conformità e sanatorie a Catania, con esperienza specifica sui vincoli Parco Etna e normativa sismica. <strong>Consulenza gratuita</strong>.',
        meta_desc='Sanatoria edilizia a Catania: doppio conforme, vincoli Parco Etna, zona sismica 2 e cosa non è sanabile. Iter pratico 2026 Studio 4e.',
    )

def rewrite_catania_dl():
    return rewrite_file(
        'guide/catania/direzione-lavori-a-catania-cosa-controlla-il-direttore-lavori.html',
        'La direzione lavori è obbligatoria per legge a Catania ogni volta che si deposita una pratica edilizia. Il DL protegge il committente dall\'impresa, certifica gli SAL per i bonus fiscali e gestisce le varianti in corso d\'opera.',
        new_content="""
<h2>Perché il direttore lavori è obbligatorio</h2>
<p>Il direttore dei lavori (DL) è il professionista abilitato che verifica la conformità del cantiere al progetto approvato. Senza DL nominato la pratica edilizia è invalida: il Comune può sospendere i lavori e il collaudo finale (necessario per il rogito) non può avvenire. Il DL non è il capocantiere — è un professionista indipendente che rappresenta gli interessi del committente, non dell'impresa.</p>

<h2>Cosa controlla concretamente il DL a Catania</h2>
<ul>
<li><strong>Conformità al progetto</strong>: misure, quote, posizione delle aperture, caratteristiche dei materiali specificati in capitolato</li>
<li><strong>Qualità esecutiva</strong>: corretta posa delle impermeabilizzazioni (critica a Catania per l'umidità da lava), giunzioni degli impianti, esecuzione dei massetti</li>
<li><strong>Vincoli sismici zona 2</strong>: qualità dei materiali strutturali (cls, acciai), corretta esecuzione dei nodi strutturali</li>
<li><strong>Varianti in corso d'opera</strong>: formalizza ogni modifica rispetto al progetto con perizia o nuova pratica se necessario</li>
<li><strong>SAL (Stati di Avanzamento Lavori)</strong>: certifica le fasi per i pagamenti all'impresa e per i bonus fiscali</li>
</ul>

<h2>DL e bonus fiscali a Catania</h2>
<p>Per accedere alle detrazioni fiscali (ristrutturazione 50%, barriere 75%, ecobonus) il DL firma le asseverazioni di conformità. Senza le firme del DL le detrazioni possono essere revocate in sede di controllo dell'Agenzia delle Entrate.</p>

<h2>Il rischio "DL di facciata"</h2>
<p>Frequente nel settore edilizio siciliano: il tecnico nomina il DL formalmente ma non compare mai in cantiere. Questa pratica espone il committente a rischi seri: opere non conformi al progetto, materiali non verificati, varianti non documentate che creano problemi al rogito. Studio 4e fornisce direzione lavori con sopralluoghi documentati e report fotografici periodici.</p>

<h2>Direzione lavori integrata a Catania</h2>
<p>Studio 4e offre progettazione e direzione lavori come servizio unico: lo stesso professionista che ha progettato segue il cantiere, eliminando i rischi di disallineamento tra progetto e esecuzione. Attivo a Catania e in tutta la provincia.</p>
""",
        urgency_title='Direzione lavori a Catania: contattaci',
        urgency_body='Studio 4e fornisce direzione lavori a Catania con sopralluoghi documentati e report SAL. Progettazione e DL come servizio integrato. <strong>Consulenza gratuita</strong>.',
        meta_desc='Direzione lavori a Catania: cosa controlla il DL, perché è obbligatorio, SAL per bonus fiscali e il rischio DL di facciata. Guida tecnica 2026.',
    )

def rewrite_catania_stima():
    return rewrite_file(
        'guide/catania/stima-costi-ristrutturazione-a-catania-come-leggere-un-preventivo.html',
        'I costi di ristrutturazione a Catania nel 2026 variano da 450 a 1.800 €/mq a seconda del livello di intervento. Un preventivo serio deve essere dettagliato voce per voce: il prezzo "a corpo" nasconde quasi sempre sorprese.',
        new_content="""
<h2>Fasce di costo a Catania nel 2026</h2>
<ul>
<li><strong>Ristrutturazione leggera</strong> (finiture, parziali impianti, un bagno): <strong>450–720 €/mq</strong></li>
<li><strong>Ristrutturazione media</strong> (bagni, cucina, impianti completi, pavimenti): <strong>720–1.100 €/mq</strong></li>
<li><strong>Ristrutturazione pesante</strong> (strutture, impianti totali, finiture premium): <strong>1.100–1.800 €/mq</strong></li>
</ul>
<p>A queste cifre si aggiungono: onorari del professionista (8–14% del costo lavori), pratiche edilizie, allacciamenti e IVA. In zone vincolate (Etna, fascia costiera jonica) i costi logistici aumentano del 10–20%.</p>

<h2>Come leggere un preventivo a Catania</h2>
<p>Un preventivo attendibile deve contenere almeno:</p>
<ul>
<li><strong>Elenco prezzi unitari</strong>: costo per ml di impianto, per mq di pavimento, per pezzo di sanitario</li>
<li><strong>Quantità misurate</strong>: mq di parete da demolire, ml di traccia impianti, numero di punti luce</li>
<li><strong>Capitolato materiali</strong>: marca e modello (o categoria equivalente) dei materiali</li>
<li><strong>Esclusioni esplicite</strong>: cosa non è incluso (ad es. smaltimento macerie, allacciamenti, pratiche)</li>
</ul>
<p>Diffidate dei preventivi "a corpo" senza dettaglio: significano che l'impresa si riserva di aggiungere costi in corso d'opera per qualsiasi imprevisto, reale o presunto.</p>

<h2>Voci di costo tipiche a Catania</h2>
<table style="width:100%; border-collapse:collapse; font-size:14px">
<thead><tr style="background:#f5f0f3"><th style="padding:8px; text-align:left; border-bottom:2px solid #7a1d52">Voce</th><th style="padding:8px; text-align:left; border-bottom:2px solid #7a1d52">Costo indicativo</th></tr></thead>
<tbody>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Demolizione tramezzi (mq)</td><td style="padding:7px; border-bottom:1px solid #eee">15–25 €/mq</td></tr>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Impianto elettrico (punto luce)</td><td style="padding:7px; border-bottom:1px solid #eee">80–150 €/punto</td></tr>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Rifacimento impianto idrico (bagno)</td><td style="padding:7px; border-bottom:1px solid #eee">1.500–3.500 €/bagno</td></tr>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Posa pavimento ceramica (mq)</td><td style="padding:7px; border-bottom:1px solid #eee">35–65 €/mq (solo posa)</td></tr>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Intonaco pareti interno (mq)</td><td style="padding:7px; border-bottom:1px solid #eee">18–30 €/mq</td></tr>
<tr><td style="padding:7px; border-bottom:1px solid #eee">Serramenti PVC standard (unità)</td><td style="padding:7px; border-bottom:1px solid #eee">350–700 €/unità (fornitura)</td></tr>
</tbody>
</table>

<h2>Il computo metrico: lo strumento per confrontare preventivi</h2>
<p>Il computo metrico estimativo è il documento che elenca tutte le voci di lavoro con quantità e prezzi unitari. Con un computo in mano puoi confrontare due preventivi voce per voce, invece di confrontare solo il totale. Studio 4e redige il computo metrico come parte del progetto esecutivo, prima di mandare a gara le imprese.</p>

<h2>Ristrutturazione con vincoli sismici a Catania</h2>
<p>In zona sismica 2, qualsiasi intervento strutturale richiede progetto ingegneristico con costi aggiuntivi rispetto alla sola progettazione architettonica. Preventivare sempre la voce "progetto strutturale" separatamente: varia da 2.000 a 8.000 € a seconda della complessità.</p>
""",
        urgency_title='Stima costi ristrutturazione a Catania',
        urgency_body='Studio 4e prepara computi metrici dettagliati e capitolati per ristrutturazioni a Catania. Nessun preventivo a corpo. <strong>Prima consulenza gratuita</strong>.',
        meta_desc='Costi ristrutturazione a Catania 2026: 450–1.800 €/mq, come leggere un preventivo voce per voce e le voci che i preventivi a corpo nascondono.',
    )


# ═══════════════════════════════════════════════════════════
# ESECUZIONE
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('═' * 55)
    print('SEZIONE 1: Barriere architettoniche (9 province)')
    print('═' * 55)
    ba_ok = 0
    for prov_slug, info in PROVINCE_INFO.items():
        print(f'\n  {info["nome"]}:')
        if rewrite_barriere(prov_slug, info):
            ba_ok += 1

    print(f'\n\nBarriere architettoniche: {ba_ok}/9 pagine riscritte')

    print('\n' + '═' * 55)
    print('SEZIONE 2: Pagine mancanti Messina')
    print('═' * 55)
    me_ok = 0
    for fn in [rewrite_messina_cila, rewrite_messina_ristrutturazione,
               rewrite_messina_sanatoria, rewrite_messina_dl]:
        print(f'\n  {fn.__name__}:')
        if fn():
            me_ok += 1
    print(f'\nMessina: {me_ok}/4 pagine riscritte')

    print('\n' + '═' * 55)
    print('SEZIONE 3: Pagine mancanti Catania')
    print('═' * 55)
    ca_ok = 0
    for fn in [rewrite_catania_sanatoria, rewrite_catania_dl, rewrite_catania_stima]:
        print(f'\n  {fn.__name__}:')
        if fn():
            ca_ok += 1
    print(f'\nCatania: {ca_ok}/3 pagine riscritte')

    total = ba_ok + me_ok + ca_ok
    print(f'\n{"═"*55}')
    print(f'TOTALE: {total}/16 pagine riscritte')
    print(f'Pagine di qualità nel sito: {28 + total}')
