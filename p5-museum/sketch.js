// ---------------------------------------------------------------------------
// QUIZ CONTENT + SCORING
// Edit this section in the p5.js Web Editor. The museum game reads it directly.
// I = understanding, C = continuity, A = room to act, R = participation.
// Each answer gives 2 points to its main trait and 1 point to a supporting one.
// ---------------------------------------------------------------------------
const choice = (id, text, score, evidence) => ({id, text, score, evidence});
const question = (id, number, gallery, title, prompt, intro, choices) =>
  ({id, number, gallery, title, prompt, intro, choices});

window.MUSEUM_QUIZ = {
  dimensions: ['I', 'C', 'A', 'R'],
  pairs: ['IC', 'IA', 'IR', 'CA', 'CR', 'AR'],
  concerns: {
    I: 'understanding',
    C: 'continuity',
    A: 'room to act',
    R: 'shared participation'
  },
  results: {
    IC: {name: 'Paper nautilus eggcase'},
    IA: {name: 'Fulgurite'},
    IR: {name: 'Starling feather'},
    CA: {name: 'Caddisfly case'},
    CR: {name: 'Glass sponge skeleton'},
    AR: {name: 'Sea bean'},
    MX: {name: 'Classification pending'}
  },
  questions: [
    question('q1', 1, 'Deep Time', 'The small detail',
      'You have time for one closer look before moving on. What would you rather leave knowing?',
      'Come and have a look at this one. You can turn it round, too.', [
        choice('q1-i', 'How they worked out what this animal was.', {I:2,C:1}, 'Chose the evidence behind an identification.'),
        choice('q1-c', 'What survived from the original, and what was restored.', {C:2,A:1}, 'Wanted to distinguish retained material from later changes.'),
        choice('q1-a', 'What I could notice before reading the explanation.', {A:2,R:1}, 'Chose space for a first-hand impression.'),
        choice('q1-r', 'What different people noticed when they first saw it.', {R:2,I:1}, 'Wanted multiple perspectives on the same object.')
      ]),
    question('q2', 2, 'Deep Time', 'The missing piece',
      'This skeleton is missing a piece. Which version would you rather encounter in the museum?',
      'There\u2019s a bit missing from this one. We\u2019ve checked under the cabinet.', [
        choice('q2-i', 'Show two possible reconstructions beside the gap. I want to compare them.', {I:2,A:1}, 'Preferred competing explanations to a single reconstruction.'),
        choice('q2-c', 'Leave the gap visible. I want to see exactly what remains.', {C:2,R:1}, 'Kept absence visible rather than filling it in.'),
        choice('q2-a', 'Add a removable reconstruction. I want to try seeing the whole animal.', {A:2,C:1}, 'Chose a reversible way to move forward with incomplete information.'),
        choice('q2-r', 'Let visitors switch between versions. Different views may help different people.', {R:2,I:1}, 'Made room for different ways of understanding the exhibit.')
      ]),
    question('q3', 3, 'Deep Time', 'What gets remembered',
      'You\u2019re making a small record of an ordinary day, to be opened years from now. What would you put at its centre?',
      'These are things people left behind. Footprints, mostly. What would you leave to remember a day by?', [
        choice('q3-i', 'The unanswered question I kept returning to.', {I:2,C:1}, 'Kept an unresolved question as the day\'s central record.'),
        choice('q3-c', 'A small routine I might otherwise forget.', {C:2,I:1}, 'Preserved an easily overlooked part of everyday life.'),
        choice('q3-a', 'A decision that changed how the day went.', {A:2,R:1}, 'Focused on a moment of making a difference.'),
        choice('q3-r', 'An exchange with someone that stayed with me.', {R:2,A:1}, 'Remembered the day through an interaction.')
      ]),
    question('q4', 4, 'Earth & Space', 'The surprise drawer',
      'You set aside an afternoon for something familiar. Just as you begin, an unexpected invitation arrives. Both sound good. What do you do?',
      'Go on, open it. I think this is the right drawer.', [
        choice('q4-i', 'Get a little more detail before deciding which interests me more.', {I:2,A:1}, 'Sought more context before choosing.'),
        choice('q4-c', 'Keep the afternoon I planned; suggest another day for the invitation.', {C:2,R:1}, 'Protected an existing intention while leaving a future opening.'),
        choice('q4-a', 'Take the invitation. I can return to my original plan.', {A:2,C:1}, 'Accepted an opportunity while treating the original plan as recoverable.'),
        choice('q4-r', 'See whether we can combine some of both without making it awkward.', {R:2,I:1}, 'Looked for a workable shared arrangement.')
      ]),
    question('q5', 5, 'Earth & Space', 'The next test',
      'An unfamiliar specimen could be studied in several ways. There is funding for one next step. Which would you back?',
      'We\u2019ve got enough money to try one of these. Just one, though. Have a look and see what you think.', [
        choice('q5-i', 'A detailed scan: more information, but it may not settle the main question.', {I:2,C:1}, 'Accepted an incomplete answer in exchange for more evidence.'),
        choice('q5-c', 'Better storage first: protect the specimen, though the answer will wait.', {C:2,A:1}, 'Protected future options before pursuing an immediate answer.'),
        choice('q5-a', 'A tiny sample test: a clearer answer, but it permanently uses some material.', {A:2,R:1}, 'Accepted a stated cost for a more decisive next step.'),
        choice('q5-r', 'A joint study with another museum: shared expertise, but a slower start.', {R:2,I:1}, 'Chose shared expertise despite a coordination cost.')
      ]),
    question('q6', 6, 'Earth & Space', 'Same label, different view',
      'You and someone else come away from the same experience with different impressions. What would you most want to do?',
      'Same display, two different descriptions. Hmm. Have a look at both.', [
        choice('q6-i', 'Compare the particular details each of us noticed.', {I:2,R:1}, 'Explored the observations behind different impressions.'),
        choice('q6-c', 'Keep both accounts intact; neither needs replacing yet.', {C:2,I:1}, 'Preserved separate accounts without forcing resolution.'),
        choice('q6-a', 'Try a different approach together and see what happens next.', {A:2,C:1}, 'Used another experience to move beyond the disagreement.'),
        choice('q6-r', 'Find out why that impression mattered to them.', {R:2,A:1}, 'Prioritised the personal significance of another perspective.')
      ]),
    question('q7', 7, 'Living Systems', 'Room to change',
      'A place you love is being changed. The proposal has real benefits, but it will feel different. What would you speak up for first?',
      'Here\u2019s the old layout, and here\u2019s the new one. Take a look. What do you think?', [
        choice('q7-i', 'A clear account of what the change is meant to improve.', {I:2,A:1}, 'Asked for the purpose and evidence behind a change.'),
        choice('q7-c', 'Keeping one part that makes the place feel like itself.', {C:2,R:1}, 'Protected a specific source of continuity.'),
        choice('q7-a', 'A trial period so we can experience it before deciding.', {A:2,C:1}, 'Favoured a practical, reversible trial.'),
        choice('q7-r', 'A way for the people who use it to shape the proposal.', {R:2,I:1}, 'Prioritised participation by the people affected.')
      ]),
    question('q8', 8, 'Living Systems', 'The shared field kit',
      'A small group has an afternoon to explore somewhere unfamiliar. The basics are covered. What extra would you most want to bring?',
      'Everything we need is packed! There\u2019s a little space left. Anything you\u2019d like to bring?', [
        choice('q8-i', 'A field guide, so we can make sense of what we find.', {I:2,R:1}, 'Brought a resource for interpreting discoveries together.'),
        choice('q8-c', 'A notebook, so details don\'t disappear when the day ends.', {C:2,I:1}, 'Made room to retain details beyond the moment.'),
        choice('q8-a', 'A map with a few optional detours marked.', {A:2,C:1}, 'Kept room for self-directed exploration within a usable plan.'),
        choice('q8-r', 'A shared camera, so everyone can add what caught their eye.', {R:2,A:1}, 'Chose a shared record that others could shape.')
      ])
  ]
};

