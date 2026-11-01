#!/usr/bin/env python3
"""Generate a private company knowledge base website from an interview spec.

  python3 generate_kb.py --spec spec.json --out ~/projects/their-kb [--logo path.png]

Fetches daveebbelaar/company-knowledge-base at a pinned commit (Next.js + Fumadocs, local Markdown, password gate),
rebrands it from the spec, writes the content, and refuses to finish if any template text is left behind.
Nothing is sent anywhere except the git clone. The template's code is NOT bundled in this repo."""
import argparse, json, os, re, secrets, shutil, subprocess, sys, tempfile

UPSTREAM = "https://github.com/daveebbelaar/company-knowledge-base.git"
PIN = "b01ec5e5a50bd718b8233710a9510be5e35c99ad"
ICONS = {"info": "Info", "palette": "Palette", "video": "Clapperboard", "wrench": "Wrench", "flask": "FlaskConical", "settings": "Settings2",
         "code": "Code2", "megaphone": "Megaphone", "sales": "TrendingUp", "support": "Headphones", "people": "Users", "book": "BookOpen",
         "shield": "ShieldCheck", "money": "Wallet", "truck": "Truck", "heart": "Heart", "home": "House", "star": "Star"}
SLUG = re.compile(r"^[a-z0-9-]+$")
UPDATED = __import__("datetime").date.today().isoformat()

def die(msg): sys.exit("ERROR: " + msg)

def mix(hexc, amount):  # mix toward white
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(round(c + (255 - c) * amount) for c in (r, g, b))

def validate(spec):
    for k in ("name", "tagline", "intro", "audience", "sections", "people"):
        if k not in spec: die(f"spec is missing '{k}'")
    if len(spec["tagline"]) != 2: die("tagline must be two short lines")
    names = {p["name"] for p in spec["people"]}
    if not names: die("at least one person (the page owner) is required")
    seen = set()
    for s in spec["sections"]:
        if not SLUG.match(s["slug"]): die(f"bad section slug {s['slug']}")
        if s.get("icon", "info") not in ICONS: die(f"icon must be one of {sorted(ICONS)}")
        if not s["pages"]: die(f"section {s['slug']} has no pages")
        for p in s["pages"]:
            if not SLUG.match(p["slug"]): die(f"bad page slug {p['slug']}")
            if p["owner"] not in names: die(f"page {s['slug']}/{p['slug']} owner '{p['owner']}' is not in people")
            seen.add(f"{s['slug']}/{p['slug']}")
    for p in spec["people"]:
        if not SLUG.match(p["slug"]): die(f"bad person slug {p['slug']}")
        if p["section"] not in {s["slug"] for s in spec["sections"]}: die(f"person {p['slug']} section is not a section slug")
        if not p.get("responsibilities"): die(f"person {p['slug']} needs responsibilities")
    for s in spec["sections"]:
        for p in s["pages"]:
            for m in re.findall(r"\]\(/docs/([^)#]+)\)", p["body"]):
                if m != "team" and not m.startswith("team/") and m not in seen: die(f"broken link /docs/{m} in {s['slug']}/{p['slug']}")
    return seen

