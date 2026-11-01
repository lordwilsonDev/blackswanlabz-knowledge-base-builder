---
name: knowledge-base-builder
description: Interview someone about the knowledge base they want, then build it as a private website. Use when a person or business wants a company handbook, team wiki, "second brain", help center or FAQ site, or says "build my knowledge base". Asks who it is for, what it must answer, what content and images they have, then generates and checks the site.
---

# Knowledge base builder

You build a small private knowledge-base website for someone else. You ask first, build second. Works with any AI model that can read files, run Python/Node, and talk with the person.

## Rules
1. Ask the questions in `references/questions.md`, in order. One at a time. If the tool limits you to four options, print a lettered list and let them answer with letters or words. Never answer for the person.
2. Use only what they tell you or give you. Never invent facts, numbers, people, customers, prices, policies or quotes. If a page has nothing real to say yet, write a short page that says what it will hold and who owns it, marked TODO. Do not fill it with made-up content.
3. Say back the specs (section 4 of the questions) and wait for a clear yes before you build.
4. Keep it private. Do not upload their content, logo or answers anywhere. Do not put passwords, API keys, personal data, or anything they call confidential into the pages. Do not publish or deploy. Ask before any outward action.
5. Images: use only files they give you or tell you to use, and only if they have the right to use them. Do not download a logo from the web for them.
6. Be plain and kind. No jargon. Tell them what you could not check.

## Permissions: the person decides, you build the process around the answer
Before anything else, ask what you may do. Ask each one separately, in plain words, and let them say yes to all, some, or none:
- **Files:** create files in one new folder they choose.
- **Commands:** run `git`, `python3`, `node` and `npm` in that folder (git and npm download the template and its packages from the internet).
- **Look:** start the site on their own computer and open it in a browser to check it.
- **Read:** read documents they point you to (only those; ask before reading anything else).

You are the project manager, not only the builder. You build the process for this person, shaped by what they allowed:
- **Every permission given:** do all the steps yourself.
- **Some or none given:** do not do the denied step. Write that step for them in `RUN-ME.md` (from `references/process-template.md`): exact commands to copy and paste, what each one does in one plain sentence, what they should see when it works, and what to do if it does not. Then wait for them to tell you the result and continue from there.
- They may change their mind at any time. Ask again before using a permission they did not give.
- They can add anything they want at any time: sections, pages, people, documents, images, rules. Add it; do not argue it down. If something is risky (confidential data, a claim you cannot check), say so once, plainly, and let them decide.

## Steps
0. Permissions (above). Write down what was granted in `SPECS.md`.
1. Interview (`references/questions.md`).
2. Write `spec.json` in the format of `references/spec-format.md` (see `examples/example-spec.json`). Write `SPECS.md` next to it: the answers in their own words, so they can change their mind later.
3. Confirm the specs with them.
4. Run `python3 scripts/generate_kb.py --spec spec.json --out <new empty folder> [--logo <image>]`. It needs git and network once, to fetch the template.
5. In the new folder run `npm ci`, `npm run check`, `npm test`. All must pass. Fix the spec and regenerate if not.
6. Run `npm run dev`, open it at `http://localhost:3000` (use `localhost`, not `127.0.0.1`), log in with `SITE_PASSWORD` from `.env`, and check the home page, one docs page, and search. Look at it; do not only trust the tests.
7. Write `PROCESS.md` in the site folder for the owner (from `references/process-template.md`): how to start and stop it, where the password is, how to add a page or a person, how to back it up, who owns what, what is TODO, what is not set up.
8. Report: where the folder is, how to start it, where the password is, which pages are TODO, and what is not set up (editing in Sanity, the chat panel needs an OpenAI key, hosting).

## Changing it later
Pages are Markdown files in `content/docs/<section>/<page>.md`; people are JSON files in `content/employees/`. Edit or add them directly (keep the frontmatter: title, description, owner, updated, order). `generate_kb.py` refuses a non-empty folder, so for big changes write a new `spec.json` and generate into a new folder. After any change run `npm test` and `npm run check`.

## Done when
The site starts, the tests and type check pass, you looked at three screens, and the person has the list of TODO pages.

## Limits
Not a licensed advisor. A shared password protects the site; it is not individual accounts. The template comes from daveebbelaar/company-knowledge-base, which had no license file when this was written: keep sites built from it private unless its owner says otherwise.
