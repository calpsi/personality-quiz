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
  {
    "id": "q1",
    "number": 1,
    "gallery": "Deep Time",
    "title": "The small fossil",
    "prompt": "This fossil cast has a tiny feature that changes how it is understood. You have time to open one part of the display. Which would you choose?",
    "intro": "It’s a very small fossil, but the label has rather a lot to say. Which part would you open?",
    "choices": [
      {
        "id": "q1-i",
        "text": "How the curators worked out what kind of animal it was.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Chose the evidence behind the fossil’s identification."
      },
      {
        "id": "q1-c",
        "text": "Which parts are original fossil, and which were restored.",
        "score": {
          "C": 2,
          "A": 1
        },
        "evidence": "Wanted to distinguish surviving material from later restoration."
      },
      {
        "id": "q1-a",
        "text": "A chance to study it without the label, then reveal the explanation.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Chose space for a first-hand impression before reading the answer."
      },
      {
        "id": "q1-r",
        "text": "What different visitors noticed when they first saw it.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Wanted several perspectives on the same fossil."
      }
    ]
  },
  {
    "id": "q2",
    "number": 2,
    "gallery": "Deep Time",
    "title": "The missing piece",
    "prompt": "This skeleton is missing one piece. Which version would you rather encounter in the museum?",
    "intro": "There’s a gap just there. We know something belonged in it, but not quite what.",
    "choices": [
      {
        "id": "q2-i",
        "text": "Show two possible reconstructions beside the gap so I can compare them.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Preferred competing explanations to a single reconstruction."
      },
      {
        "id": "q2-c",
        "text": "Leave the gap visible so I can see exactly what remains.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Kept an absence visible rather than filling it in."
      },
      {
        "id": "q2-a",
        "text": "Add a clearly marked, removable replica so I can picture the whole animal.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Chose a reversible way to move forward with incomplete information."
      },
      {
        "id": "q2-r",
        "text": "Let visitors switch between the possible versions themselves.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Made room for different ways of understanding the skeleton."
      }
    ]
  },
  {
    "id": "q3",
    "number": 3,
    "gallery": "Deep Time",
    "title": "A trace of an ordinary day",
    "prompt": "This trace-fossil wall has one empty archive slot. If you added a small record of an ordinary day, what would you put at its centre?",
    "intro": "Most days don’t leave fossils. We could keep one small trace of yours, though.",
    "choices": [
      {
        "id": "q3-i",
        "text": "An unanswered question I kept returning to.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Kept an unresolved question as the day’s central record."
      },
      {
        "id": "q3-c",
        "text": "A small routine I might otherwise forget.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Preserved an easily overlooked part of everyday life."
      },
      {
        "id": "q3-a",
        "text": "A decision that changed how the day went.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Focused on a moment of making a difference."
      },
      {
        "id": "q3-r",
        "text": "An exchange with someone that stayed with me.",
        "score": {
          "R": 2,
          "A": 1
        },
        "evidence": "Remembered the day through an interaction."
      }
    ]
  },
  {
    "id": "q4",
    "number": 4,
    "gallery": "Earth & Space",
    "title": "The surprise drawer",
    "prompt": "A mineral drawer opens to two trays: one familiar sample and one unexpected find. You only have time for one arrangement. What is closest to your instinct?",
    "intro": "The second tray wasn’t on my list. It does look interesting, doesn’t it?",
    "choices": [
      {
        "id": "q4-i",
        "text": "Read a little more about both samples before choosing which to examine.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Sought more context before choosing."
      },
      {
        "id": "q4-c",
        "text": "Stay with the familiar sample and give it the closer look I planned.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Protected an existing intention while leaving a future opening."
      },
      {
        "id": "q4-a",
        "text": "Switch to the unexpected sample; I can return to the familiar one later.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Accepted an opportunity while treating the original plan as recoverable."
      },
      {
        "id": "q4-r",
        "text": "Place both trays side by side and compare them with someone.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Looked for a shared comparison that kept both options in view."
      }
    ]
  },
  {
    "id": "q5",
    "number": 5,
    "gallery": "Earth & Space",
    "title": "The next test",
    "prompt": "If you were helping the museum choose one next step for this unfamiliar meteorite, which would you back?",
    "intro": "One meteorite, one bit of funding, and four sensible forms. I’m glad it isn’t my decision.",
    "choices": [
      {
        "id": "q5-i",
        "text": "A detailed scan: more information, though it may not settle the main question.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Accepted an incomplete answer in exchange for more evidence."
      },
      {
        "id": "q5-c",
        "text": "Better storage first: protect the meteorite, though the answer will wait.",
        "score": {
          "C": 2,
          "A": 1
        },
        "evidence": "Protected future options before pursuing an immediate answer."
      },
      {
        "id": "q5-a",
        "text": "A tiny sample test: a clearer answer, but it permanently uses some material.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Accepted a stated cost for a more decisive next step."
      },
      {
        "id": "q5-r",
        "text": "A joint study with another museum: shared expertise, but a slower start.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Chose shared expertise despite a coordination cost."
      }
    ]
  },
  {
    "id": "q6",
    "number": 6,
    "gallery": "Earth & Space",
    "title": "Same samples, different view",
    "prompt": "You and another visitor study the same two mineral samples but leave very different notes. What would you want to do next?",
    "intro": "Same samples, two different labels. Neither one looks obviously wrong to me.",
    "choices": [
      {
        "id": "q6-i",
        "text": "Compare the particular details each of us noticed.",
        "score": {
          "I": 2,
          "R": 1
        },
        "evidence": "Explored the observations behind different impressions."
      },
      {
        "id": "q6-c",
        "text": "Keep both accounts intact; neither needs replacing yet.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Preserved separate accounts without forcing resolution."
      },
      {
        "id": "q6-a",
        "text": "Try a different viewing angle together and see what changes.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Used another experience to move beyond the disagreement."
      },
      {
        "id": "q6-r",
        "text": "Ask why that impression of the samples mattered to them.",
        "score": {
          "R": 2,
          "A": 1
        },
        "evidence": "Prioritised the personal significance of another perspective."
      }
    ]
  },
  {
    "id": "q7",
    "number": 7,
    "gallery": "Living Systems",
    "title": "Room to change",
    "prompt": "This miniature habitat is being redesigned. The proposal has real benefits, but it will feel different. What would you speak up for first?",
    "intro": "Here’s the old habitat, and here’s the proposal. They moved nearly everything.",
    "choices": [
      {
        "id": "q7-i",
        "text": "A clear account of what the habitat change is meant to improve.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Asked for the purpose and evidence behind a change."
      },
      {
        "id": "q7-c",
        "text": "Keep one feature that makes the habitat feel like itself.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Protected a specific source of continuity."
      },
      {
        "id": "q7-a",
        "text": "Use a trial layout before making the redesign permanent.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Favoured a practical, reversible trial."
      },
      {
        "id": "q7-r",
        "text": "Let the keepers and regular visitors help shape the proposal.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Prioritised participation by the people affected."
      }
    ]
  },
  {
    "id": "q8",
    "number": 8,
    "gallery": "Living Systems",
    "title": "The shared field kit",
    "prompt": "A small group is taking this field kit somewhere unfamiliar. The basics are packed, with room for one extra item. What would you add?",
    "intro": "The sensible things are packed. There’s just enough room for one interesting thing.",
    "choices": [
      {
        "id": "q8-i",
        "text": "A field guide, so we can make sense of what we find.",
        "score": {
          "I": 2,
          "R": 1
        },
        "evidence": "Brought a resource for interpreting discoveries together."
      },
      {
        "id": "q8-c",
        "text": "A notebook, so details don’t disappear when the day ends.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Made room to retain details beyond the moment."
      },
      {
        "id": "q8-a",
        "text": "A map with a few optional detours marked.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Kept room for self-directed exploration within a usable plan."
      },
      {
        "id": "q8-r",
        "text": "A shared camera, so everyone can add what caught their eye.",
        "score": {
          "R": 2,
          "A": 1
        },
        "evidence": "Chose a shared record that others could shape."
      }
    ]
  }
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
