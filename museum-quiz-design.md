# What museum specimen are you?

First-version creative and interaction specification · 2 November 2026

This is a proposed design for review, not an implemented or validated personality assessment. It uses the handoff's product goals while leaving its technical examples open to revision.

## 1. The experience

A small, navigable 3D natural history museum. Three galleries surround a central hall. The visitor makes eight deliberate decisions, then one final reflection choice. Six specimen results combine recurring priorities; mixed answers can produce a seventh, explicitly unresolved result.

Target duration: approximately 8–12 minutes, to be checked with a prototype. No countdown, survival resources, correctness tests, locked personality routes, NPC dialogue trees, or penalties for exploration. The museum is closed for a quiet preview visit, explaining the lack of crowds without introducing a mystery plot.

Opening copy:

> **What museum specimen are you?**
> Walk through a small natural history museum. At eight exhibits, make a choice as yourself. At the end, discover your specimen and the decisions that led us there.
> There are no right answers, and no science knowledge is needed. You can change an answer or pass. Looking around doesn't affect your result.
> About 10 minutes · A playful reflection, not a psychological assessment.
> **Enter the museum** · **Use the step-by-step view**

The title appears before movement begins. A persistent ticket button shows “Your visit · 3 of 8 stops answered” and separate passed stops, never personality scores. Each scored hotspot is labelled “Quiz stop”; decorative cases are labelled “Look closer.”

## 2. Navigation and interaction rules

- First-person camera, authored standing positions, tap/click to approach. Drag or keyboard buttons turn the view within a comfortable range. No joystick, jumping, precision movement, head bob, or required motion aiming.
- Start facing the central case; the three gallery entrances are visible from the hall. Select a doorway or use the ticket map to travel. Gallery order is free.
- Short eased movement, approximately 0.6–0.9 seconds; reduced-motion mode cuts directly. Offer movement off from the opening screen. Sound is off until enabled; nothing depends on it.
- Selecting a case frames it and opens a legible 2D question panel. Avoid putting essential text on small 3D textures. On phones, artwork sits above a scrollable answer sheet.
- Four answer buttons, “Not sure / pass,” and “Back to gallery.” Selection previews the consequence; “Keep this choice” confirms it. Edit is always available through the ticket.
- No timed gestures. Every slider, rotation, or placement has tap and keyboard alternatives. Inspection never unlocks an answer or changes its weight.
- All eight questions are available in any order. No reaction depends on an unanswered station. Optional callbacks are factual acknowledgements, never praise or personality judgements.
- Completion means eight answered or passed stops. A visitor can also finish early; the ticket states how many remain and offers continue or finish. Q9 follows, then optional reflection, then result.
- On return, answered cases retain a small visible change. Editing replaces the original answer and state; it does not add another score.
- WebGL unavailable or uncomfortable: the same scenes and questions appear in a linear 2D version with identical IDs, scoring, and result quality.

## 3. Spatial layout

Conceptual footprint: 24 m wide × 22 m deep, single floor. These are modelling dimensions, not construction or accessibility certification.

Coordinates: x increases east; z increases north; origin is the southwest corner.

| Space | Bounds in metres | Contents |
|---|---|---|
| Entrance vestibule | x 9–15, z 0–4 | Title, controls, optional ticket colour |
| Central hall | x 8–16, z 4–14 | Empty result case, map/ticket stand, bench |
| Deep Time, west | x 0–8, z 4–14 | Q1 fossil detail, Q2 incomplete skeleton, Q3 trace wall |
| Earth & Space, east | x 16–24, z 4–14 | Q4 mineral drawer, Q5 meteorite test, Q6 paired samples |
| Living Systems, north | x 8–16, z 14–22 | Q7 living display, Q8 shared field kit |

Hall door openings: west x=8, z=8–10; east x=16, z=8–10; north z=14, x=11–13; entrance z=4, x=11–13. No outer wing connections or dead-end corridors. Return to the hall takes one navigation action.

Case centres: Q1 (2,6.5), Q2 (2,11), Q3 (6,12.5); Q4 (22,6.5), Q5 (22,11), Q6 (18,12.5); Q7 (10,19), Q8 (14,19); result (12,9). Place standing nodes roughly 1.2–1.5 m toward the room centre from their cases. Keep at least a conceptual 1.8 m clear path around the hall case and between gallery stations. Final blockout should check camera sightlines and collision bounds.

