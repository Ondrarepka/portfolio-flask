---
title: Ledger - TTRPG campaign manager
category: design
blurb: Multi-genre-system Storytelling tool.
image: /static/uploads/hub.webp
featured: true
---
## Building Ledger — a campaign keeper where the point is what it doesn't show you
 
I run tabletop campaigns — nWoD mostly — and every campaign tool I've used had the same problem, which by now shouldn't surprise anyone who's read this far: the Storyteller's secrets and what the players actually see were the same document, just with some divs hidden by CSS. Open devtools once and the whole campaign sits right there in the page source, GM notes and all. Fine for a solo notebook. Not fine for a table of five people who actually respected the "no metagaming" rule at session zero.
 
So the rule for Ledger, from day one, was simple to say and annoyingly hard to build: a player can never receive something they're not meant to see. Not "the UI hides it." Not "well, they'd have to know where to look." Never receive it — full stop, the server just doesn't send it.
 
I'm building it with Claude Code.
 
## Architecture first, features later
 
We didn't start with a page builder or a nice compendium view. We started with the redaction boundary — every piece of content in a chronicle gets computed into two versions, Storyteller and Player, built server-side and cached separately. Pages, individual fields, even inline `:::gm` blocks tucked into a paragraph of prose that can get revealed mid-session and hidden again after. Nothing past that boundary got to be "we'll figure it out later" — that was the actual rule on the roadmap, in writing, and we stuck to it. Auth, tenancy, the whole redaction model — settled and documented before a single compendium card ever rendered.
 
That paid off, mostly. Months in, doing a full pass over every route that ships anything player-visible — reading it independently, not trusting the code that had just written itself — we found one real leak: editing your own character page returned the fully unredacted row, GM-only fields included, because the edit form needed raw markdown and nobody had built a redacted version of "give me the source, not the rendered thing." My own PC's secret backstory field. Sitting there. Readable the whole time. Small fix once we found it — a source-level redactor next to the existing one, both driven off the same "is this hidden" check so they can't drift apart — but finding it took actually looking, not "the tests are green, must be fine."
 
## Verification, or: don't trust the mocks
 
Nothing shipped without running against a real Postgres and Redis — spun up, migrated, seeded, torn down, every single time, a disposable clone of prod. Not because I don't trust tests, just because "the mocks pass" and "it works" turned out to be two different sentences more than once. A markdown table feature that looked fine on my machine left GM players staring at raw pipe characters for a day, because a cache key didn't account for the parser itself changing. An export that handled a three-page test chronicle fine brought the whole server down on a real 300-page campaign, because it turned out to be opening one DB transaction per page. You don't catch that reading a diff. You catch it by actually running the thing against something real.
 
## What it turned into
 
Systemless — the Storyteller defines their own schema, and Ledger renders whatever they build. Ten field types and counting. Two calendars, because "when we played it" and "when it happened in the story" are two different timelines, and every tool I've used quietly pretends they're the same one. A relationship graph that draws itself from links you were already writing anyway. 2FA, Stripe billing that won't nuke your data the moment a payment lapses, an admin console, and an AI-import guide you can hand to your own assistant.
 
It's live. It's mine. It's running on hardware sitting in my own apartment, and that last part still makes me laugh a little :D
 
## What's next for Ledger
 
What's next for Ledger? Huge things, honestly. System-specific support is the big one — starting with nWoD, since that's what I actually run, then probably something more mainstream like D&D 5e, and Call of Cthulhu, or rather the Universal Roleplaying System, since it's the same folks behind Call of Cthulhu — and they just put out rulebooks for Rivers of London, with Ben Aaronovitch actually involved in writing them, which, come on, that's just cool.
 
Beyond systems: some kind of social feature would be nice, or at least a marketplace/preview of chronicle schemas other people have already built, so nobody's starting from a blank page. And campaign settings in general could use a ton more features — that part's honestly still thin.
 
Stick around and find out :) Go try it yourself — one campaign's free. And hit me with ideas on what to build next :) [Ledger](https://ledger.repizz.org/)

Finally a gallery

![Compendium](/static/uploads/compendium.webp)
![Page from GM's perspective](/static/uploads/page-gm.webp)
![Page from Players's perspective](/static/uploads/page-player.webp)
![HUB](/static/uploads/hub.webp)
![Graph](/static/uploads/graph.webp)
