from pathlib import Path
from docx import Document
from copy import deepcopy
import shutil,json,hashlib
P=Path(__file__).resolve().parent
path=P/'The Quiet Collection Complete Game Copy.docx'
backup=P/'backups'/'Before Abraham voice revision 2026-11-03.docx';backup.parent.mkdir(exist_ok=True)
assert not backup.exists(), 'Backup already exists: do not apply twice'
shutil.copy2(path,backup)
doc=Document(path);before=[p.text for p in doc.paragraphs]
changes={
'ENTRY-06': 'Oh, hello! Here for an appraisal? I’m Abraham. What should I call you?',
'ENTRY-09': 'The galleries are just through there. Start wherever you like! Keep your ticket handy so you can see where you’ve been.',
'CASE-02': 'Not just yet! There are still a few stops on your ticket. Have a little wander, then come back to me.',
'Q1-INTRO': 'Come and have a look at this one. You can turn it round, too.',
'Q2-INTRO': 'There’s a bit missing from this one. We’ve checked under the cabinet.',
'Q3-INTRO': 'These are things people left behind. Footprints, mostly. What would you leave to remember a day by?',
'Q4-INTRO': 'Go on, open it. I think this is the right drawer.',
'Q5-INTRO': 'We’ve got enough money to try one of these. Just one, though. Have a look and see what you think.',
'Q6-INTRO': 'Same display, two different descriptions. Hmm. Have a look at both.',
'Q7-INTRO': 'Here’s the old layout, and here’s the new one. Take a look. What do you think?',
'Q8-INTRO': 'Everything we need is packed! There’s a little space left. Anything you’d like to bring?',
'FINAL-01': 'All eight! Now, before your appraisal—was there something you were hoping to find here?',
'AI-REFLECT-01': 'Ohh, I see. You wanted to be able to change your mind. Thanks for telling me.',
'AI-REFLECT-02': 'Ah, none of them quite said it. Thanks for explaining. I won’t guess at the rest.',
'AI-REFLECT-03': 'That’s all right. We can leave it there.',
'AI-REFLECT-04': 'Oh, I see what you mean now. Same choice, different reason. Thanks for explaining!',
'AI-REFLECT-05': 'Of course. On we go!',
'AI-REFLECT-06': 'All right. I’ll go by the choices on your ticket.',
'AI-REFLECT-07': 'I’ve still got your ticket. We can carry on with that.',
'AI-REFLECT-08': 'Right, let’s have a look at your appraisal!',
'RESULT-04': 'Here we are! Your match is {specimen_name_with_article}.',
'VISIT-MX-ABRAHAM': 'Hmm. I can’t quite pick one from these choices. I’ve put them together in a little tray for you.',
'PARTIAL-ABRAHAM': 'There are a few choices here, but I haven’t got a match for you yet. Shall we keep your ticket?',
'POSTCARD-ABRAHAM': 'Have another wander if you like. You can choose a little souvenir, too.',
'FEEDBACK-03': 'Oh, good! Would you like to keep the card, or have another look?',
'FEEDBACK-04': 'A bit of it, then? You can have another look at your choices. No need to start all over.',
'FEEDBACK-05': 'Oh, not quite you? That’s all right. You can look back at your answers if you like, or leave it here.',
'AB-HELP-01': 'Pick what feels closest to you at each stop. You can change your mind! I only use the choices on your ticket for the appraisal.',
'AB-HELP-02': 'Anywhere you like! Deep Time is on the left, Earth & Space is on the right, and Living Systems is straight ahead.',
'AB-HELP-03': 'Oh, you don’t need to know all the names. That’s what the labels are for!',
'AB-HELP-04': 'Oh, no. Have a good look around! I only use the choices on your ticket.',
'AB-HELP-05': 'Of course! Open your ticket and pick the stop you’d like to go back to. We’ll use your new answer.',
'AB-HELP-06': 'Of course. You can leave that one for now and come back before your appraisal.',
'AB-HELP-07': 'It’s a little comparison based on your choices here. It isn’t a scientific test, and you don’t have to agree with it.',
'AB-HELP-08': 'Hmm, I don’t know that one. I’d need to check.',
'AB-AMBIENT-01': 'Now, where did I put my pencil? Oh. Here it is.',
'AB-AMBIENT-02': 'You can sit here if you like. I’ll keep you company.',
'AB-AMBIENT-03': 'Bye, then! It was lovely having you here. Come and see me again sometime.',
'AB-HELP-09': 'Yes, I’m an AI-powered hamster! Our chats don’t affect your appraisal. Only the choices on your ticket do.',
'AB-HELP-10': 'Abraham is available whenever the visitor taps him or the persistent portrait. Use these authored help lines as fallbacks for companion chat. Ambient lines are optional; do not repeat them frequently or judge a quiz answer.',
'VOICE-01': 'Abraham is a friendly, earnest little hamster who considers the museum a perfectly normal place to work. He notices its peculiarities but rarely recognises their unsettling implications. He speaks simply and casually, takes small practical concerns seriously, and wants visitors to feel welcome. His warmth is sincere; he isn’t secretly teasing the visitor or delivering knowing hints.',
'VOICE-02': 'Most replies are one to three short sentences. Use contractions and concrete words. A small “Oh!”, “Hmm” or “Let’s see” can sound spontaneous, but vary the openings. Not every line needs a joke, hesitation or exclamation.',
'VOICE-06': 'Prefer “Oh, I see”, “Have a look”, “What should I call you?” and simple references to an actual choice. Describe things Abraham can point to: tickets, drawers, labels and specimens. Keep assessment explanations on the result card; do not make every conversation sound like a report.',
'VOICE-07': 'Avoid “This proves”, “You always”, “You clearly value”, “According to my analysis” and therapist-like acknowledgements such as “That’s useful to notice”. No baby talk, constant snack jokes, elaborate metaphors or knowing warnings. He must not imply he has sinister knowledge of the visitor.',
'VOICE-08': 'Be welcoming from the first meeting, then become more familiar naturally. Abraham’s friendliness does not depend on quiz choices. He can fail to notice that a room feels creepy while noticing that the visitor wants company. If someone is genuinely upset, listen and respond kindly; do not keep making jokes.',
}
changed_indices=set();found=set()
def replace_text(p,text):
 if p.runs:
  p.runs[0].text=text
  for r in p.runs[1:]:r.text=''
 else:p.add_run(text)