Room appearance: mineral plaster, dark display bases, restrained brass labels, warm overhead illumination and focused case lights. Deep Time has a limestone relief; Earth & Space has a dark ceiling panel; Living Systems has translucent botanical silhouettes. These are wayfinding cues, not personality colours. Use optional environmental sound, not mandatory audio narration.

The result case is covered by frosted glass at first with “Your exhibit · revealed at the end.” After completion it reveals the result model. Inspecting it early only explains the quiz; it never assigns a provisional specimen.

## 4. Hidden priorities

Four non-exclusive priorities, used only in authoring and code:

| Code | Priority | What an answer may prioritise | Possible cost |
|---|---|---|---|
| I | Inquiry | Understanding, evidence, examining assumptions | Delaying a decision while seeking clarity |
| C | Continuity | Keeping useful context, preserving options and what already matters | Holding on after a change is needed |
| A | Agency | Making a choice, testing, retaining room to act | Acting before enough is understood or agreed |
| R | Relationship | Shared context, participation, making room for others | Taking on too much responsibility for others |

These are not intelligence, morality, sociability, or ability scales. A person can have all four. “Relationship” includes shared understanding, not just being outgoing. Choosing continuity is not scored as fear, and choosing agency is not scored as selfishness.

## 5. All eight scored questions

The letters below are authoring IDs, not visible option labels. Render answer order with a stable per-session shuffle; retain stable choice IDs. Every choice gives +2 to its primary priority and +1 to its secondary. Each station offers each priority once as primary and once as secondary. Scientific inspection tasks have no right-answer scoring.

### Q1 · Deep Time · The small detail

Interaction: rotate a fossil cast; four optional hotspots expose its details. Rotation is unscored.

**“You have time for one closer look before moving on. What would you rather leave knowing?”**

| ID | Answer | Score | Authored consequence / evidence |
|---|---|---|---|
| q1-i | How they worked out what this animal was. | I2 C1 | A comparison overlay appears. / Chose the evidence behind an identification. |
| q1-c | What survived from the original, and what was restored. | C2 A1 | Original and restored surfaces are outlined. / Wanted to distinguish retained material from later changes. |
| q1-a | What I could notice before reading the explanation. | A2 R1 | The label folds away; reveal it at any time. / Chose space for a first-hand impression. |
| q1-r | What different people noticed when they first saw it. | R2 I1 | Three short, equally plausible visitor observations appear. / Wanted multiple perspectives on the same object. |

### Q2 · Deep Time · The missing piece

Interaction: a model skeleton has one conspicuous gap. Preview the four display treatments by tapping; no dragging required.

**“This skeleton is missing a piece. Which version would you rather encounter in the museum?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q2-i | Show two possible reconstructions beside the gap. I want to compare them. | I2 A1 | Two outline alternatives appear. / Preferred competing explanations to a single reconstruction. |
| q2-c | Leave the gap visible. I want to see exactly what remains. | C2 R1 | A small original-material label appears. / Kept absence visible rather than filling it in. |
| q2-a | Add a removable reconstruction. I want to try seeing the whole animal. | A2 C1 | A clearly marked replica fills the gap. / Chose a reversible way to move forward with incomplete information. |
| q2-r | Let visitors switch between versions. Different views may help different people. | R2 I1 | A view-toggle model appears. / Made room for different ways of understanding the exhibit. |

### Q3 · Deep Time · What gets remembered

Interaction: a trace-fossil wall has room for one additional panel. The visitor clips a chosen panel into its empty slot.

**“You’re making a small record of an ordinary day, to be opened years from now. What would you put at its centre?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q3-i | The unanswered question I kept returning to. | I2 C1 | A question-card panel appears. / Kept an unresolved question as the day's central record. |
| q3-c | A small routine I might otherwise forget. | C2 I1 | A routine sketch appears. / Preserved an easily overlooked part of everyday life. |
| q3-a | A decision that changed how the day went. | A2 R1 | A branching route sketch appears. / Focused on a moment of making a difference. |
| q3-r | An exchange with someone that stayed with me. | R2 A1 | Two overlapping speech fragments appear. / Remembered the day through an interaction. |

### Q4 · Earth & Space · The surprise drawer

