# spec.json

```json
{
  "name": "Example Co",
  "subtitle": "HANDBOOK",
  "tagline": ["First line.", "Second line."],
  "intro": "One sentence on what the organisation does.",
  "audience": "who it is for (not shown, kept for SPECS.md)",
  "accent": "#000000",
  "logo": "/path/to/logo.png",
  "hint": "Short line under the search box.",
  "footer": "Optional footer line.", "quick_links": [{"label": "Optional label", "link": "/docs/section/page"}],
  "note": {"title1": "Short title.", "title2": "Second line.", "body": "A sentence for the note card."},
  "start_title": "New here?", "start_text": "Start with the basics.", "start_button": "Start here",
  "welcome": "Markdown for the welcome page.",
  "sections": [{"slug": "about", "name": "About", "icon": "info", "description": "One line.", "owner": "Name",
    "pages": [{"slug": "what-we-do", "title": "What we do", "description": "One line.", "owner": "Name", "order": 1, "body": "Markdown. Link pages like [this](/docs/about/what-we-do)."}]}],
  "people": [{"slug": "name", "name": "Name", "role": "Role", "section": "about", "bio": "Their one-line bio.", "responsibilities": ["What to ask them about."]}]
}
```
- Slugs: lowercase letters, digits, hyphens. Every page `owner` must be a person's `name`. Every person's `section` must be a section slug.
- Icons: info, palette, video, wrench, flask, settings, code, megaphone, sales, support, people, book, shield, money, truck, heart, home, star.
- `accent` defaults to black and white. `logo` is optional. `password` is optional (a random one is made).
- Internal links must point to pages in the spec, or to `/docs/team`. The generator refuses broken links.
