# Come Importare Recensioni da Houzz e Google

## Step 1: Raccogliere Recensioni

### Da Houzz
1. Vai su: https://www.houzz.it/professionisti/architetti-e-progettisti-di-interni/studio-4e-pfvwit-pf~[TUO-ID]
2. Copia le recensioni migliori (5-10)
3. Per ogni recensione annota:
   - Nome recensore
   - Data
   - Testo completo
   - Rating (sempre 5/5)

### Da Google Business
1. Vai su Google Business Profile: Studio 4e Palermo
2. Sezione "Recensioni"
3. Copia le recensioni migliori (5-10)
4. Per ogni recensione annota:
   - Nome recensore
   - Data
   - Testo completo
   - Rating

## Step 2: Popolare Template

Apri `review-schema-template.json` e sostituisci i placeholder:
- `[NOME RECENSORE X]` → Nome reale
- `[TESTO RECENSIONE]` → Testo completo recensione
- Data → Data effettiva pubblicazione

## Step 3: Aggiungere Schema alle Pagine

### Homepage (index.html)
Aggiungi il Review Schema nel LocalBusiness esistente (dentro `aggregateRating`, aggiungi `review` array)

### Pagine Provincia Principali
- `/province/palermo/index.html`
- `/province/catania/index.html`

Aggiungi 2-3 recensioni più rilevanti per quella provincia

## Step 4: Verificare con Google Rich Results Test

Testa ogni pagina su:
https://search.google.com/test/rich-results

Verifica che le review siano riconosciute correttamente.

## Esempio Recensione Formattata

```json
{
  "@type": "Review",
  "author": {
    "@type": "Person",
    "name": "Marco R."
  },
  "datePublished": "2025-11-15",
  "reviewBody": "Professionisti eccellenti. Hanno seguito la ristrutturazione completa del nostro appartamento a Palermo centro storico. Gestione impeccabile di tutte le pratiche con Soprintendenza e Comune. Progetto architettonico bellissimo e direzione lavori attenta. Altamente consigliati!",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Houzz"
  }
}
```

## Benefici per AI

Con Review Schema:
✅ AI assistants possono citare recensioni reali
✅ Aumenta trust e authority
✅ Featured snippets Google con rating stelle
✅ ChatGPT/Claude vedono social proof strutturato
✅ Rich results su ricerche locali

## Note Importanti

- Usa SOLO recensioni reali (mai inventate)
- Mantieni il testo originale
- Includi date corrette
- Max 10 recensioni per pagina (le migliori)
- Mescola Houzz e Google per varietà