Interaction: open a mineral drawer and use a magnification control. The prompt concerns a familiar planning trade-off, not knowledge of minerals.

**“You set aside an afternoon for something familiar. Just as you begin, an unexpected invitation arrives. Both sound good. What is closest to your instinct?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q4-i | Get a little more detail before deciding which interests me more. | I2 A1 | A second information card slides out. / Sought more context before choosing. |
| q4-c | Keep the afternoon I planned; suggest another day for the invitation. | C2 R1 | The original tray remains framed. / Protected an existing intention while leaving a future opening. |
| q4-a | Take the invitation. I can return to my original plan. | A2 C1 | A second tray opens. / Accepted an opportunity while treating the original plan as recoverable. |
| q4-r | See whether we can combine some of both without making it awkward. | R2 I1 | Two trays slide alongside one another. / Looked for a workable shared arrangement. |

### Q5 · Earth & Space · The next test

Interaction: rotate a meteorite replica next to a proposed testing display. The stated trade-offs are fictional exhibit scenarios, not instructions for handling a real collection.

**“An unfamiliar specimen could be studied in several ways. There is funding for one next step. Which would you back?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q5-i | A detailed scan: more information, but it may not settle the main question. | I2 C1 | A scan preview appears. / Accepted an incomplete answer in exchange for more evidence. |
| q5-c | Better storage first: protect the specimen, though the answer will wait. | C2 A1 | The support cradle appears. / Protected future options before pursuing an immediate answer. |
| q5-a | A tiny sample test: a clearer answer, but it permanently uses some material. | A2 R1 | A labelled sample diagram appears; no specimen is damaged. / Accepted a stated cost for a more decisive next step. |
| q5-r | A joint study with another museum: shared expertise, but a slower start. | R2 I1 | Two comparison photographs appear. / Chose shared expertise despite a coordination cost. |

### Q6 · Earth & Space · Same label, different view

Interaction: place two mineral replicas side by side. Their interpretation cards disagree. No geological answer is required.

**“You and someone else come away from the same experience with different impressions. What would you most want to do?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q6-i | Compare the particular details each of us noticed. | I2 R1 | Detail markers connect to each card. / Explored the observations behind different impressions. |
| q6-c | Keep both accounts intact; neither needs replacing yet. | C2 I1 | Both cards are retained. / Preserved separate accounts without forcing resolution. |
| q6-a | Try a different approach together and see what happens next. | A2 C1 | A third viewing angle becomes available. / Used another experience to move beyond the disagreement. |
| q6-r | Find out why that impression mattered to them. | R2 A1 | The context side of the second card opens. / Prioritised the personal significance of another perspective. |

### Q7 · Living Systems · Room to change

Interaction: a miniature habitat model has four lighting/layout previews. Previews represent choices; no configuration is a science puzzle.

**“A shared place you love is being changed. The proposal has real benefits, but it will feel different. What would you speak up for first?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q7-i | A clear account of what the change is meant to improve. | I2 A1 | Before/after annotations appear. / Asked for the purpose and evidence behind a change. |
| q7-c | Keeping one part that makes the place feel like itself. | C2 R1 | One existing feature remains highlighted. / Protected a specific source of continuity. |
| q7-a | A trial period so we can experience it before deciding. | A2 C1 | A removable layout layer appears. / Favoured a practical, reversible trial. |
| q7-r | A way for the people who use it to shape the proposal. | R2 I1 | Visitor input markers appear. / Prioritised participation by the people affected. |

### Q8 · Living Systems · The shared field kit

Interaction: a fieldwork table has space for one extra item. Tap to add it to a display kit; nobody is exposed to danger and essential equipment is already supplied.

**“A small group has an afternoon to explore somewhere unfamiliar. The basics are covered. What extra would you most want to bring?”**

| ID | Answer | Score | Consequence / evidence |
|---|---|---|---|
| q8-i | A field guide, so we can make sense of what we find. | I2 R1 | A guide enters the kit. / Brought a resource for interpreting discoveries together. |
| q8-c | A notebook, so details don't disappear when the day ends. | C2 I1 | A notebook enters the kit. / Made room to retain details beyond the moment. |
| q8-a | A map with a few optional detours marked. | A2 C1 | A folded map enters the kit. / Kept room for self-directed exploration within a usable plan. |
| q8-r | A shared camera, so everyone can add what caught their eye. | R2 A1 | A camera enters the kit. / Chose a shared record that others could shape. |

