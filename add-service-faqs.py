#!/usr/bin/env python3
"""
add-service-faqs.py
Aggiunge sezione FAQ (HTML + FAQPage JSON-LD) alle 8 pagine servizio prioritarie.
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVIZI_DIR = os.path.join(BASE_DIR, "servizi")

# FAQ per ogni servizio: lista di (domanda, risposta)
SERVICE_FAQS = {
    "pratiche-edilizie-cila-scia-e-permessi": [
        (
            "Qual è la differenza tra CILA, SCIA e Permesso di Costruire?",
            "La CILA (Comunicazione di Inizio Lavori Asseverata) riguarda interventi di manutenzione straordinaria senza strutture portanti. La SCIA (Segnalazione Certificata di Inizio Attività) si usa per interventi più significativi come ristrutturazioni con modifiche distributive o cambio destinazione d'uso. Il Permesso di Costruire è obbligatorio per nuove costruzioni, demolizioni con ricostruzione e interventi su immobili vincolati. La scelta dipende dalla natura dell'intervento e va verificata caso per caso con un tecnico abilitato."
        ),
        (
            "Quando serve un architetto per la pratica edilizia?",
            "Un architetto abilitato è necessario per asseverare CILA e SCIA, progettare interventi soggetti a permesso di costruire e gestire pratiche in zone vincolate (vincolo paesaggistico, zone A, immobili tutelati dalla Soprintendenza). In molti comuni siciliani il tecnico di riferimento deve essere iscritto all'albo della provincia di intervento. Studio 4e opera in tutte e 9 le province siciliane."
        ),
        (
            "Quanto costa una pratica CILA o SCIA in Sicilia?",
            "Il costo varia in base alla complessità dell'intervento. Una CILA semplice per lavori interni in un appartamento parte generalmente da 800–1.500 €. Una SCIA per ristrutturazione con variazioni distributive si attesta tra 1.500 e 3.500 €. A questi importi si aggiungono i diritti comunali, i costi di eventuali rilievi e le spese tecniche accessorie. Il preventivo definitivo richiede la valutazione del caso specifico."
        ),
    ],
    "sanatorie-e-pratiche-in-sanatoria": [
        (
            "Cosa si può sanare con una sanatoria edilizia in Sicilia?",
            "Si possono regolarizzare gli interventi che rispettano le norme urbanistiche ed edilizie vigenti al momento della sanatoria (doppia conformità) o, in regime di condono, quelli realizzati entro le date previste dai condoni edilizi (1985, 1994, 2003). In Sicilia opera la Legge Regionale n. 37/1985 per alcune fattispecie specifiche. Non sono sanabili gli abusi in zone soggette a vincoli assoluti (es. demanio marittimo, vincolo idrogeologico)."
        ),
        (
            "Qual è il costo di una pratica in sanatoria?",
            "Il costo comprende: oneri concessori dovuti al Comune (calcolati in base alla volumetria e alla destinazione d'uso), oblazione per il condono (se applicabile), parcella del tecnico per la progettazione e la documentazione, e aggiornamento catastale se necessario. Per un appartamento con variazioni minori i costi tecnici partono da circa 1.500–2.500 €, esclusi oneri comunali che possono variare significativamente."
        ),
        (
            "Quali abusi edilizi non si possono sanare?",
            "Non sono sanabili: interventi in contrasto con gli strumenti urbanistici vigenti (es. costruzioni in zone agricole non consentite), abusi in aree soggette a vincolo paesaggistico senza autorizzazione della Soprintendenza, ampliamenti oltre i limiti volumetrici, e costruzioni in aree a rischio idrogeologico o nelle fasce di rispetto del demanio marittimo. La verifica della sanabilità richiede un'analisi tecnica preliminare."
        ),
    ],
    "ristrutturazione-completa-di-appartamenti": [
        (
            "Quanto costa ristrutturare un appartamento in Sicilia?",
            "I costi variano molto in base allo stato dell'immobile e al livello qualitativo scelto. Per una ristrutturazione completa (impianti, pavimenti, bagni, cucina, infissi, pareti) in Sicilia si lavora generalmente tra 800 e 1.400 €/mq per un livello medio-alto. Gli appartamenti storici con lavori strutturali o finiture pregiate possono superare i 1.500–2.000 €/mq. Il preventivo accurato si ottiene solo dopo rilievo e computo metrico dettagliato."
        ),
        (
            "Quanto dura una ristrutturazione completa di un appartamento?",
            "Per un appartamento di 80–120 mq si lavora solitamente in 3–5 mesi di cantiere effettivo, a cui aggiungere 4–8 settimane per progettazione, autorizzazioni e gara imprese. I tempi si allungano in presenza di vincoli (zone storiche, Soprintendenza), problemi strutturali imprevisti o ritardi nelle forniture. Una direzione lavori attiva riduce significativamente il rischio di cantieri infiniti."
        ),
        (
            "Quali documenti servono per ristrutturare un appartamento?",
            "È necessario disporre di: titolo di proprietà o disponibilità dell'immobile, planimetria catastale aggiornata, titoli edilizi pregressi (se esistono), regolamento condominiale (per verificare limitazioni), e – in base all'intervento – presentare CILA o SCIA al Comune. In zone vincolate serve anche l'autorizzazione paesaggistica. Studio 4e gestisce tutta la documentazione tecnica e amministrativa."
        ),
    ],
    "verifica-stato-legittimo-e-regolarita-urbanistica": [
        (
            "Cos'è la verifica dello stato legittimo di un immobile?",
            "La verifica dello stato legittimo (introdotta dal D.L. 76/2020 e confermata dal Testo Unico Edilizia) accerta che l'immobile sia stato costruito e trasformato nel rispetto delle autorizzazioni edilizie. Richiede la ricerca dei titoli abilitativi originali (permesso di costruire, condoni, SCIA/DIA pregresse), il confronto con la planimetria catastale e lo stato di fatto, e l'identificazione di eventuali difformità."
        ),
        (
            "Quando è obbligatoria la verifica dello stato legittimo?",
            "È obbligatoria prima di qualsiasi compravendita (per il notaio), per presentare nuove pratiche edilizie sull'immobile, per accedere ai bonus fiscali (Superbonus, bonus ristrutturazioni) e prima di eseguire lavori significativi. È fortemente consigliata anche in fase di due diligence pre-acquisto per evitare sorprese post-rogito."
        ),
        (
            "Quanto costa la verifica dello stato legittimo?",
            "Il costo dipende dalla complessità dell'immobile, dall'epoca di costruzione e dalla disponibilità degli archivi comunali. Per un appartamento in condominio si parte da circa 500–1.200 €. Per unità immobiliari più complesse, immobili storici o con pratiche pluristratificate (condoni, varianti successive) il costo sale. Il preventivo viene definito dopo una prima analisi della documentazione disponibile."
        ),
    ],
    "assistenza-tecnica-per-acquisto-immobili": [
        (
            "Cosa controlla un architetto prima dell'acquisto di un immobile?",
            "Un tecnico esperto verifica: la conformità urbanistica e catastale (stato legittimo), la presenza di vincoli (paesaggistici, storici, idrogeologici, demanio marittimo), l'agibilità/abitabilità, lo stato delle strutture e degli impianti, eventuali difformità tra progetto e stato di fatto, e la coerenza tra prezzo e interventi necessari. È un check tecnico in 10 punti che previene costose sorprese post-rogito."
        ),
        (
            "Quando conviene coinvolgere un tecnico prima di comprare casa?",
            "Sempre, ma in particolare: per immobili storici o da ristrutturare, per acquisti in zone vincolate (centro storico, costa, parchi), per immobili con condoni o varianti pregresse, e per acquisti da parte di stranieri non familiari con la normativa italiana. Studio 4e opera anche per clienti esteri che acquistano in Sicilia e offre reportistica in italiano e inglese."
        ),
        (
            "Quanto costa l'assistenza tecnica per l'acquisto di un immobile?",
            "Il servizio di due diligence tecnica pre-acquisto parte da circa 800–1.500 € per un'unità residenziale standard, inclusi sopralluogo e relazione scritta. Per immobili più complessi (ville, masserie, immobili storici, complessi con più unità) il costo viene definito su preventivo. È un investimento che può evitare spese di regolarizzazione di gran lunga superiori."
        ),
    ],
    "direzione-lavori-e-controllo-qualita": [
        (
            "Cosa fa concretamente il Direttore dei Lavori?",
            "Il Direttore dei Lavori (DL) è il tecnico incaricato di verificare che l'esecuzione corrisponda al progetto approvato, controllare la qualità dei materiali e delle lavorazioni, registrare le difformità e concordare le varianti con il committente, gestire la contabilità lavori e certificare gli stati di avanzamento, e redigere il collaudo finale con il certificato di regolare esecuzione. Rappresenta gli interessi del committente in cantiere."
        ),
        (
            "La direzione lavori è obbligatoria?",
            "È obbligatoria per tutti gli interventi che richiedono SCIA o Permesso di Costruire, e per quelli soggetti a normativa sismica (praticamente tutta la Sicilia è in zona sismica 2 o 3). Per lavori in CILA non è sempre formalmente obbligatoria ma è fortemente consigliata per tutelarne la qualità e gestire eventuali varianti in corso d'opera."
        ),
        (
            "Quanto costa la direzione lavori in Sicilia?",
            "Il compenso del DL varia tra il 3% e l'8% dell'importo lavori, a seconda della complessità dell'intervento e del livello di presidio richiesto. Per una ristrutturazione da 100.000 € si lavora orientativamente tra 3.000 e 8.000 €. Studio 4e definisce il compenso nella lettera d'incarico in modo trasparente, prima dell'avvio del cantiere."
        ),
    ],
    "progetto-di-interni-cucina-bagno-living": [
        (
            "Quanto costa un progetto di interni in Sicilia?",
            "Il costo del progetto di interni dipende dall'ampiezza degli ambienti e dal livello di dettaglio richiesto. Per cucina e bagno di un appartamento standard (progetto esecutivo con layout, prospetti, scelta materiali, coordinamento forniture) si lavora tra 1.200 e 2.500 €. Per un progetto integrato di più ambienti o per abitazioni di pregio i costi salgono proporzionalmente alla complessità e ai materiali selezionati."
        ),
        (
            "Quanto tempo richiede un progetto di interni completo?",
            "Un progetto di interni completo (cucina, bagno, living) richiede in genere 4–8 settimane dalla raccolta degli input fino alla consegna degli elaborati esecutivi, compresi i tavoli di selezione materiali e le eventuali revisioni. I tempi si adattano alla disponibilità del cliente e alla complessità dell'intervento."
        ),
        (
            "Cosa comprende un progetto bagno o cucina?",
            "Un progetto esecutivo di bagno comprende: layout planimetrico con quote, schema impianto idraulico e scarichi, sezioni con altezze e pendenze, scelta e specifiche delle piastrelle e dei sanitari, dettagli di posa, e coordinamento con idraulico e piastrellista. Per la cucina si aggiungono la planimetria ergonomica con quote di lavoro, il collegamento ai punti impianto e le indicazioni per i fornitori di arredamento."
        ),
    ],
    "efficientamento-energetico-e-comfort-abitativo": [
        (
            "Quali incentivi esistono nel 2026 per l'efficientamento energetico?",
            "Nel 2026 il Superbonus al 110% non è più disponibile nelle forme precedenti. Restano attivi: il Bonus Ristrutturazioni (50% per IRPEF, limite 96.000 €/unità) per lavori su prime case, l'Ecobonus (50–65%) per specifici interventi di risparmio energetico (coibentazione, serramenti, caldaie a condensazione, pompe di calore), e il Sismabonus per interventi antisismici. Le detrazioni sono soggette a revisioni annuali: è importante verificare la normativa vigente con il tecnico prima di avviare i lavori."
        ),
        (
            "Quanto costa un cappotto termico in Sicilia?",
            "Il costo di un cappotto termico esterno (ETICS) varia in base allo spessore dell'isolante, al tipo di finitura e alle difficoltà di cantiere. Per un edificio residenziale standard si lavora orientativamente tra 80 e 160 €/mq installato (materiale + posa). Per edifici con balconi, cornicioni, o in zone con vincoli estetici i costi aumentano. Il cappotto richiede in genere CILA o SCIA e può necessitare di autorizzazione paesaggistica in zone vincolate."
        ),
        (
            "Quali interventi migliorano di più la classe energetica in Sicilia?",
            "In Sicilia, dove il fabbisogno estivo (raffrescamento) è spesso prioritario rispetto a quello invernale, gli interventi più efficaci sono: isolamento dell'involucro (cappotto + solaio di copertura), sostituzione degli infissi con vetri basso emissivi, installazione di schermature solari esterne, e sistemi di ventilazione meccanica controllata. Le pompe di calore in sostituzione delle caldaie a gas completano un pacchetto di efficientamento integrato."
        ),
    ],
}


def build_faq_html(faqs):
    """Costruisce il blocco HTML con i <details> per le FAQ."""
    items = []
    for question, answer in faqs:
        items.append(
            f'<details style="margin-top:10px; border:1px solid #e8e0e8; border-radius:8px; padding:12px 16px">\n'
            f'    <summary style="cursor:pointer; font-weight:600; color:#3d1f36">{question}</summary>\n'
            f'    <p style="margin-top:10px; margin-bottom:0">{answer}</p>\n'
            f'  </details>'
        )
    items_html = "\n  ".join(items)
    return (
        '<section style="margin-top:32px">\n'
        '<h2>Domande frequenti</h2>\n'
        f'  {items_html}\n'
        '</section>'
    )


def build_faq_schema(faqs):
    """Costruisce il JSON-LD FAQPage schema."""
    entities = []
    for question, answer in faqs:
        entities.append({
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n</script>'


def update_service_file(filepath, service_slug):
    """Aggiunge FAQ HTML e FAQPage schema al file servizio."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    faqs = SERVICE_FAQS.get(service_slug)
    if not faqs:
        print(f"  SKIP (no FAQs defined): {service_slug}")
        return False

    # Controlla se le FAQ sono già presenti
    if 'Domande frequenti' in content:
        print(f"  SKIP (FAQs already present): {service_slug}")
        return False

    faq_html = build_faq_html(faqs)
    faq_schema = build_faq_schema(faqs)

    # Inserisci FAQ HTML prima della sezione related-guides
    insert_marker = '<section class="related-guides"'
    if insert_marker in content:
        new_content = content.replace(
            insert_marker,
            faq_html + '\n' + insert_marker,
            1
        )
    else:
        # Fallback: inserisci prima di </article>
        new_content = content.replace(
            '</article>',
            faq_html + '\n</article>',
            1
        )

    # Inserisci FAQPage schema nell'<head>, prima del </head>
    new_content = new_content.replace(
        '</head>',
        faq_schema + '\n</head>',
        1
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  UPDATED: {service_slug}")
    return True


def main():
    updated = 0
    for service_slug in sorted(SERVICE_FAQS.keys()):
        filepath = os.path.join(SERVIZI_DIR, service_slug + ".html")
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            continue
        print(f"Processing: {service_slug}")
        result = update_service_file(filepath, service_slug)
        if result:
            updated += 1

    print(f"\nDone: {updated} files updated")


if __name__ == "__main__":
    main()