// Turn the selected answer IDs into point totals and the final exhibit type.
window.MUSEUM_QUIZ.scoreVisit = function scoreVisit(answers = {}, finalChoice = 'none') {
  const quiz = window.MUSEUM_QUIZ;
  const entries = quiz.questions.flatMap(q => {
    const answer = q.choices.find(c => c.id === answers[q.id]);
    return answer ? [{...answer, questionId:q.id, title:q.title, gallery:q.gallery}] : [];
  });
  const scores = {I:0,C:0,A:0,R:0};
  const support = {I:0,C:0,A:0,R:0};
  for (const entry of entries) {
    for (const [trait, points] of Object.entries(entry.score)) {
      scores[trait] += points;
      support[trait] += 1;
    }
  }
  if (entries.length < quiz.questions.length) {
    return {complete:false, code:null, scores, support, entries};
  }
  const bestTotal = Math.max(...quiz.pairs.map(pair => scores[pair[0]] + scores[pair[1]]));
  let candidates = quiz.pairs.filter(pair => scores[pair[0]] + scores[pair[1]] === bestTotal);
  if (candidates.length > 1 && support[finalChoice] >= 2) {
    const preferred = candidates.filter(pair => pair.includes(finalChoice));
    if (preferred.length === 1) candidates = preferred;
  }
  let code = 'MX';
  if (candidates.length === 1 && [...candidates[0]].every(trait => support[trait] >= 2)) {
    code = candidates[0];
  }
  const ranked = [...quiz.dimensions].sort((a,b) => scores[b] - scores[a]);
  const evidence = [];
  if (code !== 'MX') {
    for (const trait of code) {
      const item = entries.find(entry => entry.score[trait] === 2 && !evidence.includes(entry));
      if (item) evidence.push(item);
    }
  }
  for (const entry of entries) if (evidence.length < 3 && !evidence.includes(entry)) evidence.push(entry);
  return {
    complete:true,
    code,
    result:quiz.results[code],
    scores,
    support,
    entries,
    evidence:evidence.slice(0,3),
    leading:scores[ranked[0]] - scores[ranked[1]] >= 4 ? ranked[0] : null
  };
};