All object choices are illustrative; do not interpret ownership, physical ability, income, or technical familiarity. The option states its intended reason, but other reasons remain possible. Result language says “in this visit,” not “you always.”

## 6. Final stop and optional personalisation

### Q9 · Central hall · Final commitment

Always offered once; no adaptive interrogation and no numeric score.

**“Before your exhibit is revealed, which would you most want this visit to have given you?”**

- I: A better understanding of something I hadn't quite grasped.
- C: Something worth remembering and coming back to.
- A: A new possibility I want to try for myself.
- R: Something I want to share or talk through with someone.
- No preference / I'm not sure.

This can resolve only an exact tie for a result place when that priority already has support from at least two different scored questions. It cannot override an established score lead.

### Optional reflection

Show a factual recap of the first answered question in each visited gallery (up to three), with exact selected wording. Ask: **“Was there a choice that didn't quite capture your reason? You can tell us here.”**

One optional text field, maximum 200 characters. “Skip” has equal prominence. No follow-up in v1. No score changes. Use the clarification to qualify an interpretation, never invent a motive or promote a priority. If it contradicts an interpretation, remove or soften that claim; retain the recorded choice as a fact.

If a model response is used: one short acknowledgement grounded in the text; no analysis language or classification. Blank input is not sent. Vague/off-topic input gets “Thanks. Your exhibit will be based on the choices you made.” Refusal simply proceeds. Do not repeat potentially sensitive text on the share card.

Unscored preferences: optional ticket colour on entry and optional favourite exhibit at the end. Colour styles the ticket only. Favourite exhibit becomes a separate souvenir thumbnail; it never changes or impersonates the scored specimen.

## 7. Scoring and selection: exact rules

1. Store `questionId`, `choiceId`, exact versioned wording, two weights, and authored evidence. Passes have no weight. Changing an answer replaces the record. Recompute totals from records rather than incrementing persistent totals.
2. For N answered scored questions, total weight is 3N. Each dimension ranges from 0 to 2N. For internal comparison use raw totals; proportions are `dimension / (3N)` and are not psychometric probabilities.
3. Each question offers all four primary priorities and all four secondary priorities exactly once. This balances scoring opportunity, not psychological desirability; wording still needs user testing.
4. Rank totals descending. A named specimen needs N ≥ 5, plus at least two separate supporting question IDs for each of its two priorities. No single question can choose the result.
5. If second place is tied with third, use Q9 only if it names one of those tied priorities and that priority has support from at least two questions. If this still leaves the top pair ambiguous, use the mixed result. A tie for first between exactly two priorities already defines the pair; Q9 is unnecessary. Ties that affect only which of the same two is primary do not change the specimen.
6. If the top two cannot satisfy support requirements, use the mixed result; never quietly substitute an unsupported lower priority.
7. A one-point second/third margin is “close” internally: still use the stable winning pair, but include one sentence acknowledging the third concern. Do not present confidence percentages.
8. If the leading priority exceeds the second by ≥4 points, use the leading-priority version of the result introduction. Otherwise use the balanced introduction. This threshold is an editorial heuristic to review during pilot testing.
9. N=3–4: a partial collection card with three factual choice references and “A short visit gives us a sketch, rather than a clear specimen.” No named personality assignment. Offer resume or keep card.
10. N=0–2: a visitor postcard with no inferred profile. “There aren't enough choices here to make a personal match.” Offer resume or choose an explicitly unscored souvenir. Never invent three evidence moments.
11. N≥5 with a pair ambiguity: mixed collection outcome, three factual references, uncertainty stated. No random choice, hidden specimen popularity weighting, alphabetical tie-break, or language model classification.
12. Personality outcomes never depend on gallery order, camera movement, dwell time, inspection clicks, optional preferences, free-text length, device, or movement accessibility mode.

Pseudocode:

```
answers = latest non-pass answer for each of q1..q8
scores, support = sum vectors and collect supporting question IDs
if count < 3: visitor_postcard
else if count < 5: partial_collection
else:
    candidates = all unordered pairs whose score sum is maximal
    if len(candidates) > 1 and Q9 is supported by >=2 questions:
        narrowed = candidates containing Q9
        if len(narrowed) == 1: candidates = narrowed
    if len(candidates) != 1: mixed_collection
    else if either priority has support < 2: mixed_collection
    else: specimen_for_pair(candidates[0])
```

