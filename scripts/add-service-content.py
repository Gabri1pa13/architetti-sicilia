#!/usr/bin/env python3
"""
Adds unique "Come funziona nel dettaglio" content sections to top 5 service pages.
Inserts between the "Output e decisioni" paragraph and the first .notice div.
"""
import os
import re

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'servizi')

ANCHOR = 'L\u2019obiettivo \u00e8 arrivare a decisioni verificabili: cosa si fa, come si fa, in che tempi e con quali controlli.</p>'
ANCHOR_ALT = 'Un output ben definito permette di confrontare preventivi in modo serio e di ridurre le varianti.</p>'

CONTENT = {
    'pratiche-edilizie-cila-scia-e-permessi.html': '''<h2>Come si imposta una pratica edilizia in Sicilia</h2><p>La prima decisione \u00e8 classificare correttamente l\u2019intervento. Usare la CILA quando serve la SCIA, o viceversa, espone a sospensione dei lavori e sanzioni. Studio 4e parte sempre da una lettura dei titoli edilizi esistenti, confrontati con lo stato attuale dell\u2019immobile: solo cos\u00ec si pu\u00f2 escludere che ci siano abusi pregressi che renderebbero la nuova pratica impugnabile.</p><p>Il portale telematico SUE (Sportello Unico Edilizia) \u00e8 attivo in tutti i comuni siciliani, ma le procedure locali variano: Palermo, Catania e Messina hanno iter consolidati; comuni minori possono avere tempistiche pi\u00f9 lunghe o richieste documentali aggiuntive legate ai loro PRG specifici.</p><p>Per immobili in centro storico o in zona paesaggisticamente vincolata (fascia costiera, riserve naturali, zone UNESCO come il centro storico di Palermo o la Val di Noto) anche una CILA pu\u00f2 richiedere un parere preventivo della Soprintendenza BB.CC. \u2014 un passaggio che allunga i tempi di 30\u201360 giorni se non anticipato.</p><h3>I tre errori che bloccano le pratiche edilizie</h3><ul><li><strong>Planimetria catastale non aggiornata:</strong> il catasto deve riflettere lo stato ante-intervento. Se c\u2019\u00e8 una difformit\u00e0 preesistente non sanata, la pratica viene respinta.</li><li><strong>Assenza del direttore dei lavori:</strong> obbligatorio per legge dalla fase di deposito. Studio 4e copre il ruolo di DL per tutti i progetti seguiti.</li><li><strong>Pratica di fine lavori non depositata:</strong> la CILA o SCIA aperta blocca il rogito. Il deposito della chiusura \u00e8 responsabilit\u00e0 del tecnico, non dell\u2019impresa.</li></ul>''',

    'sanatorie-e-pratiche-in-sanatoria.html': '''<h2>Come funziona una sanatoria edilizia in Sicilia</h2><p>La sanatoria edilizia (detta anche \u201caccertamento di conformit\u00e0\u201d) si distingue nettamente dal condono edilizio: il condono era un\u2019amnistia temporanea per abusi storici, l\u2019ultima in Italia risale al 2003. La sanatoria ordinaria invece \u00e8 uno strumento strutturale: regolarizza abusi formali, cio\u00e8 lavori eseguiti senza titolo ma che sarebbero stati autorizzabili se il titolo fosse stato richiesto.</p><p>In Sicilia la Legge Regionale 37/85 ha introdotto disposizioni specifiche rispetto al DPR 380/01 nazionale. Alcuni comuni siciliani hanno anche piani di recupero dei centri storici che influenzano la sanabilit\u00e0 degli interventi. La verifica della doppia conformit\u00e0 \u2014 conformit\u00e0 al PRG vigente e a quello in vigore al momento dell\u2019abuso \u2014 \u00e8 il passaggio critico.</p><p>Cosa non \u00e8 sanabile: costruzioni in fasce di rispetto (costiera, fluviale, stradale), in zone agricole E1, su aree vincolate dal Codice dei Beni Culturali senza autorizzazione, o interventi su immobili che gi\u00e0 scontavano abusi strutturali non sanati. Acquistare un immobile con un abuso non sanabile significa acquistare un problema che non ha soluzione tecnica.</p><h3>Il processo di verifica preliminare</h3><p>Studio 4e effettua una verifica preliminare gratuita (15\u201320 minuti al telefono) per identificare se l\u2019abuso \u00e8 sanabile, stimare l\u2019oblazione e valutare i rischi dell\u2019operazione. Solo dopo questa verifica viene proposto un incarico formale. Documenti utili da preparare: planimetria catastale, eventuale titolo edilizio originario, foto dello stato di fatto.</p>''',

    'ristrutturazione-completa-di-appartamenti.html': '''<h2>Le fasi di una ristrutturazione completa in appartamento</h2><p>Una ristrutturazione completa comprende tipicamente: demolizioni e smaltimento, impianti (elettrico, idrico, gas, VMC se previsto), strutture leggere (tramezzi, contropareti), finiture (pavimenti, rivestimenti bagni, porte), serramenti, opere di falegnameria su misura, tinteggiatura. L\u2019ordine delle lavorazioni \u00e8 critico: invertire sequenze causa rilavorazioni costose.</p><p>Il rilievo architettonico iniziale \u00e8 il documento base del progetto. Un rilievo impreciso di 5 cm su una cucina da 3 metri compromette l\u2019inserimento degli arredi. Studio 4e esegue il rilievo prima di qualsiasi scelta progettuale.</p><p>Per appartamenti in condominio \u00e8 necessario verificare il regolamento condominiale prima di intervenire su impianti centralizzati, facciate o solette. In molti condomini palermitani degli anni \u201960\u201380 i soffitti sono bassi (2,65\u20132,70 m) e l\u2019inserimento di controsoffitti o pavimenti sopraelevati richiede un\u2019analisi accurata delle quote finali.</p><h3>Perch\u00e9 il capitolato \u00e8 fondamentale</h3><p>Un preventivo senza capitolato \u00e8 inutilizzabile per confrontare imprese. Il capitolato definisce marca, modello, finitura e posa di ogni materiale. Senza di esso ogni impresa include voci diverse e non confrontabili. Studio 4e produce capitolati tecnici che eliminano ambiguit\u00e0 e riducono le contestazioni in cantiere del 70%.</p>''',

    'verifica-stato-legittimo-e-regolarita-urbanistica.html': '''<h2>Cos\u2019\u00e8 la verifica dello stato legittimo e perch\u00e9 \u00e8 obbligatoria</h2><p>Dal Decreto Semplificazioni 2020 (art. 9-bis DPR 380/01), lo stato legittimo di un immobile si identifica attraverso il titolo edilizio originario, tutti i titoli successivi, eventuali condoni o sanatorie, e la conformit\u00e0 catastale. L\u2019obbligo riguarda qualsiasi atto di trasferimento, ma anche l\u2019avvio di nuovi lavori: non si pu\u00f2 depositare una CILA su un immobile con abusi non dichiarati.</p><p>In Sicilia la ricerca archivistica pu\u00f2 essere complessa: comuni con archivi non digitalizzati, titoli edilizi anteriori agli anni \u201970 non sempre reperibili, condoni del 1985 e 1994 spesso parzialmente evasi. Studio 4e ha esperienza diretta con gli archivi comunali delle 9 province e sa dove cercare anche quando la documentazione non \u00e8 facilmente accessibile.</p><p>Il risultato della verifica \u00e8 una relazione tecnica asseverata che certifica lo stato legittimo, elenca eventuali difformit\u00e0 e le classifica come sanabili o non sanabili. Questo documento \u00e8 quello che il notaio richiede al momento del rogito e che le banche esigono per l\u2019istruttoria mutuo.</p><h3>Quando serve una verifica stato legittimo</h3><ul><li><strong>Prima di comprare:</strong> verificare che non ci siano abusi nascosti che bloccano il rogito o che trasferiscono problemi al nuovo proprietario.</li><li><strong>Prima di ristrutturare:</strong> non si pu\u00f2 depositare una CILA o SCIA su un immobile con abusi non sanati.</li><li><strong>In caso di successione:</strong> gli eredi rispondono degli abusi del de cuius se non identificati prima della divisione.</li></ul>''',

    'cambio-destinazione-d-uso.html': '''<h2>Cambio destinazione d\u2019uso in Sicilia: cosa verificare prima di iniziare</h2><p>Il cambio di destinazione d\u2019uso (CDU) non \u00e8 solo una pratica edilizia: \u00e8 anche un passaggio urbanistico che modifica le dotazioni di parcheggio, gli standard di abitabilit\u00e0 e gli oneri di urbanizzazione. In molti comuni siciliani il PRG limita i CDU in determinate zone: non tutto ci\u00f2 che \u00e8 tecnicamente possibile \u00e8 urbanisticamente ammissibile.</p><p>Il CDU con opere (es. da locale commerciale a residenziale con interventi di ristrutturazione) richiede di norma un Permesso di Costruire o SCIA alternativa al PdC. Il CDU senza opere (solo variazione d\u2019uso senza lavori) \u00e8 in genere pi\u00f9 rapido ma ugualmente soggetto a verifica dei requisiti igienico-sanitari e impiantistici.</p><p>Casi frequenti in Sicilia: trasformazione di garage in unit\u00e0 abitativa (spesso non consentita se la quota del piano \u00e8 sotto il livello stradale o se l\u2019altezza \u00e8 inferiore a 2,70 m), trasformazione di locali commerciali al piano terra in residenziale (in centro storico spesso vietata dai PRG per tutela del commercio di prossimit\u00e0), frazionamento con cambio d\u2019uso su grandi appartamenti storici.</p><h3>Oneri di urbanizzazione nel CDU</h3><p>Quando il cambio di destinazione comporta un aumento del carico urbanistico (es. da produttivo a residenziale), il comune pu\u00f2 richiedere il pagamento degli oneri di urbanizzazione secondaria. L\u2019importo varia per comune e per tipologia di cambio: Studio 4e calcola preventivamente il costo complessivo dell\u2019operazione prima di avviare l\u2019iter.</p>''',
}


def process_file(filename, content_html):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f'  SKIP (not found): {filename}')
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'Come funziona nel dettaglio' in html or 'Come si imposta' in html or 'Le fasi di' in html or 'Cos\u2019\u00e8 la verifica dello stato' in html or 'Oneri di urbanizzazione nel CDU' in html:
        print(f'  SKIP (already has content): {filename}')
        return False

    anchor = ANCHOR if ANCHOR in html else (ANCHOR_ALT if ANCHOR_ALT in html else None)
    if not anchor:
        print(f'  ERROR (anchor not found): {filename}')
        return False

    new_html = html.replace(anchor, anchor + content_html, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'  OK: {filename}')
    return True


if __name__ == '__main__':
    print('Adding unique content sections to service pages...')
    updated = 0
    for filename, content_html in CONTENT.items():
        if process_file(filename, content_html):
            updated += 1
    print(f'\nDone: {updated} files updated.')
