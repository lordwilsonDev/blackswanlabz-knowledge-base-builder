# BlackSwanLabz knowledge-base builder

Free. A skill that lets an AI (Claude, Codex, or any model that can read files and run Python and Node) build a private company knowledge base for someone else.

**It asks first:** who it is for, what it must answer, what content and images they have, name and colors, sections, people, access. It says the specs back, waits for a yes, then builds the site, runs the tests, and checks the screens.

## What you need to do
1. **Have an AI that can work with files.** Claude Code, Codex, or another model that can read files, run Python and Node, and talk with you. (No such AI? Ask any chat AI to follow the skill and give you the steps; it will write them for you in plain words.)
2. **Point it here** and say: "Follow knowledge-base-builder/SKILL.md and build my knowledge base."
3. **Decide what it may do.** It asks first, one by one: create files in one new folder; run commands (git, python3, node, npm; these download the template and packages from the internet); start the site and look at it in a browser; read documents you point to. You can say yes, some, or none.
4. **Answer the interview:** who it is for, what it must answer, what you already have, the name, your logo, colors, sections, people, who may open it. Anything you want added, add it. It never answers for you.
5. **Check the specs it reads back** and say yes. Nothing is built before that.
6. **Check the result.** It gives you a folder, a password, a `PROCESS.md` (how to start, add pages, back up) and a list of TODO pages. If you did not allow commands, it writes `RUN-ME.md` with exact steps for you to copy and paste.

**On your computer you need** (only if you run it yourself): Node 22.12 or newer, git, and Python 3.

**The model builds the process for you.** If you grant everything, it does everything. If you grant less, it does what you allowed and writes the rest as plain steps for you. You can change your mind, add anything, or take permissions away at any time.

## Use it
Point your AI at this repo and say: "Follow knowledge-base-builder/SKILL.md and build my knowledge base." Or install the `knowledge-base-builder` folder as a skill.

## What is real, what is not
- **Tested:** the generator was run on an example spec; the site installed, passed its type check and tests, started, and the login page loaded. Pages were not read for accuracy; that is the owner's job.
- **Not included:** hosting, individual accounts (it has one shared password), editing in Sanity, and the chat panel (needs an OpenAI key you provide).
- **Template:** the site is fetched at build time from [daveebbelaar/company-knowledge-base](https://github.com/daveebbelaar/company-knowledge-base) (pinned commit). That repo had no license file when this was written, so its code is not bundled here and sites built from it should stay private unless its owner says otherwise.
- **Honesty rule:** the skill never invents content. Empty pages are marked TODO.

Code in this repo: MIT (see LICENSE). From BlackSwanLabz. Free first.
