# jobready — "This is not a CV." (Remotion video)

A 33-second vertical (1080×1920, 30fps) Remotion video for **jobready.za** that
walks through *why a South African CV should not carry ID number, race, religion,
marital status, dependants or home address* — and what a clean CV looks like
instead.

## Scenes

| # | Frames | Scene |
|---|--------|-------|
| 1 | 0–134 | A CV full of sensitive fields. Toast: **"This is not a CV."** |
| 2 | 135–344 | WhatsApp chat — recruiter asks for CV + certified ID + proof of address. |
| 3 | 345–554 | The sensitive lines get slammed with black redaction bars. **"Real job. Asks later."** |
| 4 | 555–764 | The same person's *clean* CV (skills, experience, contact — no ID/race/etc.). |
| 5 | 765–989 | Payoff checklist + **jobready.za** sign-off. |

## Code layout

- `src/JobReadyVideo.tsx` — the whole composition (all five scenes).
- `src/Root.tsx` / `src/index.ts` — Remotion entry + composition registration.
- `remotion.config.ts` — points Remotion at the local headless Chromium.
- `scripts/prepare-chromium.mjs` — unpacks the bundled Chromium + its NSS libs.
- `render.sh` — one command render.

## Rendering

This workspace's sandbox can only reach **npm / GitHub / PyPI**, so Remotion
cannot download its usual headless browser. Instead we render with the
**`@sparticuz/chromium`** npm package (a serverless Chromium build):

```bash
cd jobready
npm install
npm run render            # -> out/JobReadyVideo.mp4
```

`render.sh` unpacks the browser (idempotent), sets
`LD_LIBRARY_PATH`/`CHROMIUM_LIB_DIR` for its bundled NSS libraries, and runs:

```
npx remotion render JobReadyVideo out/JobReadyVideo.mp4 --chrome-mode=chrome-for-testing
```

The `--chrome-mode=chrome-for-testing` flag makes Remotion use `--headless=new`
(the old `headless-shell` mode no longer exists in this Chromium).

On a normal machine with Chrome installed, plain `npx remotion render
JobReadyVideo out/JobReadyVideo.mp4` also works — the sandbox setup is only
needed here because browser downloads are blocked.

## Notable fix

The original snippet's styled components were named `iPhoneScreen` and
`iOSToast`. Because those identifiers start with a **lowercase letter**,
esbuild's JSX transform treats `<iPhoneScreen />` as a native HTML tag
(`<iphonescreen>`) rather than a React component, so none of their styles are
applied (the screen collapses to content width and loses its background).
They are renamed `PhoneScreen` and `Toast` here.
