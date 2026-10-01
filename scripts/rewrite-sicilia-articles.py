#!/usr/bin/env python3
"""
Riscrive gli articoli /sicilia/ ad alto intento di ricerca con contenuto
sostanziale (900+ parole), FAQ visibili, schema BlogPosting + FAQPage,
dateModified aggiornato e link interni verso servizi e guide.

Gli URL non cambiano: si sostituiscono solo <title>, meta description,
og/twitter, il corpo dell'<article> e si aggiungono gli schema JSON-LD.

Uso:
    python3 scripts/rewrite-sicilia-articles.py
"""
import html
import json
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://architettisicilia.it"
TODAY = "2026-10-01"
UPDATED_LABEL = "ottobre 2026"
PHONE = "+393299736697"

ARTICLES = [
    # ------------------------------------------------------------------
    {
        "file": "ecobonus-e-sismabonus-sicilia-2026-quali-incentivi-sono-rimasti.html",
        "title": "Bonus casa 2026 in Sicilia: ecobonus, sismabonus e cosa cambia nel 2027",
        "description": "Bonus ristrutturazione, ecobonus e sismabonus 2026 al 50% (prima casa) e 36%: requisiti, limiti, errori che fanno perdere la detrazione e il calo previsto dal 2027.",
        "lede": "Nel 2026 i tre bonus edilizi rimasti (ristrutturazione, ecobonus e sismabonus) valgono il 50% sull'abitazione principale e il 36% sugli altri immobili. Dal 2027 è previsto un calo al 36% e al 30%: chi ha un progetto in Sicilia ha pochi mesi per impostare bene pratiche e pagamenti.",
        "service": ("/servizi/efficientamento-energetico-e-comfort-abitativo.html", "Efficientamento energetico e comfort abitativo"),
        "body": """
<h2>Il quadro 2026 in sintesi</h2>
<p>La Legge di Bilancio 2026 (L. 199/2025) ha confermato per tutto il 2026 le aliquote già in vigore nel 2025. Superbonus e sconto in fattura sono ormai fuori gioco per i nuovi interventi; restano tre detrazioni IRPEF ripartite in 10 rate annuali:</p>
<ul>
<li><strong>Bonus ristrutturazione</strong> (art. 16-bis TUIR): manutenzione straordinaria, restauro, risanamento conservativo, ristrutturazione edilizia.</li>
<li><strong>Ecobonus</strong>: interventi di efficientamento energetico (infissi, isolamento, generatori di calore, schermature solari).</li>
<li><strong>Sismabonus</strong>: interventi di miglioramento o adeguamento sismico, centrali in una regione come la Sicilia classificata in larga parte in zona 1 e 2.</li>
</ul>
<p>L'aliquota è del <strong>50%</strong> se l'immobile è l'abitazione principale del proprietario o del titolare di un diritto reale (usufrutto, nuda proprietà con abitazione), del <strong>36%</strong> in tutti gli altri casi (seconde case, immobili locati, detentori come inquilini o comodatari). Il limite di spesa resta di 96.000 euro per unità immobiliare, da considerare unico se più bonus si sovrappongono sullo stesso intervento.</p>

<h2>Cosa cambia dal 1° gennaio 2027</h2>
<p>Salvo nuove proroghe nella prossima manovra, dal 2027 le aliquote scendono al <strong>36%</strong> per l'abitazione principale e al <strong>30%</strong> per gli altri immobili. Conta la data del pagamento (criterio di cassa per le persone fisiche), non la data di inizio lavori: un bonifico fatto il 31 dicembre 2026 vale al 50%, quello del 2 gennaio 2027 no. Per questo, chi sta valutando un cantiere in autunno deve ragionare su un cronoprogramma che concentri i pagamenti documentabili entro l'anno, senza però pagare lavori non ancora eseguiti in modo incontrollato.</p>

<h2>I requisiti che in Sicilia fanno davvero la differenza</h2>
<p>Gli incentivi sono tecnici prima che fiscali. Le verifiche che più spesso bloccano o riducono la detrazione:</p>
<ol>
<li><strong>Stato legittimo dell'immobile</strong>: difformità non sanate (verande, chiusure, frazionamenti mai dichiarati) espongono alla decadenza del beneficio. Prima di aprire la pratica serve un confronto tra progetto assentito, catasto e stato di fatto.</li>
<li><strong>Titolo edilizio corretto</strong>: la manutenzione ordinaria sulle singole abitazioni non è agevolabile con il bonus ristrutturazione; serve la CILA o la SCIA giusta, depositata prima dell'inizio lavori.</li>
<li><strong>Asseverazioni e APE</strong> per l'ecobonus: requisiti tecnici minimi (trasmittanze, efficienze) e comunicazione ENEA entro 90 giorni dalla fine lavori.</li>
<li><strong>Classificazione sismica e asseverazione del progettista strutturale</strong> per il sismabonus, da allegare al titolo edilizio, non a lavori conclusi.</li>
<li><strong>Bonifico parlante</strong> con causale normativa, codice fiscale del beneficiario e partita IVA dell'impresa.</li>
</ol>

<h2>Abitazione principale: attenzione ai casi limite</h2>
<p>Il 50% spetta solo se l'immobile è adibito ad abitazione principale dal titolare del diritto reale. Sono frequenti in Sicilia i casi di case ereditate in comproprietà, immobili acquistati da ristrutturare prima del trasferimento di residenza e famiglie con residenze separate tra coniugi. In questi casi la quota agevolabile al 50% va verificata caso per caso, e può convenire organizzare chi paga e chi intesta le fatture prima dell'inizio lavori.</p>

<h2>Ecobonus nel clima siciliano: cosa conviene davvero</h2>
<p>Con inverni miti ed estati lunghe, in zona climatica B e C il risparmio non arriva dal cappotto più spesso possibile ma da un mix equilibrato: infissi con buon fattore solare, schermature, isolamento delle coperture piane (spesso il punto più caldo della casa) e pompe di calore correttamente dimensionate. Le caldaie a combustibili fossili non sono più incentivate. Un intervento mal progettato, per esempio un isolamento interno senza verifica igrometrica in una casa in pietra, rischia di creare condensa e muffa: la detrazione non compensa un problema strutturale.</p>

<h2>Sismabonus: perché in Sicilia è il bonus più sottovalutato</h2>
<p>Gran parte dell'isola, dalla Sicilia orientale a Messina, ricade in zone ad alta pericolosità sismica. Il sismabonus copre interventi come cerchiature di aperture, consolidamento di solai, rinforzi con fibre o intonaci armati e collegamenti tra pareti. Spesso è possibile integrare questi lavori in una ristrutturazione già prevista, portando sotto l'agevolazione opere che altrimenti si farebbero comunque. Serve però un progetto strutturale depositato al Genio Civile secondo l'iter regionale.</p>

<h2>Gli errori che fanno perdere il bonus</h2>
<ul>
<li>Iniziare i lavori prima di aver depositato il titolo edilizio.</li>
<li>Pagare con bonifico ordinario o con contanti.</li>
<li>Dimenticare la comunicazione ENEA per gli interventi che la richiedono.</li>
<li>Sommare più bonus sulla stessa spesa oltre il limite di 96.000 euro.</li>
<li>Non conservare fatture, asseverazioni e titoli edilizi per i controlli dell'Agenzia delle Entrate.</li>
</ul>
<p>Le norme fiscali cambiano spesso: prima di decidere, conviene un confronto congiunto tra tecnico e commercialista sul caso specifico.</p>
""",
        "faq": [
            ("Nel 2026 il bonus ristrutturazione è ancora al 50%?",
             "Sì, per l'abitazione principale del proprietario o del titolare di un diritto reale. Per seconde case e altri immobili l'aliquota è del 36%. Il limite di spesa è di 96.000 euro per unità immobiliare."),
            ("Cosa succede ai bonus edilizi nel 2027?",
             "La normativa vigente prevede dal 2027 il passaggio al 36% per l'abitazione principale e al 30% per gli altri immobili, salvo proroghe nella prossima Legge di Bilancio. Conta la data del pagamento."),
            ("Posso avere il bonus se la casa ha piccoli abusi?",
             "Le difformità non sanate possono far decadere la detrazione. Molte difformità parziali si possono regolarizzare con le procedure introdotte dal Salva Casa, recepite in Sicilia con la L.R. 27/2024: va verificato prima di iniziare."),
            ("Il sismabonus vale anche per le case singole?",
             "Sì, si applica a edifici residenziali e produttivi in zona sismica 1, 2 e 3, quindi a quasi tutta la Sicilia. Serve l'asseverazione del progettista strutturale allegata al titolo edilizio."),
        ],
        "related": [
            ("/sicilia/sanatoria-edilizia-in-sicilia-cosa-e-il-doppio-confirme-e-quando-serve.html", "Sanatoria edilizia in Sicilia dopo il Salva Casa"),
            ("/sicilia/cila-scia-o-permesso-di-costruire-i-tempi-reali-in-sicilia-nel-2026.html", "CILA, SCIA o permesso di costruire: tempi reali"),
            ("/sicilia/pompe-di-calore-in-zona-climatica-b-e-c-dimensionamento-per-la-sicilia.html", "Pompe di calore in zona climatica B e C"),
            ("/sicilia/rinforzo-strutturale-fibre-di-carbonio-e-intonaci-armati-per-la-sismica.html", "Rinforzo strutturale per la sismica"),
            ("/servizi/verifica-stato-legittimo-e-regolarita-urbanistica.html", "Verifica stato legittimo e regolarità urbanistica"),
        ],
    },
    # ------------------------------------------------------------------
    {
        "file": "cila-scia-o-permesso-di-costruire-i-tempi-reali-in-sicilia-nel-2026.html",
        "title": "CILA, SCIA o permesso di costruire in Sicilia: quale serve e tempi reali (2026)",
        "description": "Come scegliere tra CILA, SCIA e permesso di costruire in Sicilia secondo la L.R. 16/2016: esempi di interventi, documenti, tempi reali negli uffici e errori che bloccano il cantiere.",
        "lede": "In Sicilia il Testo Unico Edilizia si applica attraverso la L.R. 16/2016, aggiornata dopo il Salva Casa. Scegliere il titolo sbagliato non è un dettaglio formale: può bloccare il cantiere, far perdere i bonus e creare problemi al momento della vendita.",
        "service": ("/servizi/pratiche-edilizie-cila-scia-e-permessi.html", "Pratiche edilizie: CILA, SCIA e permessi"),
        "body": """
<h2>Il principio: il titolo dipende dall'intervento, non dalla fretta</h2>
<p>La scelta tra CILA, SCIA e permesso di costruire dipende da cosa si modifica: impianti e distribuzione interna, prospetti, strutture, volumi, destinazione d'uso. Una pratica più leggera depositata per lavori che ne richiedono una più pesante non è valida, e l'errore emerge di solito nel momento peggiore: un controllo in cantiere, una richiesta di integrazione, una due diligence prima del rogito.</p>

<h2>Quando basta la CILA</h2>
<p>La Comunicazione di Inizio Lavori Asseverata copre la manutenzione straordinaria leggera che non tocca strutture e prospetti. Esempi tipici:</p>
<ul>
<li>demolizione e ricostruzione di tramezzi non portanti e nuova distribuzione interna;</li>
<li>spostamento o realizzazione di un bagno, rifacimento completo degli impianti;</li>
<li>frazionamento o accorpamento di unità senza modifiche strutturali o di prospetto, nei limiti previsti;</li>
<li>sostituzione di pavimenti con rifacimento dei massetti e degli impianti sottostanti.</li>
</ul>
<p><strong>Tempi:</strong> i lavori possono iniziare subito dopo il deposito telematico allo Sportello Unico per l'Edilizia del Comune. Il tempo reale è quello di preparazione: rilievo, verifica dello stato legittimo e elaborati richiedono di norma da una a tre settimane.</p>

<h2>Quando serve la SCIA</h2>
<p>La Segnalazione Certificata di Inizio Attività serve per interventi più incisivi, tra cui:</p>
<ul>
<li>interventi su parti strutturali (aperture in muri portanti, consolidamento di solai);</li>
<li>modifiche ai prospetti, come apertura o allargamento di finestre e balconi;</li>
<li>restauro e risanamento conservativo su parti strutturali;</li>
<li>varianti in corso d'opera a permessi di costruire che non costituiscono variazioni essenziali.</li>
</ul>
<p><strong>Tempi:</strong> anche la SCIA consente in genere l'avvio immediato, ma il Comune ha 30 giorni per verificare e può vietare la prosecuzione. Se l'intervento tocca le strutture, prima dei lavori va completato l'iter al Genio Civile (deposito o autorizzazione sismica), che in alcune province richiede settimane o mesi.</p>

<h2>Quando serve il permesso di costruire</h2>
<p>Il permesso di costruire è necessario per nuove costruzioni, ampliamenti, ristrutturazioni edilizie "pesanti" che modificano volumetria, sagoma o prospetti in modo rilevante, e per molti cambi d'uso tra categorie diverse nei centri storici. In molti casi è ammessa la SCIA alternativa al permesso, con i relativi rischi e responsabilità.</p>
<p><strong>Tempi:</strong> l'iter di legge prevede un'istruttoria di 60 giorni più il termine per il provvedimento finale, ma nei Comuni siciliani più grandi i tempi reali dipendono da pareri esterni (Soprintendenza, Genio Civile, ASP, vincolo idrogeologico) e da eventuali richieste di integrazione. In zona vincolata il parere paesaggistico è spesso il collo di bottiglia.</p>

<h2>Vincoli: la variabile che cambia tutto</h2>
<p>Centri storici come Ortigia, Ibla, Cefalù o il centro di Palermo, le fasce costiere e le aree soggette a vincolo paesaggistico richiedono l'autorizzazione della Soprintendenza anche per interventi esterni minimi: colori di facciata, infissi, tettoie. Una CILA perfetta non basta se manca il nulla osta paesaggistico. Per questo la verifica dei vincoli va fatta prima ancora di scegliere il titolo.</p>

<h2>Cosa è cambiato con il Salva Casa in Sicilia</h2>
<p>La Regione ha recepito il D.L. 69/2024 con la L.R. 27/2024, in vigore dal 20 novembre 2024 e poi corretta dalla L.R. 22/2025. Per chi ristruttura le novità più utili sono le tolleranze costruttive ampliate per le opere realizzate entro il 24 maggio 2024, le procedure semplificate per sanare le difformità parziali e alcune semplificazioni sul cambio di destinazione d'uso. La Regione ha pubblicato anche nuova modulistica unificata: usare moduli vecchi è una causa frequente di integrazioni.</p>

<h2>I documenti che servono sempre</h2>
<ol>
<li>Titolo di proprietà e visura catastale aggiornata.</li>
<li>Ricostruzione dello stato legittimo (licenze, concessioni, condoni precedenti).</li>
<li>Rilievo dello stato di fatto e progetto, con tavole comparative.</li>
<li>Relazione tecnica e asseverazione del progettista.</li>
<li>Dati dell'impresa, DURC e notifica preliminare quando richiesta.</li>
<li>Eventuali pareri: Soprintendenza, Genio Civile, assenso condominiale per le parti comuni.</li>
</ol>

<h2>Errori che bloccano il cantiere</h2>
<ul>
<li>Depositare una CILA per lavori che toccano strutture o prospetti.</li>
<li>Non accorgersi di una difformità preesistente: la nuova pratica la "fotografa" e la rende evidente.</li>
<li>Dimenticare la comunicazione di fine lavori e l'aggiornamento catastale.</li>
<li>Avviare opere strutturali prima della chiusura dell'iter al Genio Civile.</li>
</ul>
""",
        "faq": [
            ("Con la CILA posso iniziare i lavori subito?",
             "Sì, dopo il deposito telematico allo Sportello Unico per l'Edilizia. Il tempo da considerare è quello di preparazione della pratica, che include rilievo e verifica dello stato legittimo."),
            ("Aprire una finestra richiede la CILA o la SCIA?",
             "Modificare un prospetto richiede di norma la SCIA. Se l'apertura interessa un muro portante serve anche il progetto strutturale con l'iter al Genio Civile, e in zona vincolata l'autorizzazione paesaggistica."),
            ("Quanto tempo serve per un permesso di costruire in Sicilia?",
             "L'iter di legge prevede circa 60 giorni di istruttoria più il termine per la decisione, ma i tempi reali dipendono dai pareri esterni richiesti e dalle integrazioni. In zona vincolata possono servire diversi mesi."),
            ("Il Salva Casa vale anche in Sicilia?",
             "Sì, la Regione lo ha recepito con la L.R. 27/2024, in vigore dal 20 novembre 2024 e modificata dalla L.R. 22/2025. Alcune disposizioni si applicano con adattamenti regionali."),
        ],
        "related": [
            ("/sicilia/sanatoria-edilizia-in-sicilia-cosa-e-il-doppio-confirme-e-quando-serve.html", "Sanatoria edilizia in Sicilia dopo il Salva Casa"),
            ("/sicilia/autorizzazione-paesaggistica-liter-semplificato-per-le-zone-vincolate.html", "Autorizzazione paesaggistica semplificata"),
            ("/sicilia/agibilita-ex-abitabilita-perche-senza-non-puoi-vendere-o-affittare.html", "Agibilità: perché senza non puoi vendere o affittare"),
            ("/guide/palermo/cila-a-palermo-quando-serve-e-cosa-cambia-in-cantiere.html", "CILA a Palermo"),
            ("/servizi/verifica-stato-legittimo-e-regolarita-urbanistica.html", "Verifica stato legittimo e regolarità urbanistica"),
        ],
    },
    # ------------------------------------------------------------------
    {
        "file": "sanatoria-edilizia-in-sicilia-cosa-e-il-doppio-confirme-e-quando-serve.html",
        "title": "Sanatoria edilizia in Sicilia dopo il Salva Casa: doppia conformità e tolleranze",
        "description": "Sanatoria edilizia in Sicilia: differenza tra art. 36 e 36-bis, doppia conformità, tolleranze costruttive fino al 6%, silenzio-assenso a 45 giorni e cosa non si può sanare.",
        "lede": "Con il Salva Casa, recepito in Sicilia dalla L.R. 27/2024, sanare una difformità è diventato più semplice in molti casi. Ma non tutto è sanabile, e una pratica impostata male può fotografare un abuso invece di risolverlo.",
        "service": ("/servizi/sanatorie-e-pratiche-in-sanatoria.html", "Sanatorie e pratiche in sanatoria"),
        "body": """
<h2>Prima di tutto: tolleranza, difformità parziale o abuso totale?</h2>
<p>La prima domanda non è "come si sana" ma "che cosa ho davanti". Le categorie hanno conseguenze molto diverse:</p>
<ul>
<li><strong>Tolleranze costruttive</strong>: piccoli scostamenti di misura che non sono abusi e si dichiarano senza sanatoria.</li>
<li><strong>Difformità parziali e variazioni essenziali</strong>: opere diverse dal titolo rilasciato, oggi sanabili con la procedura semplificata dell'art. 36-bis.</li>
<li><strong>Interventi in totale difformità o senza titolo</strong>: restano soggetti all'accertamento di conformità "classico" dell'art. 36, con la doppia conformità piena.</li>
</ul>

<h2>Le tolleranze costruttive ampliate</h2>
<p>Per gli interventi realizzati entro il 24 maggio 2024 le tolleranze su altezze, distacchi, cubatura e superfici crescono al diminuire della superficie dell'unità: dal 2% per le unità oltre 500 mq fino al 6% per quelle sotto i 60 mq, con valori intermedi per le fasce comprese. Per gli interventi successivi resta il 2%. Rientrano nelle tolleranze anche alcune irregolarità geometriche, finiture e la diversa collocazione di impianti e opere interne, purché non si violi la normativa sismica e i diritti di terzi. Il tecnico le dichiara nella prima pratica utile o in una specifica asseverazione.</p>

<h2>Art. 36-bis: la sanatoria semplificata</h2>
<p>Per le difformità parziali e le variazioni essenziali la "doppia conformità" è stata alleggerita: l'opera deve essere conforme alla disciplina urbanistica vigente al momento della domanda e ai requisiti edilizi vigenti al momento della realizzazione. In pratica, un intervento che all'epoca rispettava le regole edilizie ma non era stato autorizzato correttamente può oggi essere regolarizzato più facilmente.</p>
<p>Elementi chiave della procedura:</p>
<ul>
<li>sul Comune grava un termine di 45 giorni, decorso il quale si forma il silenzio-assenso;</li>
<li>il pagamento dell'oblazione condiziona l'efficacia del titolo in sanatoria;</li>
<li>in zona vincolata serve il parere della Soprintendenza, con termini propri;</li>
<li>il Comune può subordinare la sanatoria a interventi di adeguamento, ad esempio per la sicurezza strutturale.</li>
</ul>

<h2>Art. 36: quando resta la doppia conformità piena</h2>
<p>Per le opere realizzate senza titolo o in totale difformità resta l'accertamento di conformità tradizionale: l'opera deve essere conforme sia alla disciplina vigente al momento della realizzazione sia a quella vigente oggi. Qui il silenzio dell'amministrazione equivale a rifiuto. Non è un condono: se una delle due conformità manca, l'opera non è sanabile e va rimossa o ricondotta a conformità.</p>

<h2>Cosa non si può sanare</h2>
<p>Ampliamenti in contrasto con il piano regolatore, volumi in zona di inedificabilità assoluta, opere su aree demaniali o nelle fasce di rispetto costiere tutelate e, in generale, ciò che oggi sarebbe vietato non diventano regolari con il Salva Casa. Diffidare da chi promette di "sistemare tutto": il rischio è depositare una pratica che non verrà accolta, rendendo evidente l'abuso.</p>

<h2>Il caso siciliano: condoni pendenti e verande</h2>
<p>In Sicilia sono ancora molte le domande di condono degli anni 1985, 1994 e 2003 mai definite. Un condono pendente non equivale a un titolo: prima di una vendita o di una ristrutturazione va verificato lo stato della pratica e, se possibile, portato a conclusione. Altro tema frequente sono le verande e le chiusure di balconi: il Salva Casa ha introdotto semplificazioni per le vetrate panoramiche amovibili, ma le chiusure stabili che creano volume restano un intervento da valutare con attenzione.</p>

<h2>Come procedere, passo per passo</h2>
<ol>
<li>Accesso agli atti in Comune per recuperare tutti i titoli e le pratiche precedenti.</li>
<li>Rilievo dello stato di fatto e confronto con il progetto assentito e con il catasto.</li>
<li>Classificazione di ogni difformità: tolleranza, parziale, totale.</li>
<li>Scelta della procedura e verifica dei vincoli.</li>
<li>Deposito della pratica, pagamento di sanzioni e oblazione, aggiornamento catastale.</li>
</ol>
<p>Solo al termine del percorso l'immobile è commerciabile senza riserve e può accedere ai bonus edilizi.</p>
""",
        "faq": [
            ("Che differenza c'è tra art. 36 e art. 36-bis?",
             "L'art. 36 riguarda opere senza titolo o in totale difformità e richiede la doppia conformità piena. L'art. 36-bis, introdotto dal Salva Casa, riguarda difformità parziali e variazioni essenziali con una conformità alleggerita e silenzio-assenso dopo 45 giorni."),
            ("Le tolleranze del 6% valgono per tutte le case?",
             "No. Il 6% vale per unità sotto i 60 mq e per interventi realizzati entro il 24 maggio 2024. Per unità più grandi la percentuale scende fino al 2%, che resta il valore per gli interventi successivi."),
            ("Una veranda chiusa si può sanare in Sicilia?",
             "Dipende da volume, vincoli e piano regolatore. Le vetrate panoramiche amovibili godono di semplificazioni, ma una chiusura stabile che crea volume va valutata caso per caso e non sempre è sanabile."),
            ("Un condono pendente permette di vendere casa?",
             "Un condono non definito non equivale a un titolo rilasciato e può complicare il rogito. Conviene verificare lo stato della pratica in Comune e completarla prima della vendita."),
        ],
        "related": [
            ("/sicilia/cila-scia-o-permesso-di-costruire-i-tempi-reali-in-sicilia-nel-2026.html", "CILA, SCIA o permesso di costruire"),
            ("/sicilia/verande-e-serre-solari-bioclimatiche-come-chiudere-un-balcone-legalmente.html", "Verande e serre solari: chiudere un balcone legalmente"),
            ("/sicilia/comprare-casa-in-sicilia-la-checklist-tecnica-pre-acquisto-due-diligence.html", "Checklist tecnica prima di comprare casa"),
            ("/guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html", "Sanatoria edilizia a Palermo"),
            ("/servizi/verifica-stato-legittimo-e-regolarita-urbanistica.html", "Verifica stato legittimo e regolarità urbanistica"),
        ],
    },
    # ------------------------------------------------------------------
    {
        "file": "agibilita-ex-abitabilita-perche-senza-non-puoi-vendere-o-affittare.html",
        "title": "Agibilità (ex abitabilità) in Sicilia: cos'è la SCA e quando serve per vendere o affittare",
        "description": "Agibilità in Sicilia: cos'è la Segnalazione Certificata per l'Agibilità (SCA), quando serve, documenti, cosa fare per le case vecchie senza certificato e i requisiti dopo il Salva Casa.",
        "lede": "L'agibilità attesta che un immobile è sicuro, salubre, conforme al progetto e agli impianti a norma. Oggi non si chiede più un certificato al Comune: si presenta una Segnalazione Certificata (SCA). Mancare questo passaggio non sempre blocca la vendita, ma quasi sempre complica mutuo, affitto turistico e apertura di attività.",
        "service": ("/servizi/relazioni-tecniche-e-documentazione-di-progetto.html", "Relazioni tecniche e documentazione di progetto"),
        "body": """
<h2>Da certificato di abitabilità a SCA</h2>
<p>Fino al 2016 il Comune rilasciava il "certificato di abitabilità" o di agibilità. Oggi, secondo l'art. 24 del Testo Unico Edilizia applicato in Sicilia, l'agibilità si attesta con la <strong>Segnalazione Certificata per l'Agibilità (SCA)</strong>, presentata dal titolare del titolo edilizio tramite un tecnico entro 15 giorni dalla fine dei lavori. La mancata presentazione è punita con una sanzione amministrativa.</p>

<h2>Quando va presentata</h2>
<ul>
<li>nuove costruzioni e ricostruzioni, anche parziali;</li>
<li>sopraelevazioni e ampliamenti;</li>
<li>interventi che incidono su sicurezza, igiene, risparmio energetico o impianti, come molte ristrutturazioni con SCIA o permesso;</li>
<li>cambi di destinazione d'uso, ad esempio da negozio ad abitazione o da magazzino a casa vacanze;</li>
<li>frazionamenti che creano nuove unità.</li>
</ul>

<h2>I documenti della SCA</h2>
<ol>
<li>Attestazione del direttore dei lavori o di un tecnico sulla sussistenza delle condizioni di sicurezza, igiene, salubrità e risparmio energetico.</li>
<li>Certificato di collaudo statico o dichiarazione di regolare esecuzione per le opere strutturali.</li>
<li>Dichiarazioni di conformità degli impianti (elettrico, idrico, gas, climatizzazione).</li>
<li>Aggiornamento catastale (DOCFA) coerente con lo stato realizzato.</li>
<li>Attestato di prestazione energetica quando richiesto.</li>
<li>Dichiarazione sul superamento delle barriere architettoniche, dove prevista.</li>
</ol>

<h2>Si può vendere una casa senza agibilità?</h2>
<p>Sì, la vendita è valida: l'agibilità non è un requisito di validità del contratto. Ma la giurisprudenza considera la sua mancanza un possibile inadempimento del venditore, che può portare a riduzione del prezzo o risarcimento se non era stata dichiarata. Le banche, inoltre, la richiedono spesso per concedere il mutuo. Il problema vero, però, è quando l'agibilità manca perché l'immobile non è conforme: in quel caso la questione è urbanistica, non documentale.</p>

<h2>E per affittare?</h2>
<p>Per un affitto tradizionale l'agibilità non è sempre richiesta formalmente, ma per <strong>B&amp;B, case vacanze e locazioni turistiche</strong> in Sicilia gli uffici regionali e comunali la verificano spesso insieme al CIN e al CIR. Per negozi, studi professionali e ristoranti l'agibilità con destinazione coerente è di fatto indispensabile per aprire l'attività e ottenere i pareri ASP.</p>

<h2>Case vecchie senza alcun certificato</h2>
<p>Nei centri storici siciliani molti edifici sono anteriori al 1934 o al 1967 e non hanno mai avuto un certificato. Non significa che siano irregolari: lo stato legittimo si ricostruisce con documenti d'epoca, catasto d'impianto e riprese fotografiche. Per attestare l'agibilità oggi servono comunque requisiti attuali: impianti certificati, verifica statica e requisiti igienico-sanitari. Spesso conviene presentare la SCA al termine di una ristrutturazione già in programma.</p>

<h2>Altezze e superfici minime dopo il Salva Casa</h2>
<p>Il Salva Casa ha introdotto a livello nazionale la possibilità di attestare l'agibilità con altezza minima di 2,40 metri e con monolocali da 20 mq per una persona e 28 mq per due, a precise condizioni: interventi di recupero edilizio e di miglioramento igienico-sanitario. In Sicilia l'applicazione passa attraverso la L.R. 27/2024 e i regolamenti comunali: è un'opportunità concreta per seminterrati, catoi e piccoli appartamenti, ma va verificata caso per caso.</p>

<h2>Gli errori più comuni</h2>
<ul>
<li>Considerare l'agibilità una formalità da fare "dopo", quando l'impresa ha già chiuso il cantiere e le certificazioni impianti non si trovano.</li>
<li>Presentare la SCA con un catasto non aggiornato.</li>
<li>Confondere l'agibilità con la conformità urbanistica: la prima presuppone la seconda.</li>
</ul>
""",
        "faq": [
            ("L'agibilità è obbligatoria per vendere casa?",
             "Non è un requisito di validità della compravendita, ma la sua mancanza può essere contestata dall'acquirente e complicare il mutuo. Va dichiarata nel preliminare e possibilmente risolta prima del rogito."),
            ("Entro quando si presenta la SCA?",
             "Entro 15 giorni dalla comunicazione di fine lavori, a cura del titolare del titolo edilizio tramite un tecnico abilitato. Il ritardo comporta una sanzione amministrativa."),
            ("Serve l'agibilità per una casa vacanze in Sicilia?",
             "Per le locazioni turistiche e le strutture extralberghiere è spesso richiesta insieme ai requisiti di sicurezza per CIN e CIR. Conviene verificarla prima di pubblicare l'annuncio."),
            ("Una casa costruita prima del 1967 senza certificato è irregolare?",
             "Non necessariamente. Lo stato legittimo si può ricostruire con documenti storici e catasto d'impianto. Per l'agibilità servono però impianti e requisiti igienici attuali."),
        ],
        "related": [
            ("/sicilia/aprire-un-bandb-in-sicilia-requisiti-bagni-colazione-e-barriere-architettoniche.html", "Aprire un B&B in Sicilia: requisiti 2026"),
            ("/sicilia/trasformare-un-basso-dammusocatoio-in-abitazione-requisiti-igienico-sanitari.html", "Trasformare un catoio in abitazione"),
            ("/sicilia/comprare-casa-in-sicilia-la-checklist-tecnica-pre-acquisto-due-diligence.html", "Checklist tecnica prima di comprare casa"),
            ("/sicilia/cambio-destinazione-duso-da-negozioufficio-a-casa-vacanze.html", "Cambio d'uso da negozio a casa vacanze"),
            ("/servizi/pratiche-catastali-e-docfa.html", "Pratiche catastali e DOCFA"),
        ],
    },
    # ------------------------------------------------------------------
    {
        "file": "comprare-casa-in-sicilia-la-checklist-tecnica-pre-acquisto-due-diligence.html",
        "title": "Comprare casa in Sicilia: checklist tecnica pre-acquisto in 12 punti (due diligence)",
        "description": "Prima di firmare il preliminare: 12 verifiche tecniche per comprare casa in Sicilia. Stato legittimo, catasto, condoni pendenti, vincoli, strutture, umidità, impianti e condominio.",
        "lede": "Il prezzo si tratta in agenzia, ma il valore reale di una casa si scopre negli archivi del Comune e sul posto. In Sicilia, tra condoni mai definiti, verande non dichiarate e vincoli paesaggistici, una due diligence tecnica prima del preliminare è il modo più economico per evitare sorprese.",
        "service": ("/servizi/assistenza-tecnica-per-acquisto-immobili.html", "Assistenza tecnica per l'acquisto di immobili"),
        "body": """
<h2>Perché farla prima del preliminare</h2>
<p>Il preliminare vincola entrambe le parti e di solito prevede una caparra. Se dopo la firma emerge una difformità, il margine di trattativa è ridotto e i tempi del rogito si allungano. Inserire nel preliminare una clausola che subordina l'acquisto all'esito positivo delle verifiche tecniche tutela l'acquirente senza bloccare la trattativa.</p>

<h2>Documenti e regolarità: i primi 6 punti</h2>
<ol>
<li><strong>Titolo di provenienza</strong>: atto di acquisto, successione o donazione del venditore, con eventuali vincoli o ipoteche.</li>
<li><strong>Stato legittimo</strong>: licenza, concessione o permesso originari e tutte le pratiche successive, ottenuti con accesso agli atti in Comune.</li>
<li><strong>Conformità catastale</strong>: planimetria depositata identica allo stato reale. Dal 2010 è obbligatoria per il rogito, ma la conformità catastale non garantisce quella urbanistica.</li>
<li><strong>Condoni pendenti</strong>: in Sicilia molte domande del 1985, 1994 e 2003 non sono mai state definite. Va verificato lo stato e chi sostiene i costi per concluderle.</li>
<li><strong>Agibilità</strong>: presenza del certificato o della SCA, coerenza con la destinazione d'uso.</li>
<li><strong>Vincoli</strong>: paesaggistici, storico-artistici, idrogeologici, fasce di rispetto costiere o ferroviarie. Incidono su cosa potrai fare dopo l'acquisto.</li>
</ol>

<h2>Lo stato dell'immobile: gli altri 6 punti</h2>
<ol start="7">
<li><strong>Strutture</strong>: fessurazioni, solai deformati, ferri a vista nei frontalini dei balconi, segni di cedimento. In zona sismica sono il primo controllo da fare.</li>
<li><strong>Umidità</strong>: di risalita nei piani terra, da condensa nelle pareti nord, da infiltrazione sotto terrazzi e coperture piane.</li>
<li><strong>Coperture e impermeabilizzazioni</strong>: età e stato delle guaine, pendenze, scarichi pluviali.</li>
<li><strong>Impianti</strong>: elettrico con messa a terra e differenziale, idrico e scarichi, gas; disponibilità delle dichiarazioni di conformità.</li>
<li><strong>Presenza di amianto</strong>: coperture in eternit, canne fumarie, serbatoi idrici sui tetti, ancora molto diffusi negli edifici degli anni '60-'80.</li>
<li><strong>Condominio</strong>: lavori straordinari deliberati o in discussione, morosità, regolamento (che può vietare B&amp;B o certe attività), stato di facciate e parti comuni.</li>
</ol>

<h2>Le difformità tipiche in Sicilia</h2>
<ul>
<li>verande e chiusure di balconi non autorizzate;</li>
<li>bagni e cucine spostati senza pratica;</li>
<li>tettoie e coperture di terrazzi trasformati in vani;</li>
<li>frazionamenti mai dichiarati in Comune ma presenti al catasto, o viceversa;</li>
<li>piani terra o magazzini usati come abitazione senza cambio d'uso.</li>
</ul>
<p>Molte di queste situazioni oggi si regolarizzano con le tolleranze e le procedure del Salva Casa, recepito in Sicilia con la L.R. 27/2024. Altre no. Conoscere la differenza prima di firmare consente di negoziare il prezzo o chiedere che sia il venditore a regolarizzare.</p>

<h2>Se vuoi ristrutturare dopo l'acquisto</h2>
<p>Se il piano è comprare per ristrutturare, la due diligence dovrebbe includere anche uno studio di fattibilità: cosa si può fare (aperture, frazionamenti, cambio d'uso, ampliamenti), con quali titoli e in che tempi. Nelle aste immobiliari questo passaggio è ancora più importante, perché l'immobile si compra nello stato di fatto e di diritto in cui si trova.</p>

<h2>Come organizzare le verifiche</h2>
<p>Un sopralluogo tecnico e l'accesso agli atti in Comune sono i due passaggi essenziali. I tempi dipendono soprattutto dall'archivio comunale: in alcuni Comuni l'accesso agli atti richiede pochi giorni, in altri diverse settimane. Per questo conviene richiederlo appena si avvia la trattativa.</p>
""",
        "faq": [
            ("La conformità catastale basta per comprare in sicurezza?",
             "No. Il catasto ha finalità fiscali: una planimetria aggiornata non dimostra che le opere siano state autorizzate dal Comune. Serve verificare anche lo stato legittimo urbanistico."),
            ("Cosa fare se la casa ha una veranda non autorizzata?",
             "Valutare con un tecnico se rientra nelle tolleranze o nelle procedure di sanatoria. Se è sanabile si può chiedere al venditore di regolarizzarla prima del rogito o negoziare il prezzo; se non lo è va rimossa."),
            ("Quando conviene fare la due diligence tecnica?",
             "Prima del preliminare o subito dopo una proposta d'acquisto condizionata. Inserire nel preliminare una clausola legata all'esito delle verifiche tutela l'acquirente."),
            ("Un condono pendente è un problema per il rogito?",
             "Può esserlo. Va verificato in Comune lo stato della pratica, cosa manca per definirla e chi ne sostiene i costi, e conviene disciplinarlo nel preliminare."),
        ],
        "related": [
            ("/sicilia/sanatoria-edilizia-in-sicilia-cosa-e-il-doppio-confirme-e-quando-serve.html", "Sanatoria edilizia in Sicilia dopo il Salva Casa"),
            ("/sicilia/agibilita-ex-abitabilita-perche-senza-non-puoi-vendere-o-affittare.html", "Agibilità: cos'è la SCA e quando serve"),
            ("/sicilia/comprare-allasta-in-sicilia-rischi-occulti-e-sanatorie-necessarie.html", "Comprare all'asta in Sicilia"),
            ("/sicilia/crepe-nei-muri-quando-preoccuparsi-diagnosi-delle-fessure-strutturali.html", "Crepe nei muri: quando preoccuparsi"),
            ("/guide/palermo/due-diligence-prima-dellacquisto-a-palermo-check-tecnico-in-10-punti.html", "Due diligence prima dell'acquisto a Palermo"),
        ],
    },
    # ------------------------------------------------------------------
    {
        "file": "aprire-un-bandb-in-sicilia-requisiti-bagni-colazione-e-barriere-architettoniche.html",
        "title": "Aprire un B&B o una casa vacanze in Sicilia nel 2026: requisiti, CIN, CIR e sicurezza",
        "description": "Requisiti per aprire un B&B o una casa vacanze in Sicilia nel 2026: CIN e CIR, L.R. 6/2025, rilevatori gas e CO, estintori, agibilità, bagni, regolamento di condominio e barriere architettoniche.",
        "lede": "In Sicilia per affittare a turisti servono due codici, il CIN nazionale e il CIR regionale, oltre a requisiti di sicurezza obbligatori dal 2025. Prima ancora, però, viene l'immobile: destinazione d'uso, agibilità e impianti decidono se l'attività può partire e quanto rischia ai controlli.",
        "service": ("/servizi/adeguamenti-per-b-b-e-case-vacanza.html", "Adeguamenti per B&B e case vacanza"),
        "body": """
<h2>Locazione turistica, casa vacanze o B&amp;B?</h2>
<p>La forma giuridica determina gli obblighi tecnici. In sintesi:</p>
<ul>
<li><strong>Locazione breve/turistica</strong>: affitto dell'intero appartamento fino a 30 giorni, senza servizi aggiuntivi; resta una locazione abitativa.</li>
<li><strong>Casa o appartamento per vacanze</strong>: struttura extralberghiera, anche con più unità, con obblighi di comunicazione e requisiti minimi regionali.</li>
<li><strong>Bed &amp; breakfast</strong>: ospitalità nell'abitazione in cui si risiede, con un numero limitato di camere e la somministrazione della colazione; può essere gestito in forma non imprenditoriale o imprenditoriale.</li>
</ul>
<p>Scegliere la forma sbagliata espone a sanzioni e a contestazioni del condominio. È la prima decisione da prendere, insieme al commercialista.</p>

<h2>CIN e CIR: i due codici obbligatori</h2>
<p>Dal 1° gennaio 2025 ogni unità destinata a locazione turistica o struttura ricettiva deve avere il <strong>CIN</strong> (Codice Identificativo Nazionale), introdotto dal D.L. 145/2023 e rilasciato tramite la banca dati nazionale del Ministero del Turismo. In Sicilia la L.R. 6/2025 conferma l'obbligo di affiancare il <strong>CIR</strong> regionale. Entrambi vanno esposti all'esterno dell'immobile e indicati in ogni annuncio online. Gli annunci senza codice possono essere sanzionati e rimossi dai portali.</p>

<h2>Requisiti di sicurezza obbligatori</h2>
<p>Per ottenere il CIN il titolare autocertifica la presenza di:</p>
<ul>
<li><strong>rilevatori di gas combustibile e di monossido di carbonio</strong> funzionanti, conformi alle norme tecniche, dove ci sono apparecchi a gas o a combustione;</li>
<li><strong>estintori portatili</strong> con capacità estinguente minima 13A e carica di almeno 6 kg o 6 litri, almeno uno per piano e uno ogni 200 mq, in posizione accessibile;</li>
<li>impianti conformi, con dichiarazioni di conformità disponibili per i controlli.</li>
</ul>
<p>Per le strutture imprenditoriali sopra determinate soglie si applicano anche le norme di prevenzione incendi dei Vigili del Fuoco.</p>

<h2>Requisiti dell'immobile</h2>
<ol>
<li><strong>Destinazione d'uso coerente</strong>: un magazzino o un negozio non può diventare casa vacanze senza cambio d'uso e relativa pratica.</li>
<li><strong>Agibilità</strong>: spesso verificata dagli uffici insieme alle comunicazioni turistiche.</li>
<li><strong>Requisiti igienico-sanitari</strong>: superfici minime delle camere, aerazione e illuminazione naturale, altezze interne.</li>
<li><strong>Bagni</strong>: il numero minimo dipende da camere e posti letto; molti progetti richiedono un bagno per camera per stare sul mercato, anche oltre il minimo di legge.</li>
<li><strong>Colazione</strong>: nel B&amp;B non imprenditoriale si somministrano prodotti confezionati o preparati in cucina domestica, nel rispetto delle norme igieniche; per un servizio più strutturato servono requisiti ASP.</li>
</ol>

<h2>Barriere architettoniche</h2>
<p>Per le strutture ricettive la normativa sull'accessibilità prevede, a seconda della tipologia e delle dimensioni, una quota di camere e servizi accessibili o adattabili. Anche quando non è obbligatoria, una camera accessibile amplia il mercato e va progettata fin dall'inizio: rifarla dopo costa molto di più.</p>

<h2>Condominio e centri storici</h2>
<p>Il regolamento condominiale di natura contrattuale può vietare l'uso turistico delle unità: va letto prima di comprare o investire. Nei centri storici come Ortigia, Cefalù, Taormina o il centro di Palermo, interventi su facciate, infissi e insegne richiedono spesso l'autorizzazione della Soprintendenza.</p>

<h2>Il percorso consigliato</h2>
<ol>
<li>Verifica di stato legittimo, destinazione d'uso, agibilità e regolamento condominiale.</li>
<li>Progetto di adeguamento: bagni, impianti, sicurezza, eventuale accessibilità.</li>
<li>Pratica edilizia corretta (CILA, SCIA o cambio d'uso) e lavori.</li>
<li>Certificazioni impianti, SCA e aggiornamento catastale.</li>
<li>Comunicazioni al Comune e alla Regione, richiesta di CIR e CIN.</li>
</ol>
""",
        "faq": [
            ("Serve il CIN anche per affittare una sola casa ai turisti?",
             "Sì. Dal 1° gennaio 2025 il CIN è obbligatorio per ogni unità destinata a locazione breve o turistica, oltre che per le strutture ricettive. In Sicilia va affiancato al CIR regionale."),
            ("Quali estintori servono per un affitto breve?",
             "Estintori portatili con capacità minima 13A e carica minima di 6 kg o 6 litri, almeno uno per piano e uno ogni 200 mq, oltre a rilevatori di gas e monossido di carbonio funzionanti."),
            ("Posso trasformare un magazzino in casa vacanze?",
             "Solo con un cambio di destinazione d'uso conforme al piano regolatore e il rispetto dei requisiti igienico-sanitari. Il Salva Casa ha introdotto alcune semplificazioni, da verificare nel Comune specifico."),
            ("Il condominio può vietare il B&B?",
             "Sì, se il regolamento ha natura contrattuale e contiene un divieto esplicito di destinazioni come quella turistico-ricettiva. Va verificato prima di investire."),
        ],
        "related": [
            ("/sicilia/agibilita-ex-abitabilita-perche-senza-non-puoi-vendere-o-affittare.html", "Agibilità: cos'è la SCA e quando serve"),
            ("/sicilia/cambio-destinazione-duso-da-negozioufficio-a-casa-vacanze.html", "Cambio d'uso da negozio a casa vacanze"),
            ("/sicilia/design-per-boutique-hotel-standard-minimi-per-una-clientela-luxury.html", "Design per boutique hotel"),
            ("/guide/palermo/pratica-edilizia-per-b-b-a-palermo-cosa-serve-davvero.html", "Pratica edilizia per B&B a Palermo"),
            ("/servizi/accessibilita-e-rimozione-barriere-architettoniche.html", "Accessibilità e barriere architettoniche"),
        ],
    },
]