// These helpers let the same sketch create, update and save a visit.
window.MUSEUM_QUIZ.newVisit = () => ({
  version:1, name:'', answers:{}, finalChoice:'none', reflection:'',
  discoveries:[], messages:[], finished:false,
  seed:Math.floor(Math.random() * 2147483647)
});
window.MUSEUM_QUIZ.answer = (visit, questionId, choiceId) => {
  visit.answers[questionId] = choiceId;
  return window.MUSEUM_QUIZ.scoreVisit(visit.answers, visit.finalChoice);
};
window.MUSEUM_QUIZ.save = visit => {
  localStorage.setItem('quiet-collection-visit-v1', JSON.stringify(visit));
};
window.MUSEUM_QUIZ.load = () => {
  try { return JSON.parse(localStorage.getItem('quiet-collection-visit-v1')); }
  catch { return null; }
};

// Specimen meshes arrive as indexed triangles with their museum colours. Build
// one retained p5 geometry per material, then light, orbit and display in WEBGL.
function mountSpecimenSketch(host, parts, reduced) {
  let observer;
  const sketch = new p5(p => {
    let specimen, angle = -.15, zoom = 1;
    p.setup = () => {
      const canvas = p.createCanvas(host.clientWidth, host.clientHeight, p.WEBGL);
      canvas.elt.setAttribute('aria-label', 'Your specimen in its glass display case');
      p.pixelDensity(Math.min(1.5,window.devicePixelRatio || 1));
      p.frameRate(reduced ? 20 : 40);
      specimen = p.buildGeometry(() => {
        p.noStroke();
        for (const part of parts) {
          p.fill(part.color);
          p.beginShape(p.TRIANGLES);
          for (const i of part.indices) {
            const j=i*3;
            p.normal(part.normals[j],-part.normals[j+1],part.normals[j+2]);
            p.vertex(part.vertices[j],-part.vertices[j+1],part.vertices[j+2]);
          }
          p.endShape();
        }
      });
      observer = new ResizeObserver(()=>p.resizeCanvas(host.clientWidth,host.clientHeight));
      observer.observe(host);
      canvas.mouseWheel(e=>{zoom=p.constrain(zoom-e.deltaY*.001,.75,1.5);return false;});
    };
    p.mouseDragged=()=>{if(p.mouseX>=0&&p.mouseX<p.width&&p.mouseY>=0&&p.mouseY<p.height) angle+=(p.mouseX-p.pmouseX)*.008;};
    p.draw=()=>{
      p.clear();p.ambientLight(165,154,132);p.directionalLight(255,230,177,-.4,.6,-1);
      p.rotateX(-.07);p.rotateY(angle+(reduced?0:p.sin(p.millis()*.00035)*.13));
      p.scale(Math.min(p.width/3.2,p.height/2.9)*zoom);
      p.noStroke();p.model(specimen);
      function block(x,y,z,w,h,d,color){p.push();p.translate(x,y,z);p.fill(color);p.box(w,h,d);p.pop();}
      block(0,.8,0,2.15,.16,1.35,'#67452e');
      for(const x of [-1,1])for(const z of [-.63,.63])block(x,-.1,z,.035,1.8,.035,'#c3a371');
      block(0,-1,0,2.1,.055,1.36,'#ae905b');
      block(0,-.1,.64,2,1.75,.005,p.color(213,232,211,24));
    };
  },host);
  return ()=>{observer?.disconnect();sketch.remove();};
}

