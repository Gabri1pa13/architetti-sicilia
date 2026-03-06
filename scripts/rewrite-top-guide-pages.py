#!/usr/bin/env python3
"""
Riscrive le 10 pagine guide più importanti con contenuto sostanziale (700+ parole).
Mantiene: head, nav, breadcrumb, H1, phone-cta, related-links, footer.
Sostituisce: lede, sezioni H2, CTA urgente.
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


def build_article(parts, new_lede, new_content, city, urgency_title, urgency_body):
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


def rewrite_file(rel_path, new_lede, new_content, city,
                 urgency_title="Hai un progetto?",
                 urgency_body="Studio 4e segue pratiche edilizie, ristrutturazioni e sanatorie in Sicilia da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso."):
    filepath = ROOT / rel_path
    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    parts = get_article_parts(html)
    if not parts:
        print(f"SKIP (no article found): {rel_path}")
        return False

    new_article_inner = build_article(parts, new_lede, new_content, city, urgency_title, urgency_body)

    new_html = re.sub(
        r'<article class="article">.*?</article>',
        '<article class="article">' + new_article_inner + '</article>',
        html,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    plain = re.sub(r'<[^>]+>', ' ', new_article_inner)
    plain = re.sub(r'\s+', ' ', plain).strip()
    words = len(plain.split())
    print(f"✅ {Path(rel_path).name} — {words} parole")
    return True


# ─────────────────────────────────────────────────────────────
# CONTENUTI PAGINE
# ─────────────────────────────────────────────────────────────

PAGES = []

# ──────────────────────────────────────────────────────────────
# 1. Architetto a Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/architetto-a-palermo-come-impostare-un-progetto-senza-sorprese.html",
    city="Palermo",
    lede="A Palermo ogni ristrutturazione o intervento edilizio richiede un iter preciso: rilievo, pratica edilizia, direzione lavori e coordinamento con gli uffici comunali. Saltare l'ordine delle operazioni genera ritardi, costi extra e blocchi al rogito.",
    content="""
<h2>Quando è obbligatorio un architetto a Palermo</h2>
<p>Un architetto abilitato è obbligatorio ogni volta che si presenta una pratica edilizia al Comune di Palermo: CILA, SCIA o Permesso di Costruire. Il professionista assevera che le opere rispettino le norme tecniche, il Piano Regolatore e i vincoli specifici dell'immobile. A Palermo il Piano Particolareggiato per il Centro Storico impone verifiche aggiuntive su materiali, colori e tecnologie che solo un tecnico esperto del territorio conosce. Anche per interventi che non richiedono pratiche, la consulenza tecnica preventiva riduce il rischio di difetti costruttivi e vizi nascosti.</p>

<h2>Il rilievo: il primo passo obbligatorio</h2>
<p>Prima di qualsiasi progetto il rilievo metrico e lo stato di consistenza dell'immobile sono indispensabili. Un rilievo accurato comprende: misurazioni di tutti gli ambienti con tolleranze entro 2 cm, confronto tra planimetria catastale e stato reale (le difformità superiori al 2% vanno regolarizzate), identificazione di muri portanti, posizione e sezione degli impianti esistenti. A Palermo, dove molti edifici risalgono agli anni '50–'80 con modifiche mai documentate, la discrepanza tra catasto e realtà è molto frequente. Ignorarla espone il proprietario a sanzioni e al blocco del rogito.</p>

<h2>CILA, SCIA o Permesso di Costruire: quale pratica serve</h2>
<p>La scelta della pratica dipende dall'intervento:</p>
<ul>
<li><strong>CILA</strong>: manutenzione straordinaria interna senza modifiche strutturali (nuovo bagno, tramezzi, impianti). Efficacia immediata dopo il deposito allo Sportello Unico Edilizia (SUE) di Palermo</li>
<li><strong>SCIA</strong>: ristrutturazione parziale, modifica di prospetti, cambio di aperture esterne. Permette di iniziare dopo 30 giorni di silenzio-assenso</li>
<li><strong>Permesso di Costruire</strong>: ampliamenti, sopraelevazioni, interventi strutturali. Tempi medi a Palermo: 60–120 giorni</li>
</ul>
<p>Nel centro storico e nelle zone con vincolo paesaggistico quasi ogni intervento esterno richiede anche l'autorizzazione della Soprintendenza, con ulteriori 30–60 giorni di attesa.</p>

<h2>La direzione lavori: perché non rinunciarci</h2>
<p>La direzione lavori è obbligatoria per legge ogni volta che si deposita una pratica edilizia. Il direttore lavori (DL) non è un optional: è il tecnico che risponde legalmente della corretta esecuzione delle opere. A Palermo, dove i cantieri presentano frequentemente varianti non previste soprattutto in edifici storici, il DL gestisce le modifiche in corso d'opera, certifica gli stati di avanzamento e garantisce che l'opera finale corrisponda al progetto approvato. Senza DL nominato la pratica edilizia è invalida e il rogito viene bloccato.</p>

<h2>Come impostare il budget senza sorprese</h2>
<p>Il preventivo finale di un progetto a Palermo dipende da tre fattori spesso sottovalutati:</p>
<ol>
<li><strong>Verifica dello stato legittimo</strong>: difformità catastali o urbanistiche preesistenti vanno sanate prima o in parallelo ai lavori</li>
<li><strong>Qualità del capitolato</strong>: un capitolato analitico con materiali, cicli di posa e tolleranze riduce drasticamente le varianti a cantiere aperto</li>
<li><strong>Riserva di contingency</strong>: su edifici non ristrutturati da 20+ anni, prevedere il 10–15% in più rispetto al preventivo iniziale</li>
</ol>
<p>Studio 4e stima i costi con computo metrico voce per voce prima di aprire il cantiere, eliminando i "a corpo" che lasciano spazio agli extra non preventivati.</p>

