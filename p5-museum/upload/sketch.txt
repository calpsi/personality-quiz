// Owner setup: a key saved here is visible to anyone who opens the sketch.
window.ABRAHAM_API_KEY = "";
window.MUSEUM_MUSIC_URL = "https://cdn.jsdelivr.net/gh/calpsi/personality-quiz@main/museum-site/public/assets/sergequadrado-moment-14023.mp3";

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
    "title": "A free afternoon",
    "prompt": "You have a completely free afternoon with no obligations. Which plan sounds best?",
    "intro": "A free afternoon! Those are rare. What would you do with one?",
    "choices": [
      {
        "id": "q1-i",
        "text": "A beginner workshop where someone explains how everything works as you go.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Preferred to understand a new activity while learning it."
      },
      {
        "id": "q1-c",
        "text": "Going back to a place I already like and noticing something I missed before.",
        "score": {
          "C": 2,
          "A": 1
        },
        "evidence": "Returned to something familiar to find more within it."
      },
      {
        "id": "q1-a",
        "text": "A drop-in activity where I can experiment without committing to the whole day.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Chose a low-pressure way to experiment independently."
      },
      {
        "id": "q1-r",
        "text": "Joining friends for something none of us has tried before.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Preferred discovering something new alongside other people."
      }
    ]
  },
  {
    "id": "q2",
    "number": 2,
    "gallery": "Deep Time",
    "title": "The uncertain plan",
    "prompt": "You’re planning a day out, but one important detail is still uncertain. What do you do?",
    "intro": "The plan has a little gap in it. Plans do that sometimes.",
    "choices": [
      {
        "id": "q2-i",
        "text": "Compare the two most likely versions before choosing between them.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Compared the likely possibilities before committing."
      },
      {
        "id": "q2-c",
        "text": "Keep the confirmed parts of the plan and leave that time open for now.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Protected what was already settled without forcing the missing detail."
      },
      {
        "id": "q2-a",
        "text": "Choose an easy backup plan that we can change later if needed.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Moved forward with a practical, reversible backup."
      },
      {
        "id": "q2-r",
        "text": "Ask everyone going which option they would enjoy most.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Made the uncertain part of the plan a shared decision."
      }
    ]
  },
  {
    "id": "q3",
    "number": 3,
    "gallery": "Deep Time",
    "title": "What you keep",
    "prompt": "At the end of an ordinary week, you save one small thing to remember it by. What do you choose?",
    "intro": "These are things people left behind. Footprints, mostly. What would you leave to remember a week by?",
    "choices": [
      {
        "id": "q3-i",
        "text": "A question I kept thinking about, even though I never answered it.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Kept an unresolved question as the week’s central memory."
      },
      {
        "id": "q3-c",
        "text": "A tiny routine or detail that I might otherwise forget.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Preserved an easily overlooked part of everyday life."
      },
      {
        "id": "q3-a",
        "text": "A decision I made that changed how the week went.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Focused on a moment of making a difference."
      },
      {
        "id": "q3-r",
        "text": "A conversation or message from someone that stayed with me.",
        "score": {
          "R": 2,
          "A": 1
        },
        "evidence": "Remembered the week through an interaction."
      }
    ]
  },
  {
    "id": "q4",
    "number": 4,
    "gallery": "Earth & Space",
    "title": "A last-minute invitation",
    "prompt": "You’ve planned a quiet afternoon for yourself. A friend suddenly invites you somewhere you’d probably enjoy. What do you do?",
    "intro": "Oh! A last-minute invitation. Those make the day wobble a little.",
    "choices": [
      {
        "id": "q4-i",
        "text": "Ask for a few more details before deciding which plan sounds better.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Sought more context before choosing."
      },
      {
        "id": "q4-c",
        "text": "Keep the afternoon I planned and suggest meeting another day.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Protected an existing intention while leaving a future opening."
      },
      {
        "id": "q4-a",
        "text": "Go with my friend. I can return to my original plan later.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Accepted an opportunity while treating the original plan as recoverable."
      },
      {
        "id": "q4-r",
        "text": "See whether we can meet for part of it so I still get some time to myself.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Looked for a workable shared arrangement."
      }
    ]
  },
  {
    "id": "q5",
    "number": 5,
    "gallery": "Earth & Space",
    "title": "When something goes wrong",
    "prompt": "Your phone or laptop suddenly starts behaving strangely. What do you do first?",
    "intro": "It was working a moment ago. They’re rather dramatic, these little machines.",
    "choices": [
      {
        "id": "q5-i",
        "text": "Look up the symptoms and work out what probably caused the problem.",
        "score": {
          "I": 2,
          "C": 1
        },
        "evidence": "Looked for an explanation before attempting a fix."
      },
      {
        "id": "q5-c",
        "text": "Back up anything important before changing or restarting anything.",
        "score": {
          "C": 2,
          "A": 1
        },
        "evidence": "Protected important information before trying to solve the problem."
      },
      {
        "id": "q5-a",
        "text": "Try the quickest reversible fix and see what happens.",
        "score": {
          "A": 2,
          "R": 1
        },
        "evidence": "Tested a practical fix that could easily be undone."
      },
      {
        "id": "q5-r",
        "text": "Ask a friend who’s good with technology to look at it with me.",
        "score": {
          "R": 2,
          "I": 1
        },
        "evidence": "Brought another person into solving the problem."
      }
    ]
  },
  {
    "id": "q6",
    "number": 6,
    "gallery": "Earth & Space",
    "title": "Same film, different view",
    "prompt": "You and a friend watch the same film. You love it; they don’t. What do you do next?",
    "intro": "Same film, two completely different reviews. That happens a lot here.",
    "choices": [
      {
        "id": "q6-i",
        "text": "Compare the scenes and details that each of us noticed most.",
        "score": {
          "I": 2,
          "R": 1
        },
        "evidence": "Explored the observations behind different impressions."
      },
      {
        "id": "q6-c",
        "text": "Leave it there. We can keep our different opinions without settling it.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Preserved separate accounts without forcing resolution."
      },
      {
        "id": "q6-a",
        "text": "Choose another film together and see whether our opinions line up next time.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Used another experience to move beyond the disagreement."
      },
      {
        "id": "q6-r",
        "text": "Ask what made the film land so differently for them.",
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
    "title": "A familiar place changes",
    "prompt": "A café, club or community space you love is getting a major redesign. What would you speak up for first?",
    "intro": "Here’s the old layout, and here’s the new one. They moved nearly everything.",
    "choices": [
      {
        "id": "q7-i",
        "text": "Explain what problem the redesign is meant to solve.",
        "score": {
          "I": 2,
          "A": 1
        },
        "evidence": "Asked for the purpose and evidence behind a change."
      },
      {
        "id": "q7-c",
        "text": "Keep one familiar feature that makes the place feel like itself.",
        "score": {
          "C": 2,
          "R": 1
        },
        "evidence": "Protected a specific source of continuity."
      },
      {
        "id": "q7-a",
        "text": "Try the new layout for a while before making it permanent.",
        "score": {
          "A": 2,
          "C": 1
        },
        "evidence": "Favoured a practical, reversible trial."
      },
      {
        "id": "q7-r",
        "text": "Let the regulars and staff help shape the redesign.",
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
    "title": "One extra thing",
    "prompt": "You’re taking a day trip somewhere new with friends. The basics are packed. What extra do you bring?",
    "intro": "Everything we need is packed! There’s a little space left. Anything you’d like to bring?",
    "choices": [
      {
        "id": "q8-i",
        "text": "A guide or saved list, so we can understand what we find.",
        "score": {
          "I": 2,
          "R": 1
        },
        "evidence": "Brought a resource for interpreting discoveries together."
      },
      {
        "id": "q8-c",
        "text": "A notebook, so the little details don’t disappear when the day ends.",
        "score": {
          "C": 2,
          "I": 1
        },
        "evidence": "Made room to retain details beyond the moment."
      },
      {
        "id": "q8-a",
        "text": "A map with a few optional detours marked, in case something catches my eye.",
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

// The editable quiz and p5 scene helpers stay in this file. The large
// React/Three renderer is loaded separately so p5's parser does not choke.
(function openMuseum() {
  const host = document.getElementById('museum') || document.body.appendChild(document.createElement('div'));
  host.id = 'museum';
  host.textContent = 'Opening the museum…';

  const style = document.createElement('link');
  style.rel = 'stylesheet';
  style.href = 'https://personality-quiz-abraham.vercel.app/p5-runtime.css?v=20261106-1';
  document.head.appendChild(style);

  const script = document.createElement('script');
  script.src = 'https://personality-quiz-abraham.vercel.app/p5-runtime.js?v=20261106-1';
  script.onload = () => host.removeAttribute('aria-busy');
  script.onerror = () => {
    host.textContent = 'The museum could not open.';
    console.error('Museum runtime failed to load.');
  };
  host.setAttribute('aria-busy', 'true');
  document.body.appendChild(script);
})();