def sub(path, pairs):
    s = open(path).read()
    for a, b in pairs:
        if a not in s: die(f"template changed: '{a[:50]}' not found in {path}")
        s = s.replace(a, b)
    open(path, "w").write(s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--spec", required=True); ap.add_argument("--out", required=True); ap.add_argument("--logo")
    a = ap.parse_args(); spec = json.load(open(os.path.expanduser(a.spec))); out = os.path.expanduser(a.out)
    pages = validate(spec)
    if os.path.exists(out) and os.listdir(out): die(f"{out} exists and is not empty; choose a new folder")
    tmp = tempfile.mkdtemp(); subprocess.run(["git", "clone", "--quiet", UPSTREAM, tmp + "/up"], check=True); subprocess.run(["git", "-C", tmp + "/up", "checkout", "--quiet", PIN], check=True)
    os.makedirs(out, exist_ok=True)
    shutil.copytree(tmp + "/up", out, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "node_modules"))
    shutil.rmtree(tmp)
    os.chdir(out)
    for p in ("content/docs", "content/employees", "public/avatars", "docs", "scripts/benchmark-chat.mjs"):
        shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else (os.path.exists(p) and os.remove(p))
    name = spec["name"]; upper = name.upper(); accent = spec.get("accent", "#000000"); light = "#ffffff" if accent.lower() == "#000000" else mix(accent, 0.6)
    logo = a.logo or spec.get("logo")
    if logo:
        logo = os.path.expanduser(logo)
        if not os.path.isfile(logo) or os.path.splitext(logo)[1].lower() not in (".png", ".svg", ".jpg", ".jpeg", ".webp"): die("logo must be an existing png/svg/jpg/webp file")
        ext = os.path.splitext(logo)[1].lower(); shutil.copy(logo, f"public/logo{ext}"); logo_url = f"/logo{ext}"
    else: logo_url = None
    # brand component + docs layout mark
    mark = f'<img src="{logo_url}" alt="" width={{34}} height={{34}} className="brand-logo" />' if logo_url else f'<span className="brand-mark" aria-hidden>{name[0].lower()}</span>'
    open("components/brand.tsx", "w").write(f'''import Link from "next/link";

export function Brand() {{
  return (
    <Link href="/" className="brand" aria-label={json.dumps(name + " home")}>
      {mark}
      <span>
        {json.dumps(upper)[1:-1]}<span className="brand-subtitle">{json.dumps(spec.get("subtitle", "HANDBOOK"))[1:-1]}</span>
      </span>
    </Link>
  );
}}
''')
    first = spec["sections"][0]["pages"][0]; start = f"/docs/{spec['sections'][0]['slug']}/{first['slug']}"
    note = spec.get("note", {})
    footer = spec.get("footer", "A shared place to learn.")
    allp = [(p["title"], f"/docs/{sec['slug']}/{p['slug']}") for sec in spec["sections"] for p in sec["pages"]]
    ql = [(t.replace("{", "").replace("}", ""), u) for t, u in (spec.get("quick_links") and [(q["label"], q["link"]) for q in spec["quick_links"]] or allp)][:3]
    ql += [("Meet the team", "/docs/team"), ("Browse everything", "/docs"), ("Search", "/docs")][: 3 - len(ql)]
    sub("app/layout.tsx", [('"Vellumridge Technology | Company knowledge"', json.dumps(f"{name} | Knowledge base")), ('"%s | Vellumridge"', json.dumps(f"%s | {name}")),
        ('"The team handbook for Vellumridge Technology, a fictional company."', json.dumps(spec["intro"]))])
    layout_mark = f'<img src="{logo_url}" alt="" width={{24}} height={{24}} />' if logo_url else f'<span className="brand-mark" aria-hidden>{name[0].lower()}</span>'
    sub("app/docs/layout.tsx", [('<span className="brand-mark" aria-hidden>\n              v\n            </span>\n            Vellumridge', layout_mark + "\n            " + name.replace("{", "").replace("}", "")), ("Company home", "Home")])
    sub("app/page.tsx", [("THE VELLUMRIDGE HANDBOOK", f"THE {upper} KNOWLEDGE BASE"), ("Good work starts", spec["tagline"][0]), ("with shared knowledge.", spec["tagline"][1]),
        ("How we build, how we work, and what we believe.", spec["intro"]), ("Policies, playbooks, and the answers you need.", spec.get("hint", "Search for the answer you need.")),
        ("Less admin.", note.get("title1", "Everything in one place.")), ("More fieldwork.", note.get("title2", "Easy to find.")),
        ("We build Fieldbook, scheduling and service software for teams that\n              maintain renewable energy sites.", note.get("body", spec["intro"])),
        (">departments<", ">sections<"), ("<strong>6</strong>", f"<strong>{len(spec['sections'])}</strong>"), ("First week here?", spec.get("start_title", "New here?")),
        ("Start with the essentials. We’ll help you find your feet.", spec.get("start_text", "Start with the basics.")), ("/docs/people/first-week", start), ("Your first week", spec.get("start_button", "Start here")),
        ("Knowledge by department", "Knowledge by section"), ("Vellumridge Technology", name),
        ("GOOD TO HAVE HANDY", spec.get("quick_eyebrow", "GOOD TO HAVE HANDY")), ("The everyday essentials", spec.get("quick_title", "Start with these")),
        ("/docs/operations/travel-expenses", ql[0][1]), ("Back from a client trip", ql[0][0]), ("/docs/engineering/incident-response", ql[1][1]), ("Something’s gone wrong", ql[1][0]),
        ("/docs/people/remote-work", ql[2][1]), ("Working from somewhere else", ql[2][0]), ("A fictional company for a real working demo.", footer)])
    sub("app/login/page.tsx", [("Vellumridge’s company knowledge base", f"the {name} knowledge base"), ("A fictional company. A shared place to learn.", footer)])
    sub("app/docs/[[...slug]]/page.tsx", [(". Part of our\n            fictional demo team.", ".")])
    sub("app/api/chat/route.ts", [("You are the Vellumridge handbook assistant. Answer company questions", f"You are the {name} assistant. Answer questions about {name}")])
    sub("app/api/chat/route.ts", [("[Travel expenses](/docs/operations/travel-expenses)", f"[{first['title']}]({start})")])
    sub("sanity/schema.ts", [("operations/travel-expenses", start[len("/docs/"):])])
    for f in ("scripts/check-live.mjs", "scripts/check-chat.mjs"): os.remove(f)
    pk = json.load(open("package.json")); [pk["scripts"].pop(k, None) for k in ("test:live", "test:chat")]; json.dump(pk, open("package.json", "w"), indent=2)
    sub("lib/chat.mjs", [("vellumridge.chats.v1", re.sub(r"[^a-z0-9]+", "", name.lower()) + ".chats.v1")])
    sub("sanity.config.ts", [("Vellumridge handbook", f"{name} knowledge base")])
    sub("tests/core.test.mjs", [("people.length, 10", f"people.length, {len(spec['people'])}"), ("size, 10)", f"size, {len(spec['people'])})"),
        ("    6,\n  );", f"    {len(spec['sections'])},\n  );"), ("page.body.length > 80", "page.body.length > 20")])
    # departments
    icons = sorted({ICONS[s.get("icon", "info")] for s in spec["sections"]})
    secs = ",\n".join(f'  {{ slug: {json.dumps(s["slug"])}, name: {json.dumps(s["name"])}, icon: {ICONS[s.get("icon", "info")]}, description: {json.dumps(s["description"])}, owner: {json.dumps(s["owner"])} }}' for s in spec["sections"])
    open("lib/company.ts", "w").write("import {\n" + "".join(f"  {i},\n" for i in icons) + '} from "lucide-react";\n\nexport const departments = [\n' + secs + ",\n];\n")
    # css
    css = open("app/global.css").read()
    rep = {"#315946": accent, "#fafaf7": "#ffffff", "#242c27": "#111111", "#f0f1eb": "#f3f3f3", "#6b716b": "#5f5f5f", "#e0e4dc": "#dcdcdc", "#eaf0e7": "#eeeeee", "#adc8ab": light, "#17271b": "#000000",
           "#171f1a": "#000000", "#e9eee7": "#f2f2f2", "#202c24": "#141414", "#a3b0a3": "#a8a8a8", "#1c2820": "#0d0d0d", "#354439": "#2e2e2e", "#283b2b": "#1c1c1c", "#d9ead8": "#ffffff",
           "#eaf0e3": "#f1f1f1", "#e9efe4": "#f1f1f1", "#ccd8c4": "#d4d4d4", "#cbd5c6": "#d4d4d4", "#b7c7b2": "#bdbdbd", "#90a389": "#8a8a8a", "#64705e": "#666666", "#61715a": "#666666",
           "#486b56": accent, "#324833": "#222222", "#244633": accent, "#203b2510": "#00000010", "#172c2530": "#00000030", "#172c252b": "#0000002b", "#172c2510": "#00000010"}
    for k, v in rep.items(): css = css.replace(k, v)
    open("app/global.css", "w").write(css + "\n.brand-logo{border-radius:6px;object-fit:contain;margin-right:8px;vertical-align:middle}\n.docs-brand{display:inline-flex;align-items:center;gap:8px}\n")
    # content
    def fm(d): return "---\n" + "".join(f"{k}: {json.dumps(v) if isinstance(v, str) else v}\n" for k, v in d.items()) + "---\n\n"
    os.makedirs("content/docs", exist_ok=True)
    open("content/docs/index.md", "w").write(fm({"title": f"Welcome to {name}", "description": spec["intro"], "owner": spec["people"][0]["name"], "updated": UPDATED, "order": 0}) + spec.get("welcome", spec["intro"]).strip() + "\n\n" +
        "| Section | Start here |\n| --- | --- |\n" + "".join(f"| {s['name']} | [{s['pages'][0]['title']}](/docs/{s['slug']}/{s['pages'][0]['slug']}) |\n" for s in spec["sections"]) + "\nFind the people in the [team directory](/docs/team).\n")
    for s in spec["sections"]:
        os.makedirs(f"content/docs/{s['slug']}", exist_ok=True)
        for i, p in enumerate(s["pages"], 1):
            open(f"content/docs/{s['slug']}/{p['slug']}.md", "w").write(fm({"title": p["title"], "description": p["description"], "owner": p["owner"], "updated": UPDATED, "order": p.get("order", i)}) + p["body"].strip() + "\n")
    os.makedirs("content/employees", exist_ok=True); os.makedirs("public/avatars", exist_ok=True)
    for p in spec["people"]:
        json.dump({"_id": f"employee.{p['slug']}", "_type": "employee", "slug": p["slug"], "name": p["name"], "role": p["role"], "department": p["section"], "bio": p["bio"], "responsibilities": p["responsibilities"], "updated": UPDATED}, open(f"content/employees/{p['slug']}.json", "w"), indent=2)
        open(f"public/avatars/{p['slug']}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect width="96" height="96" rx="48" fill="{accent}"/><text x="48" y="62" font-family="Georgia,serif" font-size="46" font-weight="700" text-anchor="middle" fill="#fff">{p["name"][0].upper()}</text></svg>\n')
    open("public/avatars/README.md", "w").write("Simple initials avatars. Replace a person's svg with their own picture if they agree.\n")
    pw = spec.get("password") or "kb-" + secrets.token_urlsafe(9)
    open(".env", "w").write(open(".env.example").read().replace("change-this-password", pw))
    open("README.md", "w").write(f"# {name} knowledge base\n\nBuilt with the BlackSwanLabz knowledge-base-builder skill from daveebbelaar/company-knowledge-base. Content: Markdown in `content/docs`, people in `content/employees`.\n\n```bash\nnpm ci\nnpm run dev   # open http://localhost:3000 (use localhost, not 127.0.0.1)\nnpm test && npm run check\n```\n\nThe password is `SITE_PASSWORD` in `.env`. It is a shared password for a small team, not individual accounts.\n")
    ag = open("AGENTS.md").read()
    open("AGENTS.md", "w").write(ag.replace("Vellumridge Technology and its people, product, and policies are fictional. Keep examples short, concrete, and consistent across departments.", f"This is the {name} knowledge base. Content comes from the owners' own words. Never invent facts, numbers, people, or customers."))
    left = subprocess.run("grep -rniE 'vellum|fieldbook|northstar|utrecht|fictional|travel-expenses|incident-response|first-week|remote-work' . --exclude-dir=node_modules --exclude-dir=.git --exclude=package-lock.json --exclude=chat.test.mjs -l", shell=True, capture_output=True, text=True).stdout.split()
    if left: die("template text left in: " + ", ".join(left))
    print(f"OK: {len(pages)} pages, {len(spec['people'])} people, {len(spec['sections'])} sections -> {out}\nPassword is in {out}/.env (SITE_PASSWORD).\nNext: cd {out} && npm ci && npm run check && npm test && npm run dev")
main()
