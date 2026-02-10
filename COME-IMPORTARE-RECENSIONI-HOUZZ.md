# Come Importare Recensioni da Houzz

## Metodo 1: Script Browser (Veloce)

1. Apri https://www.houzz.it/professionisti/architetti/studio-4e-pfvwit-pf~1830417201
2. Scorri verso il basso fino alla sezione "Recensioni"
3. Premi **F12** per aprire Developer Tools
4. Vai alla tab **Console**
5. Copia il contenuto di `scrape-houzz-reviews.js` e incollalo nella console
6. Premi **Invio**
7. Lo script estrarrà tutte le recensioni in formato JSON
8. Copia l'output JSON
9. Inviamelo e lo converto in Schema markup

## Metodo 2: Copia Manuale (Sempre Funziona)

Vai su Houzz e per ogni recensione copia:

```
Nome: Mario Rossi
Data: 15 novembre 2025
Rating: 5
Testo: Professionisti eccellenti. Hanno seguito la nostra ristrutturazione...
---

Nome: Laura Bianchi
Data: 3 ottobre 2025
Rating: 5
Testo: Studio molto preparato su vincoli...
---
```

Poi inviami il testo così e lo converto automaticamente.

## Metodo 3: Screenshot

Fai screenshot delle recensioni e inviameli. Le trascrivo io.

## Metodo 4: Esporta da Houzz Pro

Se hai accesso alla dashboard Houzz Pro:
1. Vai su Account > Recensioni
2. Cerca opzione "Esporta" o "Download"
3. Scarica CSV/Excel
4. Inviamelo

---

## Formato Output che Creerò

```json
{
  "@type": "Review",
  "author": {
    "@type": "Person",
    "name": "Mario Rossi"
  },
  "datePublished": "2025-11-15",
  "reviewBody": "Professionisti eccellenti...",
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

Questo verrà poi integrato in:
- Homepage (index.html)
- Pagine provincia (Palermo, Catania)
- Pagina ai-info.html

## Benefici

✅ Rich snippets Google con stelle
✅ AI assistants vedono social proof
✅ Trust signals aumentati
✅ Featured nelle ricerche "recensioni Studio 4e"
