# 🚀 Architetti Sicilia - Optimization Guide

Questa guida spiega come applicare tutte le ottimizzazioni tecniche e di conversione per massimizzare ranking SEO e lead generation.

## 📋 Cosa fanno questi script

### 1. `fix-structured-data.py`
**Impatto: 🔴 CRITICO - Risolve penalizzazioni SEO immediate**

- Rimuove HTML da JSON-LD (Google può finalmente leggere structured data)
- Fix title tags (remove `<span>` e `<a>`)
- Aggiunge lazy loading nativo alle immagini
- Estrae CSS inline duplicato in file esterno

**Risultato atteso:**
- Rich snippet funzionanti nei SERP
- Core Web Vitals migliorati
- -1.5MB di banda risparmiata

### 2. `add-conversion-tracking.py`
**Impatto: 🟠 ALTO - Ti permette di misurare ROI**

- Installa Google Tag Manager
- Traccia click su telefono
- Traccia click su WhatsApp
- Traccia submit form

**Risultato atteso:**
- Sapere quante chiamate genera ogni pagina
- Capire quali province convertono meglio
- Ottimizzare investimento in base ai dati

### 3. `add-social-proof.py`
**Impatto: 🟡 MEDIO - Aumenta conversioni del 15-25%**

- Aggiunge rating 4.8/5 e badge "50+ progetti"
- CTA personalizzate per tipo pagina:
  - **Sanatorie**: CTA urgente con telefono prominente
  - **Ristrutturazioni**: CTA preventivo gratuito
  - **Pratiche**: CTA consulenza telefonica
- Telefono cliccabile dopo ogni H1

**Risultato atteso:**
- Conversioni +15-25% (dato industria per social proof)
- Click-to-call più veloci (meno friction)

### 4. `minify-assets.py`
**Impatto: 🟢 BASSO - Performance boost marginale**

- Minifica CSS/JS (risparmio 30-40% banda)
- Aggiorna riferimenti HTML

**Risultato atteso:**
- Caricamento pagina -200-300ms
- Core Web Vitals migliorati marginalmente

---

## 🎯 Esecuzione Step-by-Step

### Step 0: Requisiti
```bash
# Installa Python 3.7+ se non ce l'hai
python3 --version

# Installa dipendenze
pip install beautifulsoup4 csscompressor
```

### Step 1: Backup completo
```bash
# Crea backup manuale PRIMA di qualsiasi script
cp -r . ../architetti-sicilia-backup-$(date +%Y%m%d)
```

### Step 2: Fix strutturali (PRIORITÀ 1)
```bash
python3 fix-structured-data.py
```

**Cosa succede:**
- Crea cartella `backup-original/` con file originali
- Processa tutti gli 800 HTML
- Tempo stimato: 2-3 minuti

**Verifica manuale:**
1. Apri `guide/palermo/architetto-a-palermo-come-impostare-un-progetto-senza-sorprese.html`
2. Cerca `<script type="application/ld+json">` nel codice
3. Verifica che NON ci siano `<a>` o `<span>` dentro il JSON
4. Apri pagina in browser, controlla che tutto sia visibile

**Se qualcosa va storto:**
```bash
# Ripristina da backup
rm -rf guide/ servizi/ studio-4e/ en/ sicilia/ index.html
cp -r backup-original/* .
```

### Step 3: Tracking conversioni (PRIORITÀ 2)