The maximum-sum-pair formulation is equivalent to selecting the two highest scores and makes ties explicit. Do not filter pair candidates by support before ranking.

### Evidence selection

Pick three different answered questions: one where the first priority was primary, one where the second was primary when available, and one from another gallery if available. If a priority has only secondary support, say it appeared alongside the leading concern; never claim it led the answer. Fill remaining slots with the highest relevant contributions, breaking ties by question ID, not visit order. If only one gallery was answered, use its real evidence and don't imply cross-gallery consistency.

Include at least one mixed or contrary choice when available in an additional short sentence. Evidence uses exact labels and conservative descriptions, not inferred biography. For mixed results choose three questions spanning different expressed priorities.

## 8. Specimen outcomes

All specimens are equally finished, attractive, and shareable; no rare/legendary tiers. Pairing is a creative metaphor, not a scientific claim that an organism has a human personality. Display factual specimen information separately from “Your visit.” Do not claim a real collection accession or provenance: use a clearly fictional catalogue code such as VISIT-IC.

### I + C · Ammonite fossil · VISIT-IC

Object: a partly exposed coiled fossil in a stone matrix, with a close-up inset. Do not use a living nautilus model as an ammonite.

- Balanced intro: “You tended to look for the explanation while keeping sight of what was already there.”
- I-leading: “Understanding came first; keeping the original context helped you get there.”
- C-leading: “You kept hold of context, and wanted enough understanding to preserve it thoughtfully.”
- Strengths: retaining useful context; checking the basis of an explanation.
- Tension: you may keep investigating or preserving something after you have enough to move on.
- Complement: a small, reversible experiment can give your careful thinking somewhere to go.
- Friction: rapid changes without an explanation may be harder to accept than the change itself.
- Closing: “What would count as enough information to take the next step?”

### I + A · Cut meteorite · VISIT-IA

Object: a cut metal-rich meteorite, rough exterior and polished interior. Its journey is not described as a choice it made.

- Balanced intro: “You wanted to understand things by getting a closer look and trying something with what you learned.”
- I-leading: “You wanted a sound explanation, with room to test it rather than leave it on the label.”
- A-leading: “You preferred to move things forward, using new information to choose your next move.”
- Strengths: questioning assumptions; turning curiosity into a next step.
- Tension: the next question or experiment may pull you away before the current one is settled.
- Complement: someone who records decisions and follows through can help discoveries accumulate.
- Friction: rules that block both explanation and experimentation may frustrate you.
- Closing: “Which possibility would you actually stay with long enough to learn from?”

### I + R · Lichen on a branch · VISIT-IR

Object: a preserved lichen-bearing branch shown with magnified detail. Use a verified real reference when making the final model.

- Balanced intro: “You often wanted to understand a thing through the perspectives and connections around it.”
- I-leading: “You sought a fuller explanation, and other perspectives were part of the evidence.”
- R-leading: “Understanding other perspectives mattered, even when it complicated your first impression.”
- Strengths: comparing perspectives; making explanations easier to share.
- Tension: you may make room for so many interpretations that your own becomes difficult to state.
- Complement: a clear personal position can give the conversation something concrete to work with.
- Friction: being pushed to agree before the different views have been heard.
- Closing: “After hearing everyone else, what is your own best reading?”

### C + A · Quartz cluster · VISIT-CA

Object: several crystals attached to a rough base; no claim that crystals demonstrate resilience or personal growth.

- Balanced intro: “You wanted room to make a change without losing everything useful underneath it.”
- C-leading: “Keeping a dependable base mattered; changes felt worthwhile when they could build on it.”
- A-leading: “You wanted to act, while keeping a way to revise or return.”
- Strengths: workable continuity; reversible, practical changes.
- Tension: you may prefer changes you can control and postpone ones that require a less tidy transition.
- Complement: an outside question can reveal which familiar constraints are still necessary.
- Friction: being asked to choose between total preservation and starting from nothing.
- Closing: “Which part really needs to stay, and which part is simply familiar?”

