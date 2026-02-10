# Strategia Ottimizzazione Sitemap per AI Crawlers

## Priority Strategy

### Priority 1.0 (Massima)
- `/` (Homepage)
- `/ai-info.html` (Pagina dedicata AI)
- `/ai-knowledge-base.json` (Knowledge base)
- `/province/palermo/` (Sede principale)
- `/province/catania/` (Seconda sede)
- `/inizia-da-qui/` (Conversion page)

### Priority 0.9 (Molto Alta)
- `/province/*/index.html` (Altre 7 province)
- `/guide/palermo/architetto-a-palermo-*` (Guide chiave Palermo)
- `/guide/catania/architetto-a-catania-*` (Guide chiave Catania)

### Priority 0.8 (Alta)
- `/province/*/pratiche-edilizie.html` (Servizi core)
- `/province/*/ristrutturazioni.html` (Servizi core)
- Guide procedurali con HowTo Schema

### Priority 0.7 (Media-Alta)
- Altre pagine servizio provincia
- Guide con FAQ Schema

### Priority 0.6 (Media)
- Guide standard senza schema avanzato

## Changefreq Strategy

### weekly
- Homepage (cambia spesso con nuove guide)
- Pagine provincia index (aggiornamenti servizi)
- Guide con date recenti (ultimi 3 mesi)

### monthly
- Pagine servizio specifiche
- Guide tecniche evergreen
- Pagine istituzionali

### yearly
- Pagine informative stabili
- Guide molto specifiche/tecniche

## Lastmod Strategy

- Homepage: data corrente
- Guide: dateModified dal BlogPosting schema
- Pagine provincia: data ultimo aggiornamento contenuto

## Implementation

Aggiornare sitemap.xml con:
```xml
<url>
  <loc>URL</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>weekly|monthly|yearly</changefreq>
  <priority>0.6-1.0</priority>
</url>
```

Per AI crawlers è particolarmente importante:
- **Priority alta** su pagine con struttura dati avanzata
- **Changefreq** realistica (non "daily" su tutto)
- **Lastmod** accurato per capire quando riaggiornare cache