**PRIMA di eseguire:**
1. Vai su [Google Tag Manager](https://tagmanager.google.com/)
2. Crea account (se non ce l'hai)
3. Crea container per `architettisicilia.it`
4. Copia il tuo GTM ID (es: `GTM-ABC1234`)

**Modifica script:**
```bash
nano add-conversion-tracking.py
# Cerca GTM-XXXXX e sostituisci con il tuo ID reale
# Salva: Ctrl+O, Esci: Ctrl+X
```

**Esegui:**
```bash
python3 add-conversion-tracking.py
```

**Setup GTM (dopo script):**
1. Vai in GTM → Triggers → New
2. Crea trigger per evento `click_phone`
3. Crea tag Google Analytics collegato
4. Pubblica container
5. Testa: apri una pagina, clicca telefono, verifica evento in GA4 Realtime

### Step 4: Social proof e CTA (PRIORITÀ 3)
```bash
python3 add-social-proof.py
```

**Verifica manuale:**
1. Apri `index.html` → Cerca badge "⭐ 4.8/5 su Houzz"
2. Apri guida sanatoria → Cerca "🚨 Rogito bloccato"
3. Apri guida ristrutturazione → Cerca "Stai pianificando una ristrutturazione?"

### Step 5: Minificazione (OPZIONALE)
```bash
python3 minify-assets.py
```

---

## 🧪 Test Post-Implementazione

### Test 1: Structured Data
```bash
# Valida structured data su Google
# Vai su: https://search.google.com/test/rich-results
# Inserisci URL: https://architettisicilia.it/guide/palermo/architetto-a-palermo-come-impostare-un-progetto-senza-sorprese.html
# Verifica: ZERO errori
```

### Test 2: Core Web Vitals
```bash
# PageSpeed Insights
# Vai su: https://pagespeed.web.dev/
# Inserisci URL homepage
# Target: LCP < 2.5s, CLS < 0.1
```

### Test 3: Conversioni
1. Apri pagina in incognito su mobile
2. Clicca telefono → Verifica che si apra dialer
3. Clicca WhatsApp → Verifica che si apra app
4. Vai in GTM Debug mode → Verifica eventi triggered

---

## 📊 Risultati Attesi (30 giorni)

| Metrica | Prima | Dopo | Delta |
|---------|-------|------|-------|
| **Rich snippet** | 0% pagine | 80%+ pagine | +80% |
| **Core Web Vitals (mobile)** | Rosso | Arancione/Verde | +20-30 posizioni |
| **Conversione traffico → lead** | ~1-2% | ~2.5-3.5% | +50-100% |
| **Click-through rate SERP** | ~2-3% | ~4-5% | +50% (grazie a rich snippet) |

**Stima lead aggiuntivi/mese:**
- Traffico attuale: ~2000 visite/mese (stima conservativa per 800 pagine)
- Conversione prima: 1.5% = 30 lead/mese
- Conversione dopo: 3% = 60 lead/mese
- **+30 lead/mese = +1 lead/giorno**

---

## 🔧 Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Problema: Script si blocca su un file
```bash
# Trova il file problematico
python3 fix-structured-data.py 2>&1 | tee log.txt
# Controlla log.txt, cerca l'ultimo file processato
# Apri quel file manualmente e verifica HTML valido
```

### Problema: Pagine sembrano rotte dopo script
```bash
# Ripristina da backup
cp -r backup-original/* .
# Controlla encoding file:
file -I index.html
# Deve essere: text/html; charset=utf-8
```

### Problema: GTM non traccia eventi
1. Apri browser DevTools → Console
2. Digita: `dataLayer`
3. Dovrebbe mostrare array con eventi
4. Se undefined: GTM non caricato, controlla GTM ID

---

## 📈 Prossimi Step (Opzionali)

### 1. Espansione local SEO
Crea pagine per comuni top-20:
- Mondello, Cefalù, Taormina, Siracusa centro, etc.
- Template: 70% comune + 30% specifico comune

### 2. Call tracking dinamico
Servizi tipo CallRail per assegnare numero univoco per sorgente traffico

### 3. A/B test CTA
Con traffico aumentato, testare:
- Colore pulsante telefono
- Wording "Chiama ora" vs "Parlaci del tuo progetto"
- Posizione form

### 4. Retargeting Facebook/Google
Pixel già pronto con GTM, attivare campagne per chi visita 3+ pagine

---

## 📞 Supporto

Se qualcosa non funziona o hai dubbi:
1. Controlla log.txt per errori
2. Verifica che Python sia 3.7+
3. Assicurati di avere permessi scrittura su tutte le cartelle

**IMPORTANTE:** Testa SEMPRE su una pagina prima di eseguire su tutte le 800.

---

**Ultima modifica:** 26 Gennaio 2026
**Autore:** Claude (Sonnet 4.5)
**Progetto:** Architetti Sicilia Lead Generation Optimization