for i,p in enumerate(doc.paragraphs[:-1]):
 key=p.text.split('|')[0].strip()
 if key in changes:
  assert key not in found,key
  replace_text(doc.paragraphs[i+1],changes[key]);found.add(key);changed_indices.add(i+1)
assert found==set(changes),set(changes)-found
# New authored conversations get a separate page, leaving the user's page structure intact.
paras=doc.paragraphs
anchor=next(p for p in paras if p.text=='Editable guidance for personalised dialogue')
heading=deepcopy(anchor._p);hp=type(anchor)(heading,anchor._parent);replace_text(hp,'Abraham optional conversations');anchor._p.addprevious(heading)
label_template=next(p for p in paras if p.text.startswith('AB-AMBIENT-01'))
body_template=paras[paras.index(label_template)+1] if label_template in paras else None
# Paragraph wrappers are not identity-stable; obtain body template by index.
li=next(i for i,p in enumerate(paras) if p.text.startswith('AB-AMBIENT-01'));body_template=paras[li+1]
extras=[
('ENTRY-14','Name left empty','No name? Let’s see… Item-09. There! You can tell me if you think of something you like better.'),
('AB-DREAM-01','Asked why the clock goes backwards','Oh, it does that. You haven’t missed anything—we’re still open.'),
('AB-DREAM-02','Looking inside the drawer of stars','Yes! Mind your sleeves. They’re quite difficult to get out.'),
('AB-DREAM-03','Visitor says the museum is creepy','Is it? Would you like me to come with you?'),
('AB-DREAM-04','Floating accession labels','Those go by the minerals. I’ll put them back when they come down.'),
('AB-DREAM-05','Hovering meteorite','Oh, you can see underneath it now! That’s handy.'),
('AB-DREAM-06','Drifting leaves','Mind your head. They tickle if they get in your ears.'),
('AB-CHAT-01','Visitor taps Abraham','Oh, hello! What can I help you with?'),
('AB-CHAT-02','Casual conversation','I found my pencil! It was right here the whole time. What have you been looking at?'),
('AB-DREAM-NOTE','Dialogue direction','These lines are optional fictional museum dialogue. Use only for the matching scene or visitor message. The offer of company is a conversation line, not an implemented follow-player action. Do not promise movement unless the game supports it.')]
for key,label,body in extras:
 for template,text in [(label_template,f'{key}  |  {label}  |  '+('Editorial' if key=='AB-DREAM-NOTE' else 'Draft')),(body_template,body)]:
  e=deepcopy(template._p);p=type(anchor)(e,anchor._parent);replace_text(p,text);anchor._p.addprevious(e)
# Existing header has page_break_before; cloned header starts its own page too.
# Preserve every pre-existing paragraph outside the deliberate voice replacements.
after_existing=[]
for i,p in enumerate(paras):
 assert p.text==(changes.get(before[i-1].split('|')[0].strip()) if i in changed_indices else before[i]), f'Unexpected change {i}'
# Guard against the document changing externally since this script started.
assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256(backup.read_bytes()).digest()
doc.save(path)
(P/'abraham-voice-changes.json').write_text(json.dumps({'replacements':changes,'newEntries':extras,'preservedOtherParagraphs':True},ensure_ascii=False,indent=2))
print(f'Updated {len(changes)} entries; added {len(extras)} entries. All other original paragraphs preserved.')