// Editable p5.js scene. The asset renderer supplies the rigged GLB animation,
// and p5 draws the scene, atmosphere, and a brief ripple when the visitor taps.
function mountMuseumSketch(host, initialise) {
  let disposeScene;
  const sketch = new p5(p => {
    let scene;
    let ripple;
    let observer;
    p.setup = () => {
      const canvas = p.createCanvas(Math.max(1, host.clientWidth), Math.max(1, host.clientHeight));
      p.pixelDensity(Math.min(window.devicePixelRatio || 1, 1.5));
      p.frameRate(45);
      scene = initialise(canvas.elt);
      if (!scene) { p.noLoop(); return; }
      const resize = () => {
        p.resizeCanvas(Math.max(1, host.clientWidth), Math.max(1, host.clientHeight), true);
        scene.resize();
      };
      observer = new ResizeObserver(resize);
      observer.observe(host);
      const tap = e => {
        const bounds = canvas.elt.getBoundingClientRect();
        ripple = {x:e.clientX-bounds.left,y:e.clientY-bounds.top,start:p.millis()};
      };
      canvas.elt.addEventListener('pointerdown', tap);
      disposeScene = () => {
        canvas.elt.removeEventListener('pointerdown', tap);
        observer.disconnect();
        scene.dispose();
      };
    };
    p.draw = () => {
      if (!scene || document.hidden) return;
      scene.tick(Math.min(p.deltaTime / 1000, .05));
      p.clear();
      p.drawingContext.drawImage(scene.surface,0,0,p.width,p.height);
      if (scene.reduced || !scene.exploring) return;
      // Small amber motes in the lamplight. Each retains a stable drift path.
      const t = p.millis() / 1000;
      p.noStroke();
      for (let i=0;i<12;i++) {
        p.fill(246,215,153,18+12*p.sin(t+i));
        p.circle(p.noise(i*13,t*.025)*p.width,p.noise(i*7+55,t*.018)*p.height,2);
      }
      if (ripple) {
        const progress=(p.millis()-ripple.start)/360;
        if (progress>=1) ripple=null;
        else {p.noFill();p.stroke(245,222,172,110*(1-progress));p.strokeWeight(1);p.circle(ripple.x,ripple.y,6+22*progress);}
      }
    };
  },host);
  return () => {disposeScene?.();sketch.remove();};
}
