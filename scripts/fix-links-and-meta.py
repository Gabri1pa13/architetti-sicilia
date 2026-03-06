#!/usr/bin/env python3
"""
1. Aggiorna related-links nelle 28 guide riscritte con link province-specifici reali.
2. Migliora meta description per tutte le 28 guide.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Mappa di tutte le pagine riscritte per provincia
GUIDE_MAP = {
    'palermo': ['architetto', 'cila', 'ristrutturazione-appartamento', 'sanatoria-edilizia', 'direzione-lavori', 'stima-costi-ristrutturazione', 'barriere-architettoniche'],
    'catania': ['architetto', 'cila', 'ristrutturazione-appartamento', 'sanatoria-edilizia', 'direzione-lavori', 'stima-costi-ristrutturazione', 'barriere-architettoniche'],
    'messina': ['architetto', 'cila', 'ristrutturazione-appartamento', 'sanatoria-edilizia', 'direzione-lavori', 'barriere-architettoniche'],
    'siracusa': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
    'trapani': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
    'ragusa': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
    'agrigento': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
    'enna': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
    'caltanissetta': ['architetto', 'cila', 'ristrutturazione-appartamento', 'barriere-architettoniche'],
}

FILE_SLUG = {
    'architetto': 'architetto-a-{prov}-come-impostare-un-progetto-senza-sorprese.html',
    'cila': 'cila-a-{prov}-quando-serve-e-cosa-cambia-in-cantiere.html',
    'ristrutturazione-appartamento': 'ristrutturazione-appartamento-a-{prov}-tempi-fasi-e-documenti.html',
    'sanatoria-edilizia': 'sanatoria-edilizia-a-{prov}-cosa-si-puo-regolarizzare-davvero.html',
    'direzione-lavori': 'direzione-lavori-a-{prov}-cosa-controlla-il-direttore-lavori.html',
    'stima-costi-ristrutturazione': 'stima-costi-ristrutturazione-a-{prov}-come-leggere-un-preventivo.html',
    'barriere-architettoniche': 'barriere-architettoniche-a-{prov}-interventi-e-requisiti-essenziali.html',
}

LABEL = {
    'architetto': 'Progettazione architettonica a {nome}',
    'cila': 'CILA a {nome}: quando serve',
    'ristrutturazione-appartamento': 'Ristrutturazione appartamento a {nome}',
    'sanatoria-edilizia': 'Sanatoria edilizia a {nome}',
    'direzione-lavori': 'Direzione lavori a {nome}',
    'stima-costi-ristrutturazione': 'Costi ristrutturazione a {nome}',
    'barriere-architettoniche': 'Barriere architettoniche a {nome}',
}

NOME = {
    'palermo': 'Palermo', 'catania': 'Catania', 'messina': 'Messina',
    'siracusa': 'Siracusa', 'trapani': 'Trapani', 'ragusa': 'Ragusa',
    'agrigento': 'Agrigento', 'enna': 'Enna', 'caltanissetta': 'Caltanissetta',
}

# Link a contenuti correlati nella sezione /sicilia/ per arricchire
SICILIA_LINKS = {
    'architetto': [
        ('/sicilia/comprare-casa-in-sicilia-la-checklist-tecnica-pre-acquisto-due-diligence.html', 'Due diligence tecnica prima di acquistare'),
        ('/sicilia/cila-scia-o-permesso-di-costruire-i-tempi-reali-in-sicilia-nel-2026.html', 'CILA, SCIA o Permesso: i tempi reali in Sicilia 2026'),
    ],
    'cila': [
        ('/sicilia/cila-scia-o-permesso-di-costruire-i-tempi-reali-in-sicilia-nel-2026.html', 'CILA, SCIA o Permesso: i tempi reali in Sicilia 2026'),
        ('/sicilia/il-computo-metrico-estimativo-lunico-strumento-per-controllare-i-costi.html', 'Il computo metrico estimativo: controllare i costi'),
    ],
    'ristrutturazione-appartamento': [
        ('/sicilia/ristrutturare-un-appartamento-anni-70-a-palermo-impianti-amianto-e-open-space.html', 'Ristrutturare un appartamento anni 70: impianti e open space'),
        ('/sicilia/preventivi-edili-perche-il-prezzo-a-corpo-e-una-trappola-e-come-evitarla.html', 'Preventivi edili: perché il prezzo a corpo è una trappola'),
    ],
    'sanatoria-edilizia': [
        ('/sicilia/sanatoria-edilizia-in-sicilia-cosa-e-il-doppio-confirme-e-quando-serve.html', 'Sanatoria in Sicilia: il doppio conforme e quando serve'),
        ('/sicilia/regolarita-urbanistica-a-palermo-come-evitare-problemi-al-rogito.html', 'Regolarità urbanistica: evitare problemi al rogito'),
    ],
    'direzione-lavori': [
        ('/sicilia/direttore-dei-lavori-vs-capocantiere-chi-difende-davvero-i-tuoi-interessi.html', 'Direttore lavori vs capocantiere: chi difende i tuoi interessi'),
        ('/sicilia/contratto-di-appalto-le-clausole-penali-per-ritardi-di-consegna.html', 'Contratto di appalto: clausole penali per ritardi'),
    ],
    'stima-costi-ristrutturazione': [
        ('/sicilia/costi-di-ristrutturazione-al-mq-in-sicilia-una-guida-realistica-fascia-alta.html', 'Costi ristrutturazione al mq in Sicilia: guida realistica'),
        ('/sicilia/preventivi-edili-perche-il-prezzo-a-corpo-e-una-trappola-e-come-evitarla.html', 'Preventivi edili: il prezzo a corpo è una trappola'),
    ],
    'barriere-architettoniche': [
        ('/sicilia/aprire-un-bandb-in-sicilia-requisiti-bagni-colazione-e-barriere-architettoniche.html', 'Aprire un B&B in Sicilia: requisiti e barriere architettoniche'),
        ('/sicilia/negozi-e-retail-ristrutturare-fronte-strada-e-abbattimento-barriere-rampe.html', 'Negozi: ristrutturare fronte strada e abbattimento barriere'),
    ],
}

META_DESC = {
    'architetto': 'Architetto a {nome} per pratiche edilizie, ristrutturazioni e direzione lavori. Vincoli specifici della provincia, iter CILA/SCIA e documenti necessari. Guida tecnica Studio 4e 2026.',
    'cila': 'CILA a {nome}: quando serve, cosa NON si può fare con la CILA e gli errori che bloccano i lavori. Documenti, tempi reali e iter completo 2026.',
    'ristrutturazione-appartamento': 'Ristrutturazione appartamento a {nome}: 4 fasi operative, costi 2026 (430–1.800 €/mq), documenti necessari e vincoli locali. Guida tecnica Studio 4e.',
    'sanatoria-edilizia': 'Sanatoria edilizia a {nome}: cosa si può regolarizzare, cos\'è il doppio conforme e quali abusi non sanabili. Iter pratico 2026 con tempi reali.',
    'direzione-lavori': 'Direzione lavori a {nome}: cosa controlla il DL, perché è obbligatorio, come protegge dal cantiere fermo. Guida tecnica Studio 4e 2026.',
    'stima-costi-ristrutturazione': 'Costi ristrutturazione a {nome} nel 2026: come leggere un preventivo voce per voce, cosa include (e cosa nasconde) il prezzo a corpo.',
    'barriere-architettoniche': 'Barriere architettoniche a {nome}: quali interventi serve autorizzare, detrazioni 75%, L.13/89 e specifiche tecniche DM 236/89. Guida pratica 2026.',
}

def build_related_links(prov, tipo):
    """Costruisce la sezione related-links con link reali alla provincia."""
    nome = NOME[prov]
    items = []

    # Prima: tutti gli altri tipi disponibili per questa provincia
    for t in GUIDE_MAP[prov]:
        if t == tipo:
            continue
        slug = FILE_SLUG[t].replace('{prov}', prov)
        label = LABEL[t].replace('{nome}', nome)
        items.append(f'<li><a href="/guide/{prov}/{slug}">{label}</a></li>')

    # Se non è Palermo: link alla stessa guida di Palermo (hub principale)
    if prov != 'palermo' and tipo in GUIDE_MAP['palermo']:
        slug_pa = FILE_SLUG[tipo].replace('{prov}', 'palermo')
        label_pa = LABEL[tipo].replace('{nome}', 'Palermo')
        items.append(f'<li><a href="/guide/palermo/{slug_pa}">{label_pa}</a></li>')

    # Link a contenuti /sicilia/ correlati
    for href, label in SICILIA_LINKS.get(tipo, []):
        items.append(f'<li><a href="{href}">{label}</a></li>')

    li_html = '\n'.join(items[:6])  # max 6 link
    return f'<section id="related-links"><h2>Approfondimenti correlati</h2><ul>{li_html}</ul></section>'


def process_page(prov, tipo):
    slug = FILE_SLUG[tipo].replace('{prov}', prov)
    path = ROOT / 'guide' / prov / slug
    if not path.exists():
        print(f'  SKIP (non esiste): {slug}')
        return False

    with open(path, encoding='utf-8') as f:
        html = f.read()

    changed = False

    # 1. Aggiorna related-links
    new_related = build_related_links(prov, tipo)
    if '<section id="related-links">' in html:
        new_html = re.sub(
            r'<section id="related-links">.*?</section>',
            new_related,
            html,
            flags=re.DOTALL
        )
    else:
        new_html = html.replace('</article>', new_related + '</article>', 1)

    # 2. Aggiorna meta description
    nome = NOME[prov]
    desc = META_DESC.get(tipo, '').replace('{nome}', nome)
    if desc:
        new_html = re.sub(
            r'<meta content="[^"]*" name="description"/>',
            f'<meta content="{desc}" name="description"/>',
            new_html
        )

    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        changed = True

    return changed


if __name__ == '__main__':
    total = 0
    for prov, tipi in GUIDE_MAP.items():
        for tipo in tipi:
            ok = process_page(prov, tipo)
            if ok:
                total += 1
                print(f'✅ {NOME[prov]} — {tipo}')

    print(f'\nAggiornate {total} pagine (internal links + meta description)')
