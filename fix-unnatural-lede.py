#!/usr/bin/env python3
"""
Rewrite unnatural lede paragraphs with human-sounding text
"""

import re
from pathlib import Path

ROOT_DIR = Path(".")

# Natural replacements by keyword/topic
NATURAL_LEDES = {
    'architetto': 'Scegliere un architetto richiede attenzione a competenze tecniche e approccio al progetto.',
    'sanatoria': 'Le sanatorie edilizie richiedono verifiche puntuali su conformità e tempistiche.',
    'ristrutturazione appartamento': 'Una ristrutturazione ben pianificata parte da un rilievo accurato e un capitolato chiaro.',
    'ristrutturazione villa': 'Ristrutturare una villa richiede coordinamento tra impianti, strutture e finiture.',
    'cila': 'La CILA copre interventi di manutenzione straordinaria che non modificano volumi o destinazioni.',
    'scia': 'La SCIA serve per opere che modificano prospetti, volumi o strutture portanti.',
    'permesso': 'Il permesso di costruire è obbligatorio per nuove costruzioni e ampliamenti significativi.',
    'computo metrico': 'Un computo metrico preciso evita varianti in corso d\'opera e contenziosi con l\'impresa.',
    'capitolato': 'Il capitolato definisce materiali, lavorazioni e tolleranze: è la base del contratto.',
    'direzione lavori': 'La direzione lavori controlla qualità, tempi e rispetto del progetto autorizzato.',
    'verifica stato legittimo': 'Lo stato legittimo confronta lo stato di fatto con i titoli edilizi: ogni difformità va sanata.',
    'regolarità urbanistica': 'La regolarità urbanistica si verifica confrontando planimetrie catastali e titoli edilizi.',
    'vincoli': 'I vincoli paesaggistici e storici condizionano materiali, colori e modifiche volumetriche.',
    'cambio destinazione': 'Il cambio di destinazione d\'uso richiede verifica urbanistica e spesso opere strutturali.',
    'frazionamento': 'Il frazionamento separa un\'unità in due o più unità autonome con accessi indipendenti.',
    'accorpamento': 'L\'accorpamento unisce più unità immobiliari in una sola, con un iter catastale e urbanistico.',
    'isolamento': 'L\'isolamento termico e acustico richiede scelta di materiali e dettagli di posa certificati.',
    'serramenti': 'I serramenti influenzano prestazioni energetiche, tenuta all\'aria e comfort acustico.',
    'impianti': 'Gli impianti vanno progettati e coordinati prima di chiudere tracce e controsoffitti.',
    'rilievo': 'Il rilievo accurato è la base per progetto e computo: errori di misura costano tempo e denaro.',
    'pratica': 'Ogni pratica edilizia richiede documenti specifici e verifica dello stato legittimo.',
    'progetto': 'Un progetto completo prevede elaborati grafici, relazioni tecniche e computo estimativo.',
    'cronoprogramma': 'Il cronoprogramma definisce sequenze di lavoro e milestone per tenere sotto controllo i tempi.',
    'varianti': 'Le varianti in cantiere vanno autorizzate se modificano quanto approvato nel titolo edilizio.',
    'interior design': 'L\'interior design unisce estetica e funzionalità: layout, materiali e illuminazione contano.',
    'bagno': 'Il progetto del bagno richiede pendenze, impermeabilizzazioni e ventilazione adeguate.',
    'cucina': 'La cucina richiede ergonomia degli spazi, ventilazione forzata e impianti dedicati.',
    'scala': 'Le scale interne devono rispettare alzate, pedate e larghezze minime per sicurezza e comfort.',
    'tetto': 'Tetti e coperture richiedono impermeabilizzazioni, ventilazione e manutenzione programmata.',
    'facciata': 'Il rifacimento di facciate richiede autorizzazioni e scelta di materiali durevoli.',
    'efficienza energetica': 'L\'efficienza energetica dipende da isolamento, serramenti, impianti e ponti termici.',
    'cappotto': 'Il cappotto termico riduce dispersioni ma richiede dettagli corretti per evitare condense.',
    'acustica': 'L\'acustica interna si migliora con materiali fonoisolanti e masse appropriate su pareti e solai.',
    'accessibilità': 'L\'accessibilità richiede rampe, ascensori e bagni conformi alle norme vigenti.',
    'b&b': 'I B&B richiedono conformità urbanistica, sicurezza antincendio e requisiti igienico-sanitari.',
    'locale commerciale': 'I locali commerciali richiedono layout funzionale, sicurezza e conformità alle normative.',
    'ufficio': 'Gli uffici richiedono illuminazione naturale, aerazione e rispetto dei requisiti di sicurezza.',
}

def get_natural_lede(filepath, original_lede):
    """Generate natural lede based on file path and content"""

    path_str = str(filepath).lower()
    lede_lower = original_lede.lower()

    # Extract city if present
    city_match = re.search(r'A ([A-Z][a-zà-ù]+),', original_lede)
    city = city_match.group(1) if city_match else None

    # Find matching keyword
    for keyword, natural_text in NATURAL_LEDES.items():
        if keyword in path_str or keyword in lede_lower:
            if city:
                return f'A {city}, {natural_text}'
            else:
                return natural_text

    # Fallback: generic professional text
    if city:
        return f'A {city}, ogni intervento edilizio richiede verifiche tecniche e amministrative accurate.'
    else:
        return 'Ogni intervento edilizio richiede verifiche tecniche e amministrative accurate.'

def fix_lede(filepath, content):
    """Fix unnatural lede paragraph"""

    # Find lede
    lede_match = re.search(r'<p class="lede">([^<]+)</p>', content, re.DOTALL)
    if not lede_match:
        return content

    original_lede = lede_match.group(1).strip()

    # Check if unnatural
    unnatural_patterns = [
        r'[a-zà-ù\s]+ diventa (?:un problema|critico) quando',
        r'ogni dettaglio conta\.',
        r'A \w+, [a-zà-ù\s]+ diventa',
    ]

    is_unnatural = any(re.search(p, original_lede, re.IGNORECASE) for p in unnatural_patterns)

    if not is_unnatural:
        return content

    # Generate natural replacement
    natural_lede = get_natural_lede(filepath, original_lede)

    # Replace
    content = content.replace(
        f'<p class="lede">{original_lede}</p>',
        f'<p class="lede">{natural_lede}</p>'
    )

    return content

def process_file(filepath):
    """Process single file"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<p class="lede">' not in content:
        return False

    original = content
    content = fix_lede(filepath, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    print("🚀 Rewriting unnatural lede paragraphs...")
    print()

    guide_files = list(ROOT_DIR.glob("guide/**/*.html")) + list(ROOT_DIR.glob("sicilia/**/*.html"))

    processed = 0

    for filepath in guide_files:
        if 'backup-original' in str(filepath):
            continue

        if process_file(filepath):
            processed += 1
            if processed <= 15:
                print(f"✅ {filepath.relative_to(ROOT_DIR)}")

    print()
    if processed > 15:
        print(f"... and {processed - 15} more files")
    print()
    print(f"✅ Done! Rewrote {processed} unnatural ledes")
    print()
    print("All ledes now sound human-written.")

if __name__ == "__main__":
    main()