### C + R · Branching coral skeleton · VISIT-CR

Object: a museum specimen or cast of a branching colony skeleton. Do not imply taking living coral as a souvenir.

- Balanced intro: “You returned to what lets people keep sharing something that matters.”
- C-leading: “You protected continuity, especially where other people relied on it.”
- R-leading: “You made room for others while trying to keep something dependable between you.”
- Strengths: remembering shared context; maintaining things others can rely on.
- Tension: keeping a shared arrangement going can turn into work you never agreed to carry alone.
- Complement: clear boundaries can protect the continuity you care about.
- Friction: changes that treat existing commitments as disposable.
- Closing: “What are you willing to maintain—and what needs to be shared?”

### A + R · Winged maple fruit · VISIT-AR

Object: a botanical specimen with paired winged fruits and a larger magnified model. Avoid describing the wings as two organisms cooperating.

- Balanced intro: “You looked for ways to move forward that left other people room to participate.”
- A-leading: “You wanted a next step, and preferred one others could help shape.”
- R-leading: “Participation mattered, but you also wanted it to lead somewhere.”
- Strengths: opening possibilities; inviting others into action.
- Tension: accommodating everyone while keeping things moving may leave your own preference unclear.
- Complement: a clearly stated constraint can make a shared plan easier to finish.
- Friction: plans that are either rigidly imposed or discussed without ever becoming a decision.
- Closing: “What would you choose if you didn't first have to make it work for everyone?”

### Mixed · Comparative study tray · VISIT-MX

Three miniature objects in an open study tray; no single specimen is presented as a settled match.

> “Your choices didn't settle into one clear specimen. Different situations brought different priorities forward.”

Follow with three concrete choice references. “This could reflect context, overlapping priorities, or simply options that weren't quite right for you.” No “rare,” “more complex than other people,” or automatically flattering interpretation. Offer review choices, keep this result, or restart. Do not ask repeated tie-breakers.

If one priority clearly leads but its second-place partners are tied, replace the opening with “Your visit repeatedly favoured [understanding / continuity / room to act / shared participation], but didn't settle on one clear second priority.” Do not describe a strongly consistent leading pattern as inconsistent simply because the specimen pair is unresolved.

### Result page and reveal

1. Reveal the specimen in the central case, with motion optional.
2. Specimen title and one-sentence personalised introduction.
3. Expandable factual museum label, visually separate from personality copy.
4. “Choices behind this exhibit”: three real moments, with context and selected wording.
5. “What this approach makes easier”: up to two strengths.
6. “Where it can get awkward”: one grounded tension.
7. “A useful counterweight”: complementary approach and potential friction, not relationship compatibility rules.
8. Closing reflection and “Does this fit?” with Yes / Partly / Not really. This feedback does not silently change the score; offer review.
9. Save a local result card, share using the device share sheet with explicit user action, review answers, or restart.

Share card: specimen image, specimen name, one sentence, quiz title. No raw answers, free text, score bars, real name, or implied scientific validation. Mixed and partial outcomes have equally polished card layouts.

## 9. Content and API boundary

All scenes, prompts, options, specimen mapping, reactions, and fallback paragraphs are authored locally. No model controls navigation, scoring, or resultId. A backend may personalise the optional acknowledgement and final wording, and handle visitor-initiated `companion_chat` with Abraham. Companion chat is available at every visit stage through his character or a persistent portrait button. It never changes scoring, selects answers, or supplies personality evidence. Opening and closing chat preserves the current question and any unsubmitted choice.

For result generation, send only canonical resultId, pair/variant, actual answer evidence, close/mixed flags, optional reflection, and allowed result text. Backend returns structured fields with evidence IDs. Validate that resultId is unchanged, at least three distinct eligible evidence IDs exist for normal results, descriptions don't invent choices, and content meets length limits. Under-three visitor cards use a separate schema with no evidence minimum. Use local text immediately if validation, network, or generation fails; never force a retry or show a fake delay.

A complete fallback is built from the authored result intro, three evidence sentences, strengths, tension, complement/friction, and closing question. Do not merely show a generic specimen label when the API is unavailable.

Keep text optional. Do not retain it beyond the session by default. A deliberate saved result can retain generated copy, with a clear preview. Restart clears answers, preferences, text, result, and scene state. Any analytics require a separate product decision; v1 needs none.

