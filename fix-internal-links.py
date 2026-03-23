#!/usr/bin/env python3
"""
fix-internal-links.py
Aggiorna le pagine servizio con link alle guide di tutte e 9 le province siciliane.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVIZI_DIR = os.path.join(BASE_DIR, "servizi")
GUIDE_DIR = os.path.join(BASE_DIR, "guide")

PROVINCES = [
    ("palermo", "Palermo"),
    ("catania", "Catania"),
    ("messina", "Messina"),
    ("siracusa", "Siracusa"),
    ("ragusa", "Ragusa"),
    ("trapani", "Trapani"),
    ("agrigento", "Agrigento"),
    ("enna", "Enna"),
    ("caltanissetta", "Caltanissetta"),
]

# Mapping: slug del file servizio → lista di slug guida (con {p} per la provincia)
SERVICE_GUIDE_MAPPING = {
    "pratiche-edilizie-cila-scia-e-permessi": [
        ("cila-a-{p}-quando-serve-e-cosa-cambia-in-cantiere", "CILA a {pn}"),
        ("scia-a-{p}-casi-tipici-e-errori-che-bloccano-i-lavori", "SCIA a {pn}"),
        ("permessi-e-vincoli-a-{p}-come-riconoscerli-prima-di-firmare", "Permessi e vincoli a {pn}"),
    ],
    "sanatorie-e-pratiche-in-sanatoria": [
        ("sanatoria-edilizia-a-{p}-cosa-si-puo-regolarizzare-davvero", "Sanatoria edilizia a {pn}"),
    ],
    "cambio-destinazione-d-uso": [
        ("cambio-destinazione-duso-a-{p}-cosa-verificare-prima-di-iniziare", "Cambio destinazione d'uso a {pn}"),
    ],
    "direzione-lavori-e-controllo-qualita": [
        ("direzione-lavori-a-{p}-cosa-controlla-il-direttore-lavori", "Direzione lavori a {pn}"),
    ],
    "pratiche-catastali-e-docfa": [
        ("catasto-a-{p}-variazioni-docfa-e-tempi-realistici", "Catasto e DOCFA a {pn}"),
    ],
    "verifica-stato-legittimo-e-regolarita-urbanistica": [
        ("verifica-stato-legittimo-a-{p}-da-dove-si-parte", "Stato legittimo a {pn}"),
        ("regolarita-urbanistica-a-{p}-come-evitare-problemi-al-rogito", "Regolarità urbanistica a {pn}"),
    ],
    "computo-metrico-estimativo": [
        ("computo-metrico-a-{p}-perche-evita-varianti-e-contenziosi", "Computo metrico a {pn}"),
    ],
    "capitolato-lavori-e-specifiche": [
        ("capitolato-lavori-a-{p}-come-renderlo-chiaro-e-misurabile", "Capitolato lavori a {pn}"),
    ],
    "rilievo-architettonico-e-restituzione": [
        ("rilievo-e-restituzione-a-{p}-errori-di-misura-che-costano", "Rilievo e restituzione a {pn}"),
    ],
    "isolamento-termico-e-acustico": [
        ("isolamento-e-comfort-a-{p}-come-ridurre-dispersioni-e-rumori", "Isolamento a {pn}"),
        ("acustica-interna-a-{p}-soluzioni-pratiche-per-pareti-e-solai", "Acustica a {pn}"),
    ],
    "efficientamento-energetico-e-comfort-abitativo": [
        ("cappotto-termico-a-{p}-rischi-di-condensa-e-dettagli", "Cappotto termico a {pn}"),
    ],
    "ristrutturazione-completa-di-appartamenti": [
        ("ristrutturazione-appartamento-a-{p}-tempi-fasi-e-documenti", "Ristrutturazione appartamento a {pn}"),
    ],
    "ristrutturazione-di-ville-e-case-indipendenti": [
        ("ristrutturazione-villa-a-{p}-controllo-qualita-e-capitolato", "Ristrutturazione villa a {pn}"),
    ],
    "coperture-tetti-terrazzi-e-impermeabilizzazioni": [
        ("tetto-e-coperture-a-{p}-come-prevenire-problemi-ricorrenti", "Tetti e coperture a {pn}"),
    ],
    "progetto-di-interni-cucina-bagno-living": [
        ("progetto-bagno-a-{p}-pendenze-impermeabilizzazioni-e-dettagli", "Progetto bagno a {pn}"),
        ("progetto-cucina-a-{p}-ergonomia-impianti-e-ventilazione", "Progetto cucina a {pn}"),
        ("interior-design-a-{p}-come-unire-estetica-e-funzionalita", "Interior design a {pn}"),
    ],
    "progetto-facciate-e-finiture-esterne": [
        ("rifacimento-facciata-a-{p}-autorizzazioni-e-scelte-materiali", "Facciata a {pn}"),
    ],
    "sicurezza-e-coordinamento-in-cantiere": [
        ("sicurezza-in-cantiere-a-{p}-ruoli-e-responsabilita", "Sicurezza in cantiere a {pn}"),
    ],
    "assistenza-tecnica-per-acquisto-immobili": [
        ("due-diligence-prima-dellacquisto-a-{p}-check-tecnico-in-10-punti", "Due diligence a {pn}"),
    ],
    "check-up-tecnico-per-immobili-datati": [
        ("due-diligence-prima-dellacquisto-a-{p}-check-tecnico-in-10-punti", "Due diligence a {pn}"),
    ],
    "accessibilita-e-rimozione-barriere-architettoniche": [
        ("barriere-architettoniche-a-{p}-interventi-e-requisiti-essenziali", "Barriere architettoniche a {pn}"),
    ],
    "progetto-impianti-e-coordinamento-tecnico": [
        ("progetto-impianti-a-{p}-elettrico-e-idrico-senza-improvvisazioni", "Progetto impianti a {pn}"),
    ],
    "studio-di-fattibilita-e-scenari-di-intervento": [
        ("studio-di-fattibilita-a-{p}-come-decidere-prima-di-spendere", "Studio di fattibilità a {pn}"),
    ],
    "gestione-varianti-e-contabilita-lavori": [
        ("gestione-varianti-in-cantiere-a-{p}-quando-sono-accettabili", "Gestione varianti a {pn}"),
    ],
    "adeguamenti-per-b-b-e-case-vacanza": [
        ("accessibilita-e-b-b-a-{p}-cosa-rende-la-struttura-conforme", "B&B e accessibilità a {pn}"),
        ("pratica-edilizia-per-b-b-a-{p}-cosa-serve-davvero", "Pratica edilizia B&B a {pn}"),
    ],
    "coordinamento-fornitori-e-arredi-su-misura": [
        ("interior-design-a-{p}-come-unire-estetica-e-funzionalita", "Interior design a {pn}"),
    ],
    "progettazione-per-locali-commerciali": [
        ("ristrutturare-un-locale-commerciale-a-{p}-layout-impianti-norme", "Locale commerciale a {pn}"),
    ],
    "progettazione-per-uffici-e-studi-professionali": [
        ("progetto-per-ufficio-a-{p}-spazi-impianti-e-sicurezza", "Progetto ufficio a {pn}"),
    ],
    "relazioni-tecniche-e-documentazione-di-progetto": [
        ("relazione-tecnica-asseverata-a-{p}-cosa-contiene-e-perche", "Relazione tecnica a {pn}"),
    ],
    "supporto-in-fase-di-preventivazione-e-gara-imprese": [
        ("stima-costi-ristrutturazione-a-{p}-come-leggere-un-preventivo", "Preventivazione a {pn}"),
    ],
    "selezione-materiali-e-dettagli-esecutivi": [
        ("scelta-pavimenti-a-{p}-resistenze-posa-e-manutenzione", "Pavimenti a {pn}"),
        ("serramenti-a-{p}-prestazioni-posa-e-pratica-energetica", "Serramenti a {pn}"),
    ],
    # Fallback per servizi non mappati esplicitamente
    "_default": [
        ("architetto-a-{p}-come-impostare-un-progetto-senza-sorprese", "Architetto a {pn}"),
    ],
}


def guide_exists(province_slug, guide_slug):
    path = os.path.join(GUIDE_DIR, province_slug, guide_slug + ".html")
    return os.path.exists(path)


def build_province_section(service_slug):
    """Costruisce la nuova sezione HTML con guide per tutte le province."""
    guide_templates = SERVICE_GUIDE_MAPPING.get(
        service_slug, SERVICE_GUIDE_MAPPING["_default"]
    )

    province_blocks = []
    for prov_slug, prov_name in PROVINCES:
        links = []
        for guide_tmpl, label_tmpl in guide_templates:
            guide_slug = guide_tmpl.replace("{p}", prov_slug)
            label = label_tmpl.replace("{pn}", prov_name)
            if guide_exists(prov_slug, guide_slug):
                href = f"/guide/{prov_slug}/{guide_slug}.html"
                links.append(f'<li><a href="{href}">{label}</a></li>')

        if links:
            links_html = "\n          ".join(links)
            province_blocks.append(
                f'<div>\n'
                f'      <strong>{prov_name}</strong>\n'
                f'      <ul style="padding-left:16px; margin:6px 0 0">\n'
                f'        {links_html}\n'
                f'      </ul>\n'
                f'    </div>'
            )

    if not province_blocks:
        return None

    blocks_html = "\n    ".join(province_blocks)
    section = (
        '<section class="related-guides" style="margin-top:32px; padding:20px; '
        'background:#f9f6f8; border-radius:12px">\n'
        '<h2 style="font-size:18px; margin-top:0">Guide per provincia</h2>\n'
        '<div style="display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); '
        'gap:12px; margin-top:12px">\n'
        f'    {blocks_html}\n'
        '</div>\n'
        '</section>'
    )
    return section


def update_service_file(filepath, service_slug):
    """Sostituisce la sezione related-guides in un file servizio."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_section = build_province_section(service_slug)
    if not new_section:
        print(f"  SKIP (no guides found): {service_slug}")
        return False

    # Pattern per trovare la sezione related-guides esistente
    pattern = r'<section class="related-guides"[^>]*>.*?</section>'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        new_content = content[:match.start()] + new_section + content[match.end():]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  UPDATED (replaced): {service_slug}")
        return True
    else:
        # Inserisci prima del footer se non esiste la sezione
        insert_before = '</article>'
        if insert_before in content:
            new_content = content.replace(
                insert_before,
                '\n' + new_section + '\n' + insert_before,
                1
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  UPDATED (inserted): {service_slug}")
            return True
        else:
            print(f"  SKIP (no insertion point): {service_slug}")
            return False


def main():
    updated = 0
    skipped = 0

    service_files = [
        f for f in os.listdir(SERVIZI_DIR)
        if f.endswith(".html") and f != "index.html"
    ]

    for filename in sorted(service_files):
        service_slug = filename.replace(".html", "")
        filepath = os.path.join(SERVIZI_DIR, filename)
        print(f"Processing: {service_slug}")
        result = update_service_file(filepath, service_slug)
        if result:
            updated += 1
        else:
            skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
