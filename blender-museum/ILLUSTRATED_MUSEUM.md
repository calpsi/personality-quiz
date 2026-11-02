# Finished illustrated environment

Open **quiet-collection-illustrated-museum.blend**. This is the newest full-museum version. The original and the two earlier style studies are preserved.

## Changes

- The approved illustrated treatment now covers the central hall, entrance, Deep Time, Earth & Space, and Living Systems, including specimen curves, imported nature props, furniture, and architecture.
- Gallery titles and exhibit labels use **Cormorant Garamond**, with spaced capitals for headings and title case for the smaller labels. The font is packed in the .blend and its SIL Open Font License is in `assets/fonts/CormorantGaramond-OFL.txt`.
- The static `YOUR EXHIBIT` label has been removed from this file.
- **WHAT ARE YOU?** floats above the central case. It gently rises and falls over six seconds, with two brief clusters of teal/coral offset echoes and short line fragments. The main text remains visible throughout.
- The central pendant has moved toward the back of the hall to give the title space.

## Animation

The file retains the original 720-frame / 24fps walkthrough camera. The title animation repeats every 144 frames across that timeline. Scrub around frames **50–55** or **103–106** to inspect the glitch; frame **1** is the clean floating title.

Collection **09 | WHAT ARE YOU — floating title** contains three text objects and three animated line fragments. The main text, colours, movement, and echoes are independently editable. For a static version, mute those animation actions, position the main title, and hide the ghost/fragment objects.

Camera **08 | Floating title close view** is used for the six-second `what-are-you-title.mp4` preview. Other camera names are unchanged.

## Rendering and files

Use **Eevee**. The illustrated materials use Shader to RGB; Cycles will not reproduce the same look. The project opens with interior walls and ceilings enabled and the hall camera active.

- `renders/08-illustrated-hall-final.png`
- `renders/09-illustrated-deep-time.png`
- `renders/10-illustrated-earth-space.png`
- `renders/11-illustrated-living-systems.png`
- `renders/12-floating-title-glitch.png`
- `what-are-you-title.mp4` — six seconds, 24fps, fixed camera.

Rebuild with `complete_illustrated_museum.py`; it reuses the approved treatment in `illustrated_hall.py` and reads the original museum file. Export the title preview with `render_title_preview.py`. These scripts replace their own named outputs, so preserve a copy before manually editing them.

This remains the editable museum environment. It does not yet implement gameplay navigation, quiz scoring, or the API companion. The procedural toon materials, line geometry, text, and animation will need a deliberate web/game export step.