def esc(s):
    return html.escape(s, quote=True)


def wa_link(title):
    text = f'Ciao, sto leggendo: "{title}". Vorrei capire se Studio 4e può seguire il mio caso in Sicilia.'
    return "https://wa.me/393299736697?text=" + urllib.parse.quote(text)


def build_article(a):
    url_path = f"/sicilia/{a['file']}"
    t = esc(a["title"])
    faq_html = "".join(
        f"<h3>{esc(q)}</h3><p>{esc(ans)}</p>" for q, ans in a["faq"]
    )
    related = "".join(f'<li><a href="{href}">{esc(label)}</a></li>' for href, label in a["related"])
    svc_href, svc_label = a["service"]
    return (
        '<article class="article">'
        f'<div class="breadcrumb"><a href="/">Home</a>›<a href="/sicilia/">Sicilia</a>›<span>{t}</span></div>'
        f"<h1>{t}</h1>"
        '<p class="byline" style="font-size:13px; color:#888; margin-top:6px; margin-bottom:0">A cura di '
        '<a href="/studio-4e/chi-e-studio-4e.html" style="color:#7a1d52">Arch. Fabio Costanzo</a>, Studio 4e · '
        f"Aggiornato: {UPDATED_LABEL}</p>"
        '<div class="phone-cta" style="margin:14px 0; padding:12px; background:rgba(122,29,82,0.08); border-left:4px solid #7a1d52; border-radius:12px">'
        f'<p style="margin:0; font-size:14px; font-weight:600">Hai un caso urgente. <a href="tel:{PHONE}" style="color:#7a1d52; font-weight:700">Chiama ora: +39 329 973 6697</a></p></div>'
        f'<p class="lede">{esc(a["lede"])}</p>'
        '<div style="margin-top:14px"><a class="btn" href="/inizia-da-qui/">Inizia da qui</a>'
        f'<a class="btn secondary" href="{esc(wa_link(a["title"]))}" style="margin-left:10px">WhatsApp</a></div>'
        f"{a['body'].strip()}"
        f'<section class="faq"><h2>Domande frequenti</h2>{faq_html}</section>'
        '<div class="notice cta-urgent"><strong>Hai un progetto in Sicilia?</strong>'
        "<p>Studio 4e segue pratiche edilizie, ristrutturazioni e sanatorie in tutta la Sicilia. "
        "<strong>Prima consulenza telefonica gratuita</strong> per valutare il tuo caso.</p>"
        f'<p style="margin-top:12px"><a class="btn" href="tel:{PHONE}" style="font-size:16px">Chiama: +39 329 973 6697</a>'
        '<a class="btn secondary" href="https://wa.me/393299736697?text=Ciao%2C%20vorrei%20una%20consulenza." style="margin-left:10px">WhatsApp</a></p></div>'
        '<div class="related-service" style="margin-top:24px; padding:16px; background:#f9f6f8; border-radius:12px; border-left:4px solid #7a1d52">'
        f'<strong>Servizio correlato:</strong> <a href="{svc_href}" style="color:#7a1d52">{esc(svc_label)}</a></div>'
        f'<section id="related-links"><h2>Approfondimenti correlati</h2><ul>{related}</ul></section>'
        "</article>"
    ), url_path


