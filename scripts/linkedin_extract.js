/**
 * Auto Applier — LinkedIn People Extractor
 *
 * Usage:
 *   1. Navigate to a LinkedIn company People page, e.g.:
 *      https://www.linkedin.com/company/{SLUG}/people/?facetSchool={SCHOOL_ID}
 *   2. Scroll to load all results.
 *   3. Open DevTools console (F12) and paste this script.
 *   4. Copy the JSON output into your workflow.
 *
 * To find your school's LinkedIn facet ID:
 *   Search your school on LinkedIn, go to the school page, and grab
 *   the numeric ID from the URL or page source.
 *
 * USC facet ID: 3084
 */

(function extractPeople() {
  const cards = document.querySelectorAll('.artdeco-entity-lockup');
  const people = [];
  const seen = new Set();

  cards.forEach(card => {
    const nameEl     = card.querySelector('.artdeco-entity-lockup__title');
    const subtitleEl = card.querySelector('.artdeco-entity-lockup__subtitle');

    if (nameEl) {
      const name     = nameEl.innerText.trim();
      const subtitle = subtitleEl ? subtitleEl.innerText.trim() : '';

      if (name && !seen.has(name) && name.length > 3) {
        seen.add(name);
        people.push({ name, title: subtitle });
      }
    }
  });

  console.log(`Found ${people.length} people:`);
  console.log(JSON.stringify(people, null, 2));
  return people;
})();