## 10. 3D production scope

- One reusable architectural kit: floor, wall, doorway, ceiling, trim.
- One hall case; three reusable case forms; one drawer unit; one bench; one field table; a ticket stand.
- Eight interaction scenes using replicas or simplified models. Reuse result models in environmental displays only without revealing scoring associations.
- Six result specimens and one tray composition. Tiny biological detail can be handled with high-resolution images/close-up panels rather than expensive geometry.
- Approximately 16 authored camera nodes: entrance, hall, three gallery thresholds, eight stations, result, bench, ticket stand.
- Bake or simplify lighting, instance repeated cases, compress textures, lazy-load optional close-ups. Verify performance on an actual midrange phone before choosing final visual fidelity.
- Every room can be visited without completing its questions. No hidden hotspots or collectibles required for a result.

## 11. Review and verification plan

Before modelling beyond a blockout: test the eight questions as plain cards with 5–8 people. Ask which answer felt obviously best, which choices lacked their actual reason, whether the outcome referenced them accurately, and whether museum-management language dominated. This is an editorial pilot, not scientific validation.

Scoring checks: all-I/C/A/R primary patterns; all passes; N=0/2/3/4/5/8; exact ties; one-point margins; unsupported pair; Q9 no preference; edits; repeat visits; different gallery orders; all free text skipped; conflicting free text; offline and invalid API output. Confirm all six pair outcomes are reachable and no navigation state changes scores. Check opportunity balance automatically.

Spatial checks: all doorways discoverable from hall; no result-case obstruction; label and answer readability at 320 px width; complete with keyboard, touch, reduced motion, audio off, and WebGL off. No content depends on hover, colour, or gesture precision.

Design verification completed: parsed all 32 score vectors and confirmed equal primary and secondary opportunities at every question. Enumerated all 65,536 complete four-choice answer patterns (before Q9): IC 9,168; IA 5,656; IR 10,390; CA 10,390; CR 5,656; AR 9,388; unresolved pair 14,888. All six results are reachable. This enumeration assumes equally frequent answer options, which real visitors will not necessarily choose. The unequal result frequencies are a consequence of secondary pairings, not evidence about population personality. Pilot testing should review both wording and pair distribution before release; do not alter scores to force equal result popularity. Spatial and human-readability checks remain prototype work.

## 12. Scientific reference boundary

These references support factual collection labels only, not personality interpretations:

- Meteorite variety and material: Natural History Museum, https://www.nhm.ac.uk/discover/types-of-meteorites.html
- Cut iron meteorite and internal structure: American Museum of Natural History, https://www.amnh.org/exhibitions/permanent/meteorites/meteorites/looking-inside-meteorites
- Lichens as composite/symbiotic organisms: USDA Forest Service, https://research.fs.usda.gov/treesearch/download/61432.pdf
- Corals as animals: NOAA, https://oceanservice.noaa.gov/facts/coral.html

Exact ammonite species, quartz provenance, maple species, and lichen identification remain art-production selections. Do not invent a location, date, collector, age, or conservation story for the factual label. Until species references are chosen, use broad labels and no specific biological claims.


## 12. Dreamscape and on-demand companion revision — 3 November 2026

The museum keeps its warm illustrated natural-history setting, with selected gently uncanny additions: a wall-mounted backwards clock, drifting labels, a floating meteorite, a wall-adjacent cabinet with a drawer of stars and airborne leaves. The clock case and cabinet stay fixed in plausible positions; only the clock hands and drawer contents are uncanny. The original palette and lighting are retained, without the added violet shadow tint. These are optional unscored discoveries, separate from numbered quiz stops. The layout and scoring stay unchanged.

Abraham can be tapped to talk whenever the visitor chooses. A persistent portrait provides access from other galleries. Companion conversation is separate from the one optional result reflection; it does not create extra assessment questions or alter the specimen match. The host supplies only current scene context, bounded session chat history and relevant museum facts for companion replies. Authored directions remain available offline. No unsolicited chat interruptions.

The Blender scene and local interaction preview are in `blender-museum/quiet-collection-dreamscape.blend`; implementation status and the game integration contract are in `blender-museum/dreamscape/README.md`. A live frontend/backend is still required for free-text AI conversation. This revision does not modify the Word copy document currently under user review.
