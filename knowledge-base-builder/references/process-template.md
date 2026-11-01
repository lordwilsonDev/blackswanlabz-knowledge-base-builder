# Process templates

Fill these in for the person. Plain words. No jargon without one sentence of explanation.

## RUN-ME.md (only for steps the person did not let you do)
For each step you could not do, write:
1. **What this step does** (one sentence).
2. **The command** (one command per box, ready to copy and paste), and the folder to run it in.
3. **What you should see** if it worked.
4. **If it did not work:** the two most likely causes and what to try. Then "tell your AI what you saw".

Typical steps: install Node 22.12 or newer (https://nodejs.org) and git; run `python3 scripts/generate_kb.py --spec spec.json --out <new empty folder> --logo <image>`; in the new folder run `npm ci`, `npm run check`, `npm test`, `npm run dev`; open `http://localhost:3000` (use `localhost`, not `127.0.0.1`) and log in with `SITE_PASSWORD` from `.env`.

## PROCESS.md (always written, goes in the site folder)
- **Start and stop:** the exact commands, and the address to open.
- **Password:** where it is (`.env`, `SITE_PASSWORD`) and how to change it. It is one shared password, not individual accounts.
- **Add a page:** copy a file in `content/docs/<section>/`, change the frontmatter and text, run `npm test`.
- **Add a person:** copy a file in `content/employees/`, change it, add `public/avatars/<slug>.svg` (or the test will fail).
- **Back up:** copy the whole folder (without `node_modules`).
- **Owners:** which person owns which section.
- **TODO pages:** the list, so nobody mistakes an empty page for a finished one.
- **Not set up:** hosting (it runs only on this computer), editing in Sanity, the chat panel (needs the owner's own OpenAI key).
- **Keep it private** unless the template's author allows otherwise; never put secrets or other people's personal data in the pages.
