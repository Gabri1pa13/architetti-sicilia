# ✅ VERIFICA ORA - Test Rapidi Post-Implementazione

Tutte le modifiche sono state applicate. Ora verifica che funzioni tutto.

---

## 🔍 TEST 1: Apri pagina in browser (30 secondi)

```bash
# Da terminale, apri una guida
open guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html
```

**Checklist visiva:**
- [ ] Dopo H1 vedi box con "📞 Hai un caso urgente?"
- [ ] Più in basso vedi CTA con "🚨 Rogito bloccato"
- [ ] In fondo alla CTA vedi "⭐ 4.8/5 su Houzz • 50+ progetti"
- [ ] Title nel tab browser è pulito (no `<span>`)
- [ ] Pagina si carica velocemente

**Se tutto OK → Continua**

---

## 🔍 TEST 2: Valida structured data (2 minuti)

1. Vai su: https://search.google.com/test/rich-results
2. Inserisci URL: `https://architettisicilia.it/guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html`
3. Click "Test URL"

**Target:** ZERO errori. Se ci sono errori "name contains HTML" → problema non risolto.

**Se 0 errori → Perfetto! Rich snippet funzioneranno.**

---

## 🔍 TEST 3: Performance check (2 minuti)

1. Vai su: https://pagespeed.web.dev/
2. Testa homepage: `https://architettisicilia.it/`
3. Guarda metriche mobile

**Target:**
- LCP (Largest Contentful Paint): < 2.5s 🟢
- CLS (Cumulative Layout Shift): < 0.1 🟢
- FID (First Input Delay): < 100ms 🟢

**Se LCP > 3s 🔴:** Possibile problema font/immagini, ma structured data fix è OK.

---

## 🔍 TEST 4: Mobile real device (1 minuto)

1. Apri guida su smartphone: https://architettisicilia.it/guide/palermo/sanatoria-edilizia-a-palermo-cosa-si-puo-regolarizzare-davvero.html
2. Tap su "📞 Chiama ora: +39 329 973 6697"

**Deve:** Aprire dialer telefono con numero pre-compilato.

3. Tap su "WhatsApp"

**Deve:** Aprire app WhatsApp (o web) con messaggio pre-compilato.

**Se funzionano → Click-to-call OK!**

---

## 🔍 TEST 5: Verifica homepage (1 minuto)

```bash
open index.html
```

**Checklist:**
- [ ] Sotto i badge "711+ pagine" vedi nuovi badge:
  - ⭐ 4.8/5 su Houzz
  - 50+ progetti
  - Dal 2002 a Palermo

**Se ci sono → Social proof OK!**

---

## 📊 COSA FARE DOPO (settimana prossima)

### 1. Setup Google Tag Manager (2h, priorità ALTA)

Senza tracking non sai quante chiamate genera il sito.

**Steps:**
1. Vai su https://tagmanager.google.com/
2. Crea account → container `architettisicilia.it`
3. Copia GTM ID (es: `GTM-ABC1234`)
4. Modifica file: `nano add-conversion-tracking.py`
5. Cerca `GTM-XXXXX` e sostituisci con il tuo ID
6. Esegui: `python3 add-conversion-tracking.py`
7. In GTM: crea trigger per eventi `click_phone`, `click_whatsapp`
8. Collega GTM a Google Analytics 4

**Risultato:** Saprai esattamente quale pagina genera quale chiamata.

---

### 2. Monitora ranking (settimana 1-4)

**Google Search Console:**
- Performance → Confronta "Last 28 days" vs periodo precedente
- Guarda: Impressions, Clicks, CTR, Average position
- Target settimana 2-3: Vedere +5-10 posizioni medie
- Target settimana 4: Vedere +10-20% impressions

**Come:**
1. Vai su https://search.google.com/search-console
2. Verifica proprietà dominio (se non già fatto)
3. Performance → Confronta periodi

---

### 3. Monitora conversioni (settimana 1-4)

**Manuale (fino a setup GTM):**
- Conta lead/settimana
- Chiedi a ogni chiamata: "Dove ci hai trovato?"
- Tieni registro: Google / Diretto / Altro

**Con GTM (dopo setup):**
- Google Analytics 4 → Events → `click_phone` count
- Conversion rate: eventi / pageviews

**Target:** +30-50% lead entro 30 giorni vs baseline.

---

## 🚨 SE QUALCOSA NON VA

### Problema: Pagine sembrano rotte

**Ripristina da backup:**
```bash
cd /Users/gabrielecostanzo/Desktop
rm -rf "architetti-sicilia_-3 2"
cp -r "architetti-sicilia-backup-20260126-135908" "architetti-sicilia_-3 2"
```

### Problema: Rich Results Test mostra errori

**Check:** Apri file HTML, cerca `<script type="application/ld+json">`, verifica che NON contenga `<a>` o `<span>` nel JSON.

Se contiene HTML → Script non ha funzionato su quel file specifico.

### Problema: CSS/JS non caricano

**Check:** Apri DevTools (F12) → Console → Cerca errori 404.

Se vedi 404 su `.min.css` o `.min.js` → File minificati mancano.

**Fix:**
```bash
python3 minify-assets.py
```

---

## ✅ TUTTO OK? NEXT STEPS

Se tutti i test sopra passano:

1. **Oggi:**
   - [ ] Upload su server produzione (se non già fatto)
   - [ ] Test live su https://architettisicilia.it/

2. **Questa settimana:**
   - [ ] Setup GTM + tracking conversioni
   - [ ] Verifica Google Search Console collegato

3. **Prossime 4 settimane:**
   - [ ] Monitora ranking settimanale
   - [ ] Conta lead/settimana
   - [ ] Confronta con baseline pre-modifiche

4. **Dopo 30 giorni:**
   - [ ] Report risultati: traffico, posizioni, lead
   - [ ] Decide prossime ottimizzazioni

---

**Hai domande?** Rileggi [IMPLEMENTATION-REPORT.md](IMPLEMENTATION-REPORT.md) per dettagli completi.

**Tutto chiaro?** Inizia dal Test 1 sopra. 👆