<h2>Documenti da raccogliere prima del primo appuntamento</h2>
<p>Per impostare subito il lavoro in modo efficiente, è utile raccogliere in anticipo:</p>
<ul>
<li>Atto di provenienza dell'immobile</li>
<li>Planimetria catastale attuale</li>
<li>Titoli edilizi originali (concessione, licenza o condono)</li>
<li>Certificato di agibilità o di abitabilità</li>
<li>Regolamento condominiale (se applicabile)</li>
</ul>
<p>Se alcuni documenti mancano, Studio 4e effettua le visure necessarie prima di iniziare la progettazione.</p>
""",
    urgency_title="Rogito bloccato o immobile irregolare a Palermo?",
    urgency_body="Studio 4e gestisce sanatorie, accertamenti di conformità e pratiche edilizie a Palermo da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso."
))

# ──────────────────────────────────────────────────────────────
# 2. CILA a Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/cila-a-palermo-quando-serve-e-cosa-cambia-in-cantiere.html",
    city="Palermo",
    lede="La CILA (Comunicazione di Inizio Lavori Asseverata) è il titolo edilizio per la manutenzione straordinaria a Palermo. Si può iniziare il cantiere il giorno stesso del deposito, ma classificare male l'intervento blocca i lavori e crea problemi al rogito.",
    content="""
<h2>Interventi che richiedono la CILA a Palermo</h2>
<p>La CILA si applica agli interventi di manutenzione straordinaria che non modificano volumi, superfici e destinazione d'uso. A Palermo rientrano nella CILA: spostamento o aggiunta di servizi igienici con relativa tracciatura di pareti non portanti, rifacimento completo degli impianti elettrici e idraulici, apertura o chiusura di porte interne, sostituzione di pavimenti con modifica del massetto, installazione di sistemi di climatizzazione. Non serve la CILA per manutenzione ordinaria: tinteggiatura interna, sostituzione di serramenti della stessa misura, riparazione di impianti senza modifiche planimetriche.</p>

<h2>Cosa NON si può fare con una CILA (serve SCIA o permesso)</h2>
<p>Molti proprietari classificano erroneamente come CILA interventi che richiedono pratiche più complesse. A Palermo richiedono SCIA (non CILA): modifiche di prospetto o facciata, apertura o chiusura di finestre verso l'esterno, cambio di destinazione d'uso, demolizione e ricostruzione di tramezzi che modificano sostanzialmente la distribuzione. Richiedono il Permesso di Costruire: qualsiasi intervento su elementi strutturali (travi, pilastri, solai portanti), ampliamenti di superficie o volume, sopraelevazioni.</p>

