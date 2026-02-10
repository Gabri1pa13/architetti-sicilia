// Script per estrarre recensioni da Houzz (da eseguire nella console del browser)
// 1. Apri https://www.houzz.it/professionisti/architetti/studio-4e-pfvwit-pf~1830417201
// 2. Apri la console del browser (F12 > Console)
// 3. Incolla questo script e premi Invio
// 4. Copia l'output JSON e salvalo

(function extractHouzzReviews() {
  const reviews = [];

  // Selettori possibili per le recensioni Houzz (potrebbero variare)
  const reviewElements = document.querySelectorAll('[data-testid="review-card"], .review-card, .hz-review, [class*="review"]');

  console.log(`Trovati ${reviewElements.length} elementi recensione`);

  reviewElements.forEach((element, index) => {
    try {
      // Prova diversi selettori per nome
      const authorElement = element.querySelector('[data-testid="reviewer-name"], .reviewer-name, [class*="author"], [class*="name"]');
      const author = authorElement ? authorElement.textContent.trim() : `Recensore ${index + 1}`;

      // Prova diversi selettori per data
      const dateElement = element.querySelector('[data-testid="review-date"], .review-date, time, [class*="date"]');
      let date = 'Data non trovata';
      if (dateElement) {
        date = dateElement.getAttribute('datetime') || dateElement.textContent.trim();
      }

      // Prova diversi selettori per testo recensione
      const textElement = element.querySelector('[data-testid="review-text"], .review-text, .review-body, [class*="comment"], [class*="text"]');
      const text = textElement ? textElement.textContent.trim() : '';

      // Prova diversi selettori per rating
      const ratingElement = element.querySelector('[data-testid="rating"], .rating, [class*="star"]');
      let rating = 5; // Default 5 stelle se non trovato
      if (ratingElement) {
        const ratingText = ratingElement.getAttribute('aria-label') || ratingElement.textContent;
        const match = ratingText.match(/(\d+)/);
        rating = match ? parseInt(match[1]) : 5;
      }

      if (text && text.length > 10) { // Solo recensioni con testo significativo
        reviews.push({
          author,
          date,
          text,
          rating
        });
      }
    } catch (e) {
      console.error(`Errore elaborazione recensione ${index}:`, e);
    }
  });

  const output = {
    totalReviews: reviews.length,
    extractedAt: new Date().toISOString(),
    reviews: reviews
  };

  console.log('=== RECENSIONI ESTRATTE ===');
  console.log(JSON.stringify(output, null, 2));
  console.log('\n=== COPIA IL JSON SOPRA ===');

  return output;
})();

// ISTRUZIONI ALTERNATIVE SE LO SCRIPT NON FUNZIONA:
//
// Copia manualmente ogni recensione in questo formato:
//
// Nome: [Nome Recensore]
// Data: [Data]
// Rating: [1-5 stelle]
// Testo: [Testo completo recensione]
// ---
//
// Poi invia il testo e lo converto in Schema markup
