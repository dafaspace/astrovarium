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

## _HQ's four checks (3 Nov), and where each stands

1. **iPhone home-screen shortcut: open, the deciding test.** WebKit gives a home-screen web app
   storage of its own, apart from Safari. So the chain old shortcut, bridge, new site may import
   the charts into Safari's storage, and a new shortcut added afterwards may start empty. Until a
   test says otherwise the bridge assumes the worst on iOS: when it runs as a home-screen app
   (`navigator.standalone`) it does not redirect on its own. It shows "Save your charts as a file"
   first, then "Open the new address", and the new site, opened empty from a new shortcut, offers
   "Import charts from a file" on its first screen.
   The test, start to end, with a real library:
   - first in the iOS Simulator, with the bridge and the app served locally on two different
     origins, before anything is pushed (session);
   - then on a real iPhone (Dafa): old shortcut, bridge, new site, new shortcut. Are the charts
     there?
   The result goes here, and the verdict goes to Dafa with the plan.

   **Simulator result, 3 Nov 2026** (iPhone 17 Pro, iOS 26.5; the old site and the bridge on
   127.0.0.1:3112/astrotrip/, the new app on localhost:3111; 1019 charts with notes):
   - The old shortcut opens the bridge in place of the app: the old service worker fetches the
     page network-first. The bridge sees 1019 charts.
   - "Open" opens the new address in a view inside the old shortcut. The charts, the language
     and the theme arrive, but in **the old shortcut's storage**. Safari at the same address is
     empty.
   - A new shortcut opens **empty**: added from Safari, or from the share sheet of that view.
     _HQ's worry was right.
   - **The file works end to end.** "Save charts as a file" in the old shortcut gives the share
     sheet with `astrovarium-charts-<date>.csv` (109 KB) and Save to Files. In the new
     shortcut, Library > Import CSV > the file: "Charts imported: 1019", notes included.
   - So on an iPhone shortcut the bridge leads with the file: it is the main button, and the
     text says what to do. The first empty start of the new shortcut offers the import once.
     That offer was not seen in the simulator, because the shortcut served its cached page; it
     is to be checked on the device. The CSV does not carry the settings or the key. The key
     link opens on the new address.
   - **Desktop and Android** (Browser pane, which runs Chrome): the automatic path works. 1019
     charts, notes, settings and the key arrive. Nothing is doubled when the bridge is used
     twice. The `#key=` link is carried on. The address ends clean.
   - Not testable in the Browser pane: the service-worker swap. The pane does not register
     service workers. In the simulator the old shortcut did reach the bridge.
   - Still for a real iPhone (Dafa): the same chain, plus the import offer.
2. **Size: measured, it fits.** The 1019-chart test library (`test-sample.json`) is 105 KB of
   JSON, which comes to 186 KB as a plain URL fragment and 30 KB once compressed with
   deflate-raw and base64url. The bridge compresses with `CompressionStream('deflate-raw')`
   (Safari 16.4+, Chrome 80+), and a browser without it is sent to the file path. 30 KB is far
   inside what Chrome (2 MB) and Safari accept. Still to check: a real saved library with its
   notes, which carries more fields per chart than the test sample. After the import
   `history.replaceState` clears the fragment, so birth data does not stay in the history.
3. **A way back: in the plan.** Before redirecting, the bridge offers "Save your charts as a file",
   using the CSV export the app already has (`libToCsv`). The new site takes the same file
   (`importCsvText`). Settings and the key are carried by the fragment. The key link from
   `ACCESS-KEYS.md` also works on the new address, so if the fragment fails the key does not.
4. **The bridge stays at least a year: agreed.** It is three static files at no cost. Review it no
   earlier than Nov 2027, and only once the old address gets no visits.

## Said plainly

- On iPhone a home-screen shortcut opens the bridge, but the new address opens in Safari rather than
  as the installed app. The tester has to add the new one to the home screen once. Charts still
  move.
- A URL can carry a few megabytes; a thousand saved charts fit. Past that the bridge falls back to
  "export CSV here, import there".
