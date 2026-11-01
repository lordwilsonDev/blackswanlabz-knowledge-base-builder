# BlackSwanLabz knowledge-base builder

Free. A skill that lets an AI (Claude, Codex, or any model that can read files and run Python and Node) build a private company knowledge base for someone else.

**It asks first:** who it is for, what it must answer, what content and images they have, name and colors, sections, people, access. It says the specs back, waits for a yes, then builds the site, runs the tests, and checks the screens.

## Use it
Point your AI at this repo and say: "Follow knowledge-base-builder/SKILL.md and build my knowledge base." Or install the `knowledge-base-builder` folder as a skill.

## What is real, what is not
- **Tested:** the generator was run on an example spec; the site installed, passed its type check and tests, started, and the login page loaded. Pages were not read for accuracy; that is the owner's job.
- **Not included:** hosting, individual accounts (it has one shared password), editing in Sanity, and the chat panel (needs an OpenAI key you provide).
- **Template:** the site is fetched at build time from [daveebbelaar/company-knowledge-base](https://github.com/daveebbelaar/company-knowledge-base) (pinned commit). That repo had no license file when this was written, so its code is not bundled here and sites built from it should stay private unless its owner says otherwise.
- **Honesty rule:** the skill never invents content. Empty pages are marked TODO.

Code in this repo: MIT (see LICENSE). From BlackSwanLabz. Free first.
