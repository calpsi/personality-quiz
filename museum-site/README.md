# The Quiet Collection

Mobile-first playable museum prototype, using the existing Blender scene and Hunyuan Abraham. Source copy is imported from the edited Word master; that document is not modified.

## Run locally

With Node 22+ and npm installed: `npm install`, then `npm run dev`.
This workspace also has a local npm installation under `.sites-runtime/bin` and a bundled Node runtime used by Codex.

## Existing API key

Run `python3 scripts/set-api-key.py` in Terminal. It asks for confirmation of the local `.env.local` destination, then accepts the key through hidden input. Restart the development server afterward. The key is never sent to the frontend or included in Git. Optional `OPENAI_MODEL` defaults to `gpt-6-luna`; use a model available to your API project. API billing is separate from a ChatGPT subscription.

For the hosted Site, configure `OPENAI_API_KEY` as a secret runtime environment variable through Sites, then deploy the saved version again. A local `.env.local` does not configure production. No key has been installed or live paid request tested as part of this prototype.

Browser → same-origin `/api/abraham` → OpenAI Responses API → browser.
The server recomputes the specimen from valid answer IDs. Optional conversation and exploration personalise speech only; they never affect scoring. Requests use `store:false`, bounded context, timeout, and an authored fallback. API route requires Sites identity outside localhost; the current Site is owner-private. The in-memory per-user limiter is best-effort per Worker instance; use durable rate limits/budgets before a broad public launch.

## p5.js

The p5.js Web Editor can share browser sketches, but cannot conceal a secret embedded in JavaScript. This repository uses Three.js for the exported Blender scene and a Vinext/Worker server for protected API calls. It is not a drop-in p5 editor sketch. A p5 frontend could call a separately hosted authenticated backend; keep the secret there and add a restricted CORS policy. Keeping frontend and API together is simpler for this project.

## Implemented

- Entry, name, three galleries, eight stops, saved/revisable choices, stable answer order, final tie-break and optional reflection.
- Deterministic six-specimen/mixed scoring, evidence, result card, download and native share.
- 3D museum export, animated rigged Abraham, gallery camera nodes, drag to look, persistent companion chat, reduced motion and no-3D view.
- Recorded oddities, authored context-based result note, optional AI chat and result note, visible fallback when unconfigured.
- Local visit persistence and explicit reset. Name/answers/chat excluded from share card.

## Current prototype limits

Blender's Eevee Shader-to-RGB is not directly portable; the web geometry uses warm PBR materials and the painted geometry, so exact rendered lighting needs another art pass. Some oddity actions are represented in dialogs; specimen-specific question display treatments, full navigation/collision, follow-player behavior, and speech/lip sync are not implemented. Result specimens are lightweight procedural replicas. Downloads currently use a typography-based card, not a specimen screenshot. Browser visual QA is limited when browser access is disabled. All eight scored answers are required, following the latest edited copy (older early-finish design is superseded).

## Checks

`npm test` covers all 65,536 answer combinations, scoring boundaries, edits, exact ties, persistence validation, memory boundaries and API fallbacks. `npx tsc --noEmit` checks TypeScript. `npm run build` builds production.

## Assets

Museum and Abraham are derived from this project's Blender/Hunyuan assets. Kenney Nature Kit assets inside the museum are CC0; see the parent `blender-museum/ASSET_CREDITS.md`. Cormorant Garamond is bundled under its OFL license in public/assets. Three.js and Draco decoder licenses are retained in dependencies / distribution.

## Publication status

Local preview verified at http://127.0.0.1:5173/. Production build succeeds. Initial Sites project registration returned `appgprj_6ae8d6170eec819195bfa6c1055c68ad`, but renewing the expired source credential later returned `project_not_found` (404). No hosted deployment is verified. Retain that project ID and resolve service/account access before retrying; do not create a duplicate Site automatically.

## Navigation and Abraham revision

Opening tagline removed. Chat launchers now appear only on the result page. During exploration Abraham walks a doorway-aware route using the existing weighted leg/foot bones; no source Blender rig is overwritten. Reduced motion pauses his route. Free OrbitControls navigation replaces the continuously forced camera: drag to orbit, two-finger pan/pinch, right-drag pan, wheel zoom, focused-canvas arrow keys, or on-screen movement buttons. Gallery and stop buttons are optional camera shortcuts. This is an orbit/pan viewer, not a first-person collision simulation; the camera can pass through geometry. The browser walk is procedural rather than a new exported Blender animation clip.

## Game presentation revision

Reception now frames the actual 3D Abraham behind the desk, with progressive dialogue and mouth-shape animation (text dialogue only; no generated voice audio). Entry title has sliced offset glitch layers; no quiz title is displayed during exploration. Numbered 3D exhibit markers open stops. Exhibit action cards preview a display note and confirm through stamping. Random authored thought bubbles project above Abraham's head, appear intermittently, and hide outside the camera view. Reduced motion disables glitch and mouth movement. Browser visual QA remains pending.
