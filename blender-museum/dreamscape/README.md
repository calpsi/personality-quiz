# The Quiet Collection — dreamscape revision

Open `../quiet-collection-dreamscape.blend`. This is a separate version based on the museum with the latest Hunyuan facial rig. Earlier scenes and the copy-review Word document are untouched.

## Scene changes

Warm timber, painterly materials and amber lamps remain. The original palette, shadows and light objects are preserved without recolouring. Selected anomalies create the uncanny feeling without moving the room layout or numbered quiz stops:

- A brass clock with a solid wooden case is mounted on the north hall wall and runs backwards. Its case stays still. Touching it pauses/resumes its hands in the preview.
- Three accession cards hover away from their displays. Touching them lowers them; touching again restores their drift.
- The meteorite hangs above an empty cradle. Inspecting it gives Abraham's reaction.
- A small cabinet stands against the north hall wall below the clock and contains a drawer of stars. The drawer can be opened/closed.
- Botanical leaves float in Living Systems and can be gathered/released.
- The central specimen and fragments hover gently. Existing WHAT ARE YOU? glitch remains; its main text stays readable.
- A quiet floating annotation and a few luminous dust motes sit behind the central case.
- Abraham is at the right side of the hall and has a talk prompt. His original mesh and facial rig are retained.

All new text is provisional. The Word document currently being edited is not regenerated or changed.

## Try the interactions in Blender

1. Open the new scene and switch to the Scripting workspace.
2. Select the embedded `museum_interactions.py` in the Text Editor and press Run Script. It does not run automatically or make network calls.
3. In a 3D viewport, press N and select the **Museum** tab.
4. Use **Enable click interactions**, then click Abraham or an anomaly. Esc ends the click mode. The sidebar buttons also trigger each interaction without needing to find it in the scene.
5. Abraham's panel offers directions, a reaction to the strangeness, and casual conversation. **Back to the museum** closes it. The Talk button stays available throughout this preview.

These are authored local replies, not a connected AI conversation. Object hits and the sidebar actions are a Blender prototype; they are not exported browser events. Script state changes are undoable, and reopening the saved scene resets the preview. Render in Eevee: the painterly Shader to RGB materials are not Cycles compatible.

## Required playable-game behaviour

The project currently has no gameplay frontend or chat backend. The following defines the next integration, rather than claiming it is already live:

- Every visible Abraham mesh resolves to `interaction_id=abraham`. Tap/click opens the same companion panel as an always-available portrait button. Enter/Space and a labelled 44px minimum button provide equivalent access.
- The portrait stays available in all galleries, while answering questions and after the result. Abraham need not teleport or follow the camera to remain reachable.
- Opening chat preserves question ID, unsent selection, scroll position and visit progress. Closing returns focus to the triggering control. Escape closes chat. Chat does not submit answers or advance a question.
- Suggested topics: directions, the nearby exhibit, the current oddity, and casual chat. Include free-text input for live `companion_chat`, with visible sending/error/retry states and an always-available Close control.
- Only send the current message, a bounded recent history, relevant museum facts, gallery and visit stage. Do not infer traits from chats, wandering or anomaly interactions. Do not route companion messages into scoring or the optional scored-result explanation record.
- Validate generated JSON and allowlisted expression/gesture values. Treat reply as plain text. Keep provider credentials server-side. No credentials have been added in this revision.
- Authored replies remain available if AI is offline. Say “I can't reply freely just now, but I can still help with directions.” Retain the visitor's draft on error. Discard late responses after chat is closed/reset or a newer request supersedes them.
- Anomaly interactions are optional, repeatable and unscored. Keep them distinct from numbered quiz choices. Nothing locks a route or requires a scavenger hunt.
- Reduced motion: hold objects at their stored `rest_location` / `rest_rotation`, suppress title ghosts and fragments, and leave captions static. Avoid camera shake, automatic camera movement and new flashing effects. Existing title glitch can be disabled separately.

The companion system prompt in `../abraham/abraham-system-prompt.md` now includes `companion_chat`, knowledge boundaries for these fictional anomalies and the actual facial-rig capabilities. The existing reflection and final-profile contracts are retained.

## Files

- `build_dreamscape.py`: reproducible additive scene build and still renders.
- `museum_interactions.py`: embedded opt-in local Blender interaction preview.
- `dream-hall.png` / `dream-earth-space.png`: rendered checks.
- `dreamscape-preview.mp4`: short animated hall preview.
- `interaction-manifest.json`: identifiers and intended game events, not a game implementation.

Reference direction: Penacony's dreamlike dislocations were the user's visual reference; this museum keeps its own natural-history setting and objects. No game assets were copied. Background reference: https://blog.playstation.com/2024/01/26/honkai-star-rail-version-2-0-features-new-realm-penacony-live-february-6/