def build_schemas(a, url):
    blog = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": a["title"],
        "description": a["description"],
        "url": url,
        "mainEntityOfPage": url,
        "inLanguage": "it",
        "datePublished": "2025-01-15",
        "dateModified": TODAY,
        "image": f"{SITE}/assets/images/og.jpg",
        "author": {"@type": "Person", "name": "Fabio Costanzo", "jobTitle": "Architetto",
                   "url": f"{SITE}/studio-4e/chi-e-studio-4e.html"},
        "publisher": {"@type": "Organization", "name": "Architetti Sicilia", "url": f"{SITE}/"},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
            for q, ans in a["faq"]
        ],
    }
    return "".join(
        f'<script data-architetti-sicilia="1" data-rewrite="1" type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
        for s in (blog, faq)
    )


def set_meta(content, attr, name, value):
    pattern = re.compile(rf"""<meta content=(?:"[^"]*"|'[^']*') {attr}="{re.escape(name)}"/>""")
    new = f'<meta content="{esc(value)}" {attr}="{name}"/>'
    content, n = pattern.subn(lambda _: new, content)
    if n == 0:
        raise SystemExit(f"meta {attr}={name} non trovato")
    return content


def process(a):
    path = ROOT / "sicilia" / a["file"]
    content = path.read_text(encoding="utf-8")
    article, url_path = build_article(a)
    url = SITE + url_path

    content, n = re.subn(r'<article class="article">.*?</article>', lambda _: article, content, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"{a['file']}: <article> non trovato")

    content = re.sub(r"<title>.*?</title>", lambda _: f"<title>{esc(a['title'])}</title>", content, count=1, flags=re.S)
    content = set_meta(content, "name", "description", a["description"])
    content = set_meta(content, "property", "og:title", a["title"])
    content = set_meta(content, "property", "og:description", a["description"])
    content = set_meta(content, "name", "twitter:title", a["title"])
    content = set_meta(content, "name", "twitter:description", a["description"])

    # Breadcrumb JSON-LD: aggiorna il nome dell'ultima voce
    def fix_breadcrumb(m):
        data = json.loads(m.group(2))
        if data.get("@type") == "BreadcrumbList":
            data["itemListElement"][-1]["name"] = a["title"]
            return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)
        return m.group(0)
    content = re.sub(r'(<script data-architetti-sicilia="1" type="application/ld\+json">)(.*?)(</script>)',
                     fix_breadcrumb, content, flags=re.S)

    # Schema idempotente: rimuove eventuali versioni precedenti di questo script
    content = re.sub(r'<script data-architetti-sicilia="1" data-rewrite="1" type="application/ld\+json">.*?</script>',
                     "", content, flags=re.S)
    content = content.replace("</head>", build_schemas(a, url) + "</head>", 1)

    path.write_text(content, encoding="utf-8")
    return url


def update_sitemap(urls):
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    for url in urls:
        text, n = re.subn(
            rf"(<loc>{re.escape(url)}</loc>(?:(?!</url>).)*?<lastmod>)[^<]*(</lastmod>)",
            rf"\g<1>{TODAY}\g<2>", text, flags=re.S)
        if n == 0:
            print(f"  attenzione: {url} non in sitemap.xml")
    sm.write_text(text, encoding="utf-8")


def update_index():
    idx = ROOT / "sicilia" / "index.html"
    text = idx.read_text(encoding="utf-8")
    for a in ARTICLES:
        href = f"/sicilia/{a['file']}"
        text = re.sub(rf'(<a href="{re.escape(href)}">)[^<]*(</a>)',
                      lambda m: m.group(1) + html.escape(a["title"], quote=False) + m.group(2), text)
    idx.write_text(text, encoding="utf-8")


def main():
    urls = []
    for a in ARTICLES:
        url = process(a)
        urls.append(url)
        print(f"OK  {a['file']}")
    update_sitemap(urls)
    update_index()
    print(f"\n{len(urls)} articoli riscritti, sitemap aggiornata.")


if __name__ == "__main__":
    main()
