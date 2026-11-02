# Moving the web version to astrovarium.com

Astrovarium session, 3 Nov 2026. Dafa bought astrovarium.com and astrovarium.app at Cloudflare
Registrar on 3 Nov (from _HQ). Nothing below is done until Dafa says so.

## The trap

Everything a web user has lives in the browser's storage for one origin: their saved charts
(`astrarium_charts`), the access key (`astrarium_access`), settings, all under `astrarium_*`.
`dafaspace.github.io` and `astrovarium.com` are different origins, so a plain redirect leaves every
saved chart behind, out of reach.

And the plain redirect is what GitHub does by itself: give the `astrotrip` repo a custom domain and
GitHub sends `dafaspace.github.io/astrotrip/*` to the new domain with a 301. The old page never
loads again, so nothing can read the old storage. The Android APK and the iOS build are not
affected: their storage lives inside the app.

## The plan

1. **Rename the code repo** `dafaspace/astrotrip` to `dafaspace/astrovarium`, with GitHub Pages on
   the custom domain `astrovarium.com` (a `CNAME` file in the repo). The local folder is already
   `AstroVarium`; `git remote set-url` follows.
2. **A new small repo under the old name, `dafaspace/astrotrip`,** keeps
   `dafaspace.github.io/astrotrip/` alive as a bridge. It holds three files:
   - `index.html`: reads every `astrarium_*` key, packs them into the URL fragment and opens
     `https://astrovarium.com/#move=<data>`. The fragment never reaches any server. With no saved
     data it goes straight to the new address. Its page also says in one line that the app moved,
     with a link, for the case when scripts are off.
   - `sw.js` under the same name as the old one: the installed service worker finds it, updates,
     clears the old caches and stops serving the old app. Without it an installed copy would keep
     showing the old version from its cache.
   - `manifest.json` with the same `start_url`, so an installed home-screen shortcut opens the
     bridge and from there the new address.
3. **The app on the new domain** reads `#move=` once on start: it writes keys that are missing,
   never overwrites ones already there, removes the fragment from the address bar and says
   "Charts moved: N". The CSV export button stays as a second way out.
4. **astrovarium.app** redirects to astrovarium.com with a Cloudflare Redirect Rule, keeping the
   path. One main address, so one storage.
5. **DNS at Cloudflare:** the four GitHub Pages A records and `www` CNAME to
   `dafaspace.github.io`, proxied, SSL mode "Full" set by hand (root CLAUDE.md, Domains). Written
   into `_HQ/DOMAINS.md` and `SITES` in `_portfolio/check-sites.mjs` the day it serves.
6. **Then the links:** dafaspace.com card, the store listing's support and privacy URLs, the
   letters, ACCESS-KEYS.md (key links are built on the site address; old links keep working through
   the bridge, which carries the `#key=` on).

## What is checked before the switch

- In the Browser pane: a profile with saved charts and a key on the old address, opened after the
  switch, lands on the new one with the same charts, the same key and the same settings.
- An installed PWA (Chrome desktop) opens the bridge and arrives.
- The old key link `dafaspace.github.io/astrotrip/#key=...` still opens access.

## Said plainly

- On iPhone a home-screen shortcut opens the bridge, but the new address opens in Safari rather than
  as the installed app. The tester has to add the new one to the home screen once. Charts still
  move.
- A URL can carry a few megabytes; a thousand saved charts fit. Past that the bridge falls back to
  "export CSV here, import there".
