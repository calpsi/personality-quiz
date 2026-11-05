# The Quiet Collection · p5.js edition

Open the preview at http://127.0.0.1:5174 while the local server is running. To start it again from this folder, run:

    python3 -m http.server 5174 --bind 127.0.0.1

The included museum.js and museum.css are already built. Serve this folder on any static web host to run it online. Keep the assets and vendor folders beside index.html. The sketch loads its own models, music, and p5.js runtime.

Edit **sketch.js** to change the canvas, pacing, touch effects, or specimen presentation. The visitor's exhibit uses p5 WEBGL geometry, materials, lights, and camera interaction. The exploration sketch uses p5 for the canvas, timing and compositing, with Three.js for the existing animated GLB assets. React provides the accessible HTML menus and dialogue.

The source for scoring, interactions, visitor records, and the six specimens is in **src/**. Changes to sketch.js take effect on refresh. After changing src/, run **node p5-museum/build.mjs** from the parent museum repository with museum-site dependencies installed.

In the p5 Web Editor, use the supplied index.html and sketch.js and upload museum.js, museum.css, vendor/p5.min.js and the assets tree with matching paths, subject to your account's storage and upload limits. The local or static-hosted copy requires no editor upload.

Abraham uses written conversation and visit-based remarks in the standalone edition. An optional **window.MUSEUM_CHAT_ENDPOINT** set before museum.js can point to a compatible authenticated server endpoint. Cross-origin hosting requires that endpoint to permit your sketch origin. Keep service credentials on the server.