<h2>Documenti necessari per la CILA a Palermo</h2>
<p>Il tecnico incaricato predispone la pratica sul portale telematico SUE del Comune di Palermo. I documenti richiesti:</p>
<ol>
<li>Asseverazione del tecnico abilitato (architetto o ingegnere) sulla conformità dell'intervento</li>
<li>Elaborati grafici: pianta dello stato attuale e di progetto (scala 1:100 o 1:50)</li>
<li>Relazione tecnica descrittiva delle opere</li>
<li>Documentazione fotografica dello stato ante-intervento</li>
<li>Estratto catastale e planimetria catastale aggiornata</li>
<li>Titolo di proprietà o altro diritto sull'immobile</li>
<li>Delibera condominiale (solo se l'intervento interessa parti comuni)</li>
</ol>

<h2>Tempi e procedura allo SUE di Palermo nel 2026</h2>
<p>Il SUE (Sportello Unico Edilizia) del Comune di Palermo riceve le pratiche esclusivamente in modalità telematica. Dopo il deposito digitale, la ricevuta viene rilasciata entro 1–3 giorni lavorativi. I lavori possono iniziare il giorno del deposito: la CILA è ad efficacia immediata, non richiede alcuna attesa. Il Comune ha 30 giorni per richiedere integrazioni. Se arriva una richiesta di integrazione i lavori devono sospendersi fino alla risposta. Studio 4e prepara le pratiche in modo da ridurre al minimo le richieste di integrazione.</p>

<h2>Cosa cambia in cantiere con la CILA aperta</h2>
<p>Dal momento del deposito, in cantiere devono essere presenti: copia della CILA con ricevuta, elaborati di progetto firmati, nominativo del direttore lavori. Il direttore lavori (obbligatorio per legge) controlla la conformità dell'esecuzione al progetto asseverato. Al termine dei lavori va depositata la CILA di fine lavori, anche se le opere sono state eseguite esattamente come previsto. Senza chiusura della pratica la CILA rimane aperta e blocca il rogito in caso di vendita o successione.</p>

<h2>Errori tipici che bloccano i cantieri a Palermo</h2>
<ul>
<li><strong>CILA al posto di SCIA</strong>: il Comune può emettere ordinanza di sospensione lavori</li>
<li><strong>Mancanza del direttore lavori</strong>: rende invalida la pratica</li>
<li><strong>CILA di fine lavori non depositata</strong>: la pratica aperta blocca il rogito</li>
<li><strong>Planimetria catastale obsoleta</strong>: il dato catastale deve riflettere lo stato ante-intervento</li>
<li><strong>Interventi in centro storico senza verifica vincoli</strong>: anche una CILA può richiedere pareri aggiuntivi in zone tutelate</li>
</ul>
""",
))

# ──────────────────────────────────────────────────────────────
# 3. Ristrutturazione appartamento Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/ristrutturazione-appartamento-a-palermo-tempi-fasi-e-documenti.html",
    city="Palermo",
    lede="Una ristrutturazione di appartamento a Palermo dura mediamente 4–8 mesi dal primo sopralluogo all'abitabilità. I ritardi nascono quasi sempre da tre cause: rilievo impreciso, documenti catastali non aggiornati, preventivo senza capitolato analitico.",
    content="""
<h2>Le 4 fasi di una ristrutturazione a Palermo (con tempi realistici)</h2>
<ol>
<li><strong>Analisi preliminare (2–4 settimane)</strong>: rilievo metrico, verifica dello stato legittimo urbanistico-catastale, ricognizione degli impianti, identificazione di vincoli condominiali e normativi</li>
<li><strong>Progettazione e pratiche edilizie (4–8 settimane)</strong>: elaborati grafici, scelta materiali e finiture, capitolato tecnico con computo metrico, deposito CILA o SCIA allo Sportello Unico Edilizia di Palermo</li>
<li><strong>Cantiere (8–20 settimane a seconda dell'ampiezza)</strong>: demolizioni, strutture, impianti, finiture. La sequenza corretta è determinante: gli impianti si installano prima delle finiture, non dopo</li>
<li><strong>Chiusura (2–3 settimane)</strong>: deposito fine lavori al SUE, variazione catastale DOCFA se necessaria, dichiarazioni di conformità degli impianti (elettrico, idraulico, gas)</li>
</ol>

<h2>Documenti da raccogliere prima di iniziare</h2>
<p>Raccogliere questi documenti in anticipo riduce tempi e costi del progetto:</p>
<ul>
<li>Atto di provenienza dell'immobile</li>
<li>Planimetria catastale attuale (da confrontare con lo stato reale)</li>
<li>Titoli edilizi originali: concessione o licenza edilizia, eventuali condoni o sanatorie</li>
<li>Certificato di agibilità o abitabilità</li>
<li>Schema degli impianti esistenti (se disponibile)</li>
<li>Regolamento condominiale, soprattutto per interventi su facciate o strutture</li>
</ul>
<p>Attenzione: a Palermo è molto frequente la difformità tra planimetria catastale e stato di fatto. Va regolarizzata prima del rogito.</p>

<h2>Quanto costa ristrutturare un appartamento a Palermo nel 2026</h2>
<p>I costi dipendono dallo stato dell'immobile, dalla complessità degli impianti e dalla qualità delle finiture. Stime indicative per il 2026:</p>
<ul>
<li><strong>Ristrutturazione leggera</strong> (finiture, impianti parziali, bagno): 450–700 €/mq</li>
<li><strong>Ristrutturazione media</strong> (bagni, cucina, impianti completi, pavimenti): 700–1.100 €/mq</li>
<li><strong>Ristrutturazione pesante</strong> (strutture, impianti completi, finiture premium): 1.100–1.800 €/mq</li>
</ul>
<p>A questi importi si aggiungono: onorario del professionista (6–12% dell'importo lavori), costi pratiche edilizie, eventuali sanatorie di difformità preesistenti.</p>

<h2>Vincoli specifici di Palermo da verificare</h2>
<p>Prima di avviare qualsiasi progetto a Palermo, verificare:</p>
<ul>
<li><strong>Centro storico</strong>: il Piano Particolareggiato Esecutivo limita materiali (no cappotto esterno su edifici storici), colori delle facciate, tipologia delle aperture. Molti interventi richiedono l'autorizzazione della Soprintendenza</li>
<li><strong>Zone paesaggistiche</strong>: presenti lungo la costa e vicino ai corsi d'acqua</li>
<li><strong>Zona sismica 2</strong>: tutti gli interventi su elementi strutturali richiedono autorizzazione sismica specifica</li>
<li><strong>Regolamento condominiale</strong>: può limitare orari di cantiere, uso degli ascensori per i materiali, interventi sulle facciate</li>
</ul>

<h2>Come scegliere un'impresa a Palermo</h2>
<p>Sul mercato palermitano la qualità delle imprese è molto variabile. Elementi da verificare prima di firmare:</p>
<ul>
<li>DURC aggiornato (Documento Unico di Regolarità Contributiva)</li>
<li>Iscrizione alla Camera di Commercio con codice ATECO edilizio</li>
<li>Referenze verificabili su lavori simili completati negli ultimi 2 anni</li>
<li>Disponibilità a firmare un capitolato dettagliato voce per voce (non "a corpo")</li>
<li>Polizza RC professionale e assicurazione cantiere</li>
</ul>
<p>Non affidarsi mai a chi propone di lavorare senza pratiche edilizie o di "sistemare i documenti dopo i lavori".</p>

<h2>Il controllo del cantiere con la direzione lavori</h2>
<p>La direzione lavori è obbligatoria per legge quando si deposita una pratica edilizia. Il direttore lavori verifica la conformità delle opere al progetto approvato, controlla la qualità dell'esecuzione (impermeabilizzazioni, pendenze scarichi, isolamenti), gestisce le varianti necessarie e certifica gli stati di avanzamento per i pagamenti all'impresa. Studio 4e offre progettazione e direzione lavori come servizio integrato: la stessa figura che ha progettato segue il cantiere fino alla consegna.</p>
""",
))

# ──────────────────────────────────────────────────────────────
# 4. Sanatoria edilizia Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html",
    city="Palermo",
    lede="A Palermo le difformità edilizie riguardano la maggior parte degli immobili costruiti prima del 1985. Non tutto può essere sanato: la distinzione tra abuso sanabile e non sanabile è tecnica e dipende dalla data, dalla tipologia e dalla localizzazione dell'opera.",
    content="""
<h2>Condono edilizio vs. accertamento di conformità: due strumenti diversi</h2>
<p>Esistono due strumenti distinti per regolarizzare gli abusi edilizi:</p>
<ul>
<li><strong>Condono edilizio</strong>: amnistie straordinarie nazionali che hanno coperto opere realizzate fino a date precise. Le ultime leggi di condono (1985, 1994, 2003) avevano scadenze perentorie per la presentazione delle domande: non è possibile presentarne di nuove oggi</li>
<li><strong>Accertamento di conformità (sanatoria ordinaria)</strong>: regolarizzazione di opere realizzate senza titolo o in difformità, ma conformi alla normativa urbanistica vigente sia al momento della realizzazione sia al momento della domanda (principio della doppia conformità). Si può presentare in qualsiasi momento, senza scadenze</li>
</ul>

<h2>La doppia conformità: il criterio decisivo</h2>
<p>L'accertamento di conformità richiede che l'opera sia stata conforme alla normativa sia all'epoca della realizzazione sia oggi. Questo criterio esclude dalla sanatoria ordinaria:</p>
<ul>
<li>Ampliamenti in zone dove la normativa non lo permetteva neanche al momento della costruzione</li>
<li>Opere in aree soggette a vincolo paesaggistico o idrogeologico realizzate senza le dovute autorizzazioni</li>
<li>Abusi in zone agricole o di rispetto dei corsi d'acqua</li>
<li>Strutture realizzate in violazione della normativa antisismica (a Palermo, zona sismica 2, particolarmente rilevante)</li>
</ul>

<h2>Difformità più frequenti a Palermo</h2>
<p>Studio 4e gestisce decine di pratiche di sanatoria a Palermo ogni anno. Le irregolarità più comuni:</p>
<ul>
<li>Tramezzi spostati rispetto alla planimetria catastale originale</li>
<li>Bagni aggiunti o riposizionati rispetto al titolo edilizio</li>
<li>Finestre allargate o ridotte rispetto al progetto approvato</li>
<li>Verande o chiusure di logge realizzate senza pratica</li>
<li>Variazioni parziali di destinazione d'uso non autorizzate</li>
</ul>
<p>Molte di queste difformità sono sanabili con l'accertamento di conformità, quando sussistono i requisiti di doppia conformità.</p>

<h2>La procedura di sanatoria al SUE di Palermo (tempi reali)</h2>
<ol>
<li>Rilievo dello stato di fatto e confronto con atto di provenienza e planimetria catastale</li>
<li>Verifica della doppia conformità con il PRG vigente e quello dell'epoca</li>
<li>Preparazione degli elaborati: stato di fatto, stato di progetto, relazione tecnica asseverata</li>
<li>Deposito della domanda di accertamento di conformità allo SUE di Palermo con pagamento delle sanzioni</li>
<li>Attesa della determinazione comunale: teoricamente 60 giorni, in pratica a Palermo 3–6 mesi</li>
<li>Rilascio della concessione in sanatoria: il documento che legalizza le opere</li>
<li>Aggiornamento catastale DOCFA (se ci sono variazioni di superficie o distribuzione)</li>
</ol>

<h2>Costi della sanatoria a Palermo</h2>
<p>Il costo totale si compone di:</p>
<ul>
<li><strong>Sanzione amministrativa</strong>: calcolata sul valore delle opere abusive (da poche centinaia a decine di migliaia di euro)</li>
<li><strong>Oneri di urbanizzazione</strong>: dovuti se le opere aumentano il carico urbanistico</li>
<li><strong>Onorario tecnico</strong>: 1.500–5.000 € per pratiche standard, più per casi complessi</li>
<li><strong>Aggiornamento catastale</strong>: 200–500 € per il DOCFA</li>
</ul>
<p>Studio 4e fornisce una stima del costo totale prima di avviare la pratica, senza sorprese.</p>

<h2>Cosa succede se non si regolarizza</h2>
<p>Le difformità non sanate creano problemi concreti:</p>
<ul>
<li>Il notaio può rifiutare il rogito in presenza di abusi rilevanti</li>
<li>Le banche non concedono mutui su immobili con irregolarità edilzie</li>
<li>In caso di successione i coeredi devono regolarizzare prima di procedere alla divisione</li>
<li>Il Comune può emettere ordinanze di demolizione per abusi non prescritti</li>
</ul>
""",
    urgency_title="Rogito bloccato per abusi edilizi a Palermo?",
    urgency_body="Studio 4e segue accertamenti di conformità e sanatorie a Palermo da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per capire cosa si può regolarizzare e i costi stimati."
))

# ──────────────────────────────────────────────────────────────
# 5. Direzione lavori Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/direzione-lavori-a-palermo-cosa-controlla-il-direttore-lavori.html",
    city="Palermo",
    lede="La direzione lavori a Palermo è obbligatoria per legge ogni volta che si deposita una pratica edilizia. Non è un optional: è la figura che tutela il committente, garantisce la conformità al progetto e risponde legalmente dell'esecuzione delle opere.",
    content="""
<h2>Cosa fa concretamente il direttore lavori a Palermo</h2>
<p>Il direttore lavori (DL) è il tecnico nominato dal committente che controlla l'esecuzione del cantiere. Le sue responsabilità concrete:</p>
<ul>
<li>Verificare che le opere siano eseguite in conformità al progetto approvato e al capitolato</li>
<li>Controllare la qualità dei materiali in opera (campioni, certificati CE, documenti di trasporto)</li>
<li>Gestire le varianti necessarie in corso d'opera e documentarle con perizie scritte</li>
<li>Redigere i Certificati di Stato Avanzamento Lavori (SAL) che autorizzano i pagamenti all'impresa</li>
<li>Emettere il Certificato di Regolare Esecuzione al termine dei lavori</li>
<li>Depositare la pratica di fine lavori allo Sportello Unico Edilizia di Palermo</li>
</ul>

<h2>Perché la direzione lavori è obbligatoria per legge</h2>
<p>Il DPR 380/2001 (Testo Unico Edilizia) stabilisce l'obbligo della direzione lavori per qualsiasi intervento soggetto a CILA, SCIA o Permesso di Costruire. Il tecnico incaricato risponde penalmente e civilmente delle opere eseguite. La sua firma sugli elaborati finali è condizione necessaria per il deposito della pratica di fine lavori. Senza DL nominato la pratica edilizia è invalida, il cantiere è irregolare e l'immobile non può essere venduto regolarmente. A Palermo i controlli degli uffici tecnici sono particolarmente frequenti nel centro storico e nelle zone vincolate.</p>

<h2>La differenza tra DL e coordinatore per la sicurezza</h2>
<p>Queste due figure vengono spesso confuse:</p>
<ul>
<li><strong>Direttore Lavori</strong>: verifica la conformità tecnico-urbanistica delle opere al progetto approvato. Sempre obbligatorio con pratiche edilizie</li>
<li><strong>Coordinatore per la Sicurezza in Esecuzione (CSE)</strong>: obbligatorio quando nel cantiere operano più imprese contemporaneamente. Controlla le misure di sicurezza per i lavoratori</li>
</ul>
<p>Per cantieri con una sola impresa il CSE non è obbligatorio. Quando operano più imprese (es. edile + impianti + serramenti) entrambe le figure sono necessarie.</p>

<h2>DL e varianti: come si gestiscono le modifiche in corso d'opera</h2>
<p>In cantiere, soprattutto su edifici storici palermitani, emergono frequentemente situazioni non previste: muri portanti diversi da quelli indicati nelle planimetrie, impianti fuori posto, livelli non conformi. Il DL gestisce queste varianti documentandole formalmente con perizie tecniche. Le varianti rilevanti devono essere comunicate al SUE con apposita pratica. Quelle minori vengono riportate negli elaborati di fine lavori. Senza questa documentazione il cantiere può essere considerato in difformità dal progetto approvato.</p>

<h2>Come scegliere il direttore lavori a Palermo</h2>
<p>Il DL deve avere: iscrizione all'albo professionale (architetti o ingegneri di Palermo), polizza RC aggiornata, esperienza documentata su cantieri simili. È importante che il DL sia un soggetto diverso dall'impresa esecutrice (conflitto di interessi) e preferibilmente lo stesso professionista che ha progettato le opere. Studio 4e offre progettazione e direzione lavori come servizio integrato: la stessa persona che ha progettato segue il cantiere, conosce ogni dettaglio del progetto e gestisce le varianti con piena cognizione di causa.</p>

<h2>Costi della direzione lavori a Palermo nel 2026</h2>
<p>Il compenso del DL varia in base all'importo e alla complessità dei lavori. Riferimenti orientativi per il mercato palermitano:</p>
<ul>
<li>Ristrutturazione leggera con CILA: 3–5% dell'importo lavori</li>
<li>Ristrutturazione media con SCIA: 4–7%</li>
<li>Cantieri complessi o con vincoli (centro storico, zone paesaggistiche): 6–10%</li>
</ul>
<p>Studio 4e fornisce un preventivo tecnico completo (progettazione + DL) prima di iniziare.</p>
""",
))

# ──────────────────────────────────────────────────────────────
# 6. Architetto a Catania
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/catania/architetto-a-catania-come-impostare-un-progetto-senza-sorprese.html",
    city="Catania",
    lede="A Catania progettare una ristrutturazione significa confrontarsi con vincoli specifici: la classificazione sismica di zona 2, la presenza del Parco dell'Etna in molte aree limitrofe e il centro storico barocco tutelato dall'UNESCO. Un professionista che conosce il territorio fa la differenza tra un cantiere che procede e uno bloccato.",
    content="""
<h2>Quando è obbligatorio un architetto a Catania</h2>
<p>Un architetto abilitato è obbligatorio per ogni pratica edilizia al Comune di Catania o nei comuni della provincia. Le specificità locali rendono la figura tecnica ancora più importante rispetto ad altre città:</p>
<ul>
<li><strong>Centro storico barocco UNESCO</strong>: cambio di serramenti, colori di facciata, pavimentazioni esterne richiedono pareri specifici della Soprintendenza di Catania</li>
<li><strong>Parco dell'Etna</strong>: molte zone periferiche ricadono nell'area del Parco, con normative aggiuntive di compatibilità ambientale</li>
<li><strong>Zona sismica 2</strong>: qualsiasi intervento su elementi portanti richiede calcoli strutturali certificati da un ingegnere strutturista</li>
</ul>

<h2>Il rilievo a Catania: attenzione alla costruzione su basalto</h2>
<p>A Catania molti edifici storici sono costruiti sul basalto lavico, con fondazioni e strutture che spesso non risultano nelle planimetrie originali. Il rilievo iniziale deve comprendere: verifica della struttura portante (obbligatoria per edifici pre-1980 in zona sismica), misurazione precisa delle aperture (spesso irregolari negli edifici storici), confronto con la planimetria catastale. Una specificità catanese sono le cavità sotterranee presenti in alcune zone del centro che possono influenzare la stabilità delle fondazioni: vanno identificate prima di qualsiasi intervento.</p>

<h2>CILA, SCIA o Permesso di Costruire a Catania</h2>
<p>Le categorie di pratiche edilizie sono le stesse nazionali ma con specificità locali:</p>
<ul>
<li><strong>CILA</strong>: manutenzione straordinaria senza modifiche strutturali. Deposito telematico allo SUE di Catania, efficacia immediata</li>
<li><strong>SCIA</strong>: ristrutturazione con modifiche di prospetto. I 30 giorni di attesa a Catania sono in genere rispettati, ma in centro storico è necessaria l'autorizzazione paesaggistica preventiva</li>
<li><strong>Permesso di Costruire</strong>: interventi strutturali, ampliamenti, sopraelevazioni. Tempi medi a Catania: 90–150 giorni</li>
<li><strong>Nulla Osta Parco Etna</strong>: per interventi in prossimità del Parco, aggiunge 30–60 giorni all'iter</li>
</ul>

<h2>Il rischio sismico a Catania: progettazione strutturale</h2>
<p>Catania è classificata in zona sismica 2 con storia di eventi sismici importanti (terremoto del 1693). Ogni intervento su strutture portanti richiede: progetto strutturale firmato da ingegnere abilitato, autorizzazione sismica preventiva dell'Ufficio del Genio Civile di Catania, collaudo statico al termine dei lavori. Questo vale anche per ristrutturazioni apparentemente "leggere" che toccano solai, travi o pilastri. Studio 4e coordina la progettazione architettonica con quella strutturale, garantendo un iter senza sorprese.</p>

<h2>Direzione lavori a Catania: specificità costruttive locali</h2>
<p>La direzione lavori a Catania richiede conoscenza della costruzione su basalto e tufo lavico: materiali con comportamento strutturale e igrometrico molto diverso dal laterizio del nord Italia. I DL che non conoscono questi materiali rischiano di approvare finiture incompatibili con il substrato, impermeabilizzazioni inadeguate o consolidamenti sbagliati. Studio 4e opera a Catania da anni con esperienza specifica sulle costruzioni etnee.</p>

<h2>Costi orientativi a Catania nel 2026</h2>
<p>I costi a Catania sono generalmente comparabili a Palermo:</p>
<ul>
<li>Ristrutturazione leggera: 400–650 €/mq</li>
<li>Ristrutturazione media: 650–1.050 €/mq</li>
<li>Ristrutturazione pesante: 1.050–1.700 €/mq</li>
</ul>
<p>In centro storico il costo aumenta del 15–25% per via dei vincoli e delle difficoltà logistiche di cantiere (ZTL, accessi stretti, smaltimento differenziato dei materiali storici).</p>
""",
))

# ──────────────────────────────────────────────────────────────
# 7. CILA a Catania
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/catania/cila-a-catania-quando-serve-e-cosa-cambia-in-cantiere.html",
    city="Catania",
    lede="La CILA a Catania copre gli interventi di manutenzione straordinaria senza modifiche di volumi, strutture o destinazione d'uso. A Catania, in zona sismica 2, occorre valutare con attenzione se l'intervento tocca elementi strutturali che richiedono autorizzazione sismica specifica.",
    content="""
<h2>Interventi che richiedono la CILA a Catania</h2>
<p>La CILA a Catania si applica agli stessi interventi validi a livello nazionale: manutenzione straordinaria interna che non modifica volumi, superfici, strutture portanti o destinazione d'uso. Rientrano nella CILA: spostamento di servizi igienici con tracciatura di pareti non portanti, rifacimento impianti elettrici e idraulici, sostituzione di pavimenti con modifica del massetto, installazione di climatizzatori con aperture di piccolo taglio, apertura o chiusura di porte interne. Non servono per manutenzione ordinaria (tinteggiatura, sostituzione serramenti stessa misura, riparazioni puntuali).</p>

<h2>CILA e zona sismica a Catania: quando serve qualcosa in più</h2>
<p>Catania è in zona sismica 2. Questo significa che anche interventi apparentemente semplici possono richiedere autorizzazione sismica se riguardano elementi strutturali. In particolare, a Catania non è possibile presentare sola CILA per: demolizione e ricostruzione di pareti in muratura portante (anche se il progetto le chiama "tramezzi"), rinforzi o consolidamenti di strutture esistenti, modifica di aperture in pareti portanti. In questi casi serve sempre la valutazione di un ingegnere strutturista e la richiesta all'Ufficio del Genio Civile di Catania.</p>

<h2>Documenti per la CILA al SUE di Catania</h2>
<p>Il tecnico deposita la pratica telematicamente sullo Sportello Unico Edilizia del Comune di Catania. Documenti richiesti:</p>
<ol>
<li>Asseverazione del tecnico abilitato sulla conformità dell'intervento alle norme</li>
<li>Elaborati grafici: piante stato attuale e di progetto</li>
<li>Relazione tecnica descrittiva</li>
<li>Documentazione fotografica dello stato ante-intervento</li>
<li>Planimetria catastale aggiornata ed estratto catastale</li>
<li>Titolo di proprietà</li>
<li>Delibera condominiale (se si toccano parti comuni)</li>
</ol>
<p>Per immobili in centro storico tutelato UNESCO, può essere necessario allegare documentazione fotografica aggiuntiva e ottenere il parere preventivo della Soprintendenza di Catania.</p>

<h2>Tempi di deposito e procedura al Comune di Catania</h2>
<p>Lo SUE di Catania riceve le pratiche telematicamente. Dopo il deposito la ricevuta viene emessa entro 1–3 giorni lavorativi. La CILA è ad efficacia immediata: i lavori possono iniziare il giorno del deposito. Il Comune ha 30 giorni per richiedere integrazioni o segnalare irregolarità. In caso di richiesta di integrazione, i lavori devono essere sospesi fino alla risposta del tecnico. Studio 4e prepara le pratiche in modo completo per ridurre al minimo le integrazioni.</p>

<h2>La CILA di fine lavori a Catania</h2>
<p>Al termine dei lavori va obbligatoriamente depositata la CILA di fine lavori, che chiude formalmente la pratica. Se durante il cantiere sono sorte varianti rispetto al progetto originale, queste vanno documentate nella relazione finale. Senza chiusura della CILA, la pratica rimane tecnicamente aperta e genera problemi in caso di vendita, successione o richiesta di mutuo.</p>

<h2>Errori frequenti nelle CILA a Catania</h2>
<ul>
<li>Non verificare se l'intervento tocca elementi portanti in muratura lavica (difficile da riconoscere a vista)</li>
<li>Omettere il parere della Soprintendenza per immobili in centro storico UNESCO</li>
<li>Non depositare la CILA di fine lavori</li>
<li>Utilizzare planimetria catastale non aggiornata allo stato ante-intervento</li>
<li>Non nominare il direttore lavori (obbligatorio per legge)</li>
</ul>
""",
))

# ──────────────────────────────────────────────────────────────
# 8. Ristrutturazione appartamento Catania
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/catania/ristrutturazione-appartamento-a-catania-tempi-fasi-e-documenti.html",
    city="Catania",
    lede="Ristrutturare un appartamento a Catania presenta sfide specifiche: la zona sismica 2 impone calcoli strutturali per qualsiasi intervento sulle parti portanti, i centri storici in pietra lavica richiedono spesso autorizzazioni paesaggistiche, e le difformità catastali negli edifici pre-1980 sono molto diffuse.",
    content="""
<h2>Le fasi di una ristrutturazione a Catania</h2>
<ol>
<li><strong>Analisi preliminare (2–4 settimane)</strong>: rilievo metrico, verifica dello stato legittimo, identificazione della struttura portante (fondamentale in zona sismica), ricognizione degli impianti esistenti, analisi dei vincoli</li>
<li><strong>Progettazione e pratiche (4–10 settimane)</strong>: elaborati grafici, eventuale progetto strutturale, deposito CILA o SCIA, autorizzazioni aggiuntive (Soprintendenza, Parco Etna se applicabile)</li>
<li><strong>Cantiere (8–20 settimane)</strong>: demolizioni, strutture, impianti, finiture nella sequenza corretta</li>
<li><strong>Chiusura (2–4 settimane)</strong>: fine lavori al SUE, eventuale collaudo statico, variazione catastale DOCFA, conformità impianti</li>
</ol>

<h2>Il rischio sismico nelle ristrutturazioni catanesi</h2>
<p>Catania è in zona sismica 2: qualsiasi intervento che interessa la struttura portante dell'edificio (anche una singola trave o un pilastro) richiede:</p>
<ul>
<li>Progetto strutturale firmato da ingegnere abilitato</li>
<li>Autorizzazione sismica preventiva dell'Ufficio del Genio Civile di Catania (tempi medi: 30–60 giorni)</li>
<li>Collaudo statico al termine dei lavori strutturali</li>
</ul>
<p>Questo vale anche per interventi che sembrano minori: consolidamento di un solaio ammalorato, apertura di una porta in una parete portante, installazione di una scala interna che appoggia su una trave esistente.</p>

<h2>Documenti essenziali prima di iniziare a Catania</h2>
<ul>
<li>Atto di provenienza con storia delle compravendite</li>
<li>Planimetria catastale (spesso discordante dallo stato reale negli edifici storici catanesi)</li>
<li>Titoli edilizi originali (concessione, licenza, eventuale condono)</li>
<li>Certificato di agibilità o abitabilità</li>
<li>Documentazione strutturale originale (raramente disponibile per edifici pre-1960)</li>
<li>Regolamento condominiale</li>
</ul>
<p>Per gli edifici nel centro storico è spesso necessario anche un'indagine diagnostica sulle murature (martinetto piatto, carotaggio) prima di progettare qualsiasi intervento strutturale.</p>

<h2>Quanto costa ristrutturare a Catania nel 2026</h2>
<p>Stime indicative per appartamenti a Catania:</p>
<ul>
<li><strong>Ristrutturazione leggera</strong> (finiture, impianti parziali): 420–680 €/mq</li>
<li><strong>Ristrutturazione media</strong> (bagni, cucina, impianti completi): 680–1.080 €/mq</li>
<li><strong>Ristrutturazione pesante</strong> (strutture, impianti totali, finiture premium): 1.080–1.750 €/mq</li>
</ul>
<p>In centro storico il costo aumenta del 15–25% per logistica, vincoli della Soprintendenza e compatibilità dei materiali con la pietra lavica.</p>

<h2>Vincoli del centro storico di Catania</h2>
<p>Il centro storico barocco di Catania è patrimonio UNESCO. Gli interventi su edifici storici richiedono:</p>
<ul>
<li>Parere della Soprintendenza di Catania per modifiche di facciata, serramenti, balconi, cornicioni</li>
<li>Materiali compatibili con l'architettura barocca (no PVC in facciata, no cappotto esterno)</li>
<li>Colori delle facciate approvati dal piano del colore comunale</li>
<li>Criteri di reversibilità per interventi su elementi di pregio</li>
</ul>

<h2>Come scegliere un'impresa a Catania</h2>
<p>Verificare prima di firmare: DURC aggiornato, esperienza documentata su edifici in zona sismica e su costruzioni in pietra lavica o tufo, referenze verificabili, disponibilità a firmare capitolato analitico. Diffidare di chi propone di "fare senza pratiche" o di gestire l'autorizzazione sismica "in seguito". A Catania un cantiere irregolare in zona sismica è soggetto a sanzioni molto severe.</p>
""",
))

# ──────────────────────────────────────────────────────────────
# 9. Architetto a Messina
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/messina/architetto-a-messina-come-impostare-un-progetto-senza-sorprese.html",
    city="Messina",
    lede="A Messina, città ricostruita dopo il terremoto del 1908 con normative antisismiche pionieristiche, ogni intervento edilizio deve fare i conti con la storia costruttiva dell'edificio. Il Piano Regolatore di Messina, le zone costiere soggette a vincolo paesaggistico e l'area metropolitana dello Stretto rendono l'iter normativo tra i più articolati della Sicilia.",
    content="""
<h2>Quando è obbligatorio un architetto a Messina</h2>
<p>Un architetto abilitato è obbligatorio per qualsiasi pratica edilizia al Comune di Messina o nei comuni della provincia. Le specificità locali che rendono indispensabile la competenza tecnica locale:</p>
<ul>
<li><strong>Edifici post-1908</strong>: la ricostruzione avvenne con tecnologie miste (cemento armato primitivo, murature in laterizio, acciaio) non sempre documentate nei catasti</li>
<li><strong>Zona sismica 1</strong>: Messina è in zona sismica 1, la più elevata in Italia — tutti gli interventi strutturali richiedono autorizzazione al Genio Civile di Messina</li>
<li><strong>Vincolo paesaggistico costiero</strong>: ampi tratti del litorale messinese ricadono in zone vincolate che richiedono l'autorizzazione della Soprintendenza</li>
<li><strong>Area metropolitana dello Stretto</strong>: normative specifiche per interventi nei comuni di Reggio Calabria e Messina connessi ai progetti infrastrutturali</li>
</ul>

<h2>Il rilievo a Messina: strutture del dopoguerra</h2>
<p>Dopo il terremoto del 1908, Messina fu ricostruita in fretta con tecniche miste: edifici "antisismici" dell'epoca con telai in cemento armato povero, murature di tufo, rinforzi in acciaio. Queste strutture oggi hanno oltre 100 anni e le planimetrie originali spesso non corrispondono allo stato reale. Un rilievo strutturale preliminare è fondamentale prima di qualsiasi progetto di ristrutturazione, soprattutto per identificare quali pareti sono portanti e quali no.</p>

<h2>La zona sismica 1 a Messina: implicazioni pratiche</h2>
<p>Messina è classificata in zona sismica 1 (massima pericolosità in Italia). Questo comporta:</p>
<ul>
<li>Progetto strutturale obbligatorio per qualsiasi intervento che tocchi elementi portanti</li>
<li>Autorizzazione preventiva dell'Ufficio del Genio Civile di Messina per lavori strutturali (tempi: 45–90 giorni)</li>
<li>Collaudo statico obbligatorio al termine dei lavori strutturali</li>
<li>Obbligo di miglioramento sismico in caso di ristrutturazione pesante (oltre il 25% del valore dell'immobile)</li>
</ul>
<p>Studio 4e coordina la progettazione architettonica con quella strutturale, con ingegneri con esperienza specifica in zona sismica 1.</p>

<h2>Pratiche edilizie al SUE di Messina</h2>
<p>Lo Sportello Unico Edilizia del Comune di Messina riceve le pratiche telematicamente. Le categorie di intervento seguono le stesse norme nazionali:</p>
<ul>
<li><strong>CILA</strong>: manutenzione straordinaria interna senza modifiche strutturali. Efficacia immediata</li>
<li><strong>SCIA</strong>: ristrutturazione con modifiche di prospetto. 30 giorni di attesa</li>
<li><strong>Permesso di Costruire</strong>: interventi strutturali, ampliamenti, sopraelevazioni. Tempi medi a Messina: 90–180 giorni</li>
</ul>
<p>Per le zone con vincolo paesaggistico costiero, quasi ogni intervento esterno richiede anche il nulla osta della Soprintendenza di Messina, con ulteriori 30–60 giorni.</p>

<h2>Costi orientativi a Messina nel 2026</h2>
<p>I costi di ristrutturazione a Messina sono simili alle altre città siciliane:</p>
<ul>
<li>Ristrutturazione leggera: 430–680 €/mq</li>
<li>Ristrutturazione media: 680–1.080 €/mq</li>
<li>Ristrutturazione pesante: 1.080–1.750 €/mq</li>
</ul>
<p>In zona sismica 1, l'adeguamento o miglioramento sismico può aggiungere il 20–40% al costo base della ristrutturazione strutturale.</p>

<h2>Studio 4e a Messina e provincia</h2>
<p>Studio 4e opera in tutta la provincia di Messina gestendo pratiche edilizie, ristrutturazioni, sanatorie e direzione lavori. La conoscenza del territorio messinese — uffici comunali, Soprintendenza, Genio Civile — permette di definire dall'inizio i tempi e i costi reali del progetto, senza sorprese a cantiere aperto.</p>
""",
))

# ──────────────────────────────────────────────────────────────
# 10. Stima costi ristrutturazione Palermo
# ──────────────────────────────────────────────────────────────
PAGES.append(dict(
    path="guide/palermo/stima-costi-ristrutturazione-a-palermo-come-leggere-un-preventivo.html",
    city="Palermo",
    lede="A Palermo un preventivo di ristrutturazione senza capitolato allegato non è un preventivo: è una stima a corpo che può raddoppiare. Imparare a leggere un preventivo vale quanto scegliere l'impresa giusta.",
    content="""
<h2>Costi medi di ristrutturazione a Palermo nel 2026</h2>
<p>Prima di ricevere qualsiasi preventivo, è utile avere un riferimento di mercato per valutare le offerte ricevute:</p>
<ul>
<li><strong>Manutenzione ordinaria</strong> (tinteggiatura, piccole riparazioni): 80–150 €/mq</li>
<li><strong>Ristrutturazione leggera</strong> (finiture, parziale impianti, bagno): 450–700 €/mq</li>
<li><strong>Ristrutturazione media</strong> (bagni completi, cucina, impianti, pavimenti): 700–1.100 €/mq</li>
<li><strong>Ristrutturazione pesante</strong> (strutture, impianti totali, finiture premium): 1.100–1.800 €/mq</li>
</ul>
<p>Questi valori si riferiscono a lavori edili ed impiantistici. Non includono: onorario del professionista (6–12%), pratiche edilizie, mobili su misura, elettrodomestici.</p>

<h2>Preventivo a corpo vs. preventivo analitico: la differenza che conta</h2>
<p>La distinzione più importante da comprendere:</p>
<ul>
<li><strong>Preventivo a corpo (forfait)</strong>: un'unica cifra per "fare tutto". Non elenca materiali, quantità, prezzi unitari. Qualsiasi modifica diventa un extra a discrezione dell'impresa. Difficile da confrontare con altri preventivi. È il tipo di preventivo che genera la maggior parte dei contenziosi a Palermo</li>
<li><strong>Preventivo analitico con capitolato</strong>: ogni voce di lavoro è descritta con quantità, unità di misura, prezzo unitario e importo. Permette di confrontare preventivi diversi voce per voce. Le varianti si calcolano ai prezzi concordati. Questo è l'unico strumento che protegge il committente</li>
</ul>

<h2>Le voci che mancano sempre nei preventivi</h2>
<p>I preventivi a corpo a Palermo escludono sistematicamente voci che diventeranno extra durante il cantiere:</p>
<ul>
<li>Smaltimento materiali di risulta (costo significativo per grandi demolizioni)</li>
<li>Verniciatura e finitura dei soffitti (spesso "esclusa" e poi richiesta come extra)</li>
<li>Sigillature e raccordi tra finiture diverse (bagno/pavimento, pareti/soffitto)</li>
<li>Ponteggi interni per soffitti alti</li>
<li>Protezione di pavimenti e infissi durante il cantiere</li>
<li>Allacciamenti provvisori di cantiere (acqua, luce)</li>
<li>Pulizie finali</li>
</ul>

<h2>Il computo metrico: l'unico strumento di confronto reale</h2>
<p>Il computo metrico è un documento tecnico che elenca tutte le voci di lavoro con le rispettive quantità misurate. Viene preparato dall'architetto o dal geometra prima di richiedere i preventivi alle imprese. Con il computo metrico:</p>
<ul>
<li>Tutte le imprese quotano le stesse quantità e le stesse specifiche tecniche</li>
<li>Il confronto tra preventivi diversi è immediato e oggettivo</li>
<li>Le varianti in corso d'opera si calcolano ai prezzi unitari già concordati</li>
<li>Il direttore lavori può certificare il lavoro eseguito rispetto a quello concordato</li>
</ul>
<p>Studio 4e prepara il computo metrico prima di aprire il cantiere per ogni progetto, indipendentemente dall'importo.</p>

<h2>Come confrontare preventivi di imprese diverse</h2>
<p>Se non hai il computo metrico del professionista, verifica almeno questi elementi prima di scegliere:</p>
<ol>
<li>Le imprese quotano le stesse opere? (es. stesse quantità di piastrelle, stesso tipo di impianto)</li>
<li>I materiali sono specificati per marca e tipo o genericamente "a scelta"?</li>
<li>Sono incluse le finiture (primer, stucco, verniciatura)?</li>
<li>Sono inclusi smaltimento e trasporto dei rifiuti?</li>
<li>Il preventivo include IVA e contributi previdenziali del tecnico?</li>
</ol>
<p>Una differenza di prezzo superiore al 30% tra preventivi per lo stesso lavoro indica quasi sempre che non si stanno confrontando le stesse cose.</p>

<h2>Le garanzie da richiedere sempre</h2>
<p>Prima di firmare qualsiasi contratto con un'impresa a Palermo:</p>
<ul>
<li>DURC (Documento Unico di Regolarità Contributiva) valido</li>
<li>Polizza responsabilità civile professionale e assicurazione cantiere</li>
<li>Garanzia decennale per vizi costruttivi (obbligatoria per legge per alcuni lavori)</li>
<li>Cronoprogramma scritto con date di inizio e fine cantiere</li>
<li>Modalità di pagamento legate agli stati di avanzamento lavori (non anticipi fissi)</li>
</ul>
""",
))


# ─────────────────────────────────────────────────────────────
# ESECUZIONE
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Riscrittura pagine guide con contenuto sostanziale...\n")
    ok = 0
    for page in PAGES:
        result = rewrite_file(
            page["path"],
            page["lede"],
            page["content"],
            page["city"],
            page.get("urgency_title", f"Hai un progetto a {page['city']}?"),
            page.get("urgency_body",
                     f"Studio 4e segue pratiche edilizie, ristrutturazioni e sanatorie a {page['city']} "
                     "da oltre 20 anni. <strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso.")
        )
        if result:
            ok += 1
    print(f"\n✅ Completato: {ok}/{len(PAGES)} pagine riscritte")
