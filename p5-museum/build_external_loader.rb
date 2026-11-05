#!/usr/bin/env ruby
require 'json'

ROOT = File.expand_path('..', __dir__)
P5_ROOT = __dir__
PUBLIC_ROOT = File.join(ROOT, 'museum-site', 'public')
ASSET_ROOT = 'https://cdn.jsdelivr.net/gh/calpsi/personality-quiz@main/museum-site/public/assets/'
RUNTIME_ROOT = 'https://personality-quiz-abraham.vercel.app/'

def absolute_assets(source)
  source
    .gsub(%r{(?<![\w:/.-])assets/}, ASSET_ROOT)
    .gsub(%r{url\((['"]?)assets/}) { "url(#{$1}#{ASSET_ROOT}" }
end

def inject_questions(source, questions)
  replacement = "  questions: #{JSON.pretty_generate(questions)}\n};"
  pattern = /  questions: .*?\n};(?=\n\n\/\/ Turn)/m
  raise 'Could not find the editable question block.' unless source.match?(pattern)
  source.sub(pattern, replacement)
end

runtime = absolute_assets(File.read(File.join(P5_ROOT, 'museum.js')))
styles = absolute_assets(File.read(File.join(P5_ROOT, 'museum.css')))
File.write(File.join(PUBLIC_ROOT, 'p5-runtime.js'), runtime)
File.write(File.join(PUBLIC_ROOT, 'p5-runtime.css'), styles)

questions = JSON.parse(File.read(File.join(P5_ROOT, 'src', 'lib', 'questions.json')))
[
  File.join(ROOT, 'museum-site', 'lib', 'copy.json'),
  File.join(P5_ROOT, 'src', 'lib', 'copy.json')
].each do |copy_path|
  copy = JSON.parse(File.read(copy_path))
  questions.each do |entry|
    number = entry.fetch('number')
    copy["Q#{number}-INTRO"] = entry.fetch('intro')
    copy[entry.fetch('id')] = entry.fetch('prompt')
    entry.fetch('choices').each do |answer|
      copy[answer.fetch('id')] = answer.fetch('text')
      copy["#{answer.fetch('id')}-evidence"] = answer.fetch('evidence')
    end
  end
  File.write(copy_path, JSON.pretty_generate(copy) + "\n")
end
safe_path = File.join(P5_ROOT, 'web-editor-p5-safe.js')
safe_source = inject_questions(File.read(safe_path), questions)
File.write(safe_path, safe_source)
sketch_path = File.join(P5_ROOT, 'sketch.js')
File.write(sketch_path, inject_questions(File.read(sketch_path), questions))
editable = safe_source.split('// p5-safe app loader:', 2).first.rstrip
loader = <<~JAVASCRIPT


  // The editable quiz and p5 scene helpers stay in this file. The large
  // React/Three renderer is loaded separately so p5's parser does not choke.
  (function openMuseum() {
    const host = document.getElementById('museum') || document.body.appendChild(document.createElement('div'));
    host.id = 'museum';
    host.textContent = 'Opening the museum\u2026';

    const style = document.createElement('link');
    style.rel = 'stylesheet';
    style.href = '#{RUNTIME_ROOT}p5-runtime.css?v=20261105-2';
    document.head.appendChild(style);

    const script = document.createElement('script');
    script.src = '#{RUNTIME_ROOT}p5-runtime.js?v=20261105-2';
    script.onload = () => host.removeAttribute('aria-busy');
    script.onerror = () => {
      host.textContent = 'The museum could not open.';
      console.error('Museum runtime failed to load.');
    };
    host.setAttribute('aria-busy', 'true');
    document.body.appendChild(script);
  })();
JAVASCRIPT

sketch = editable + loader
File.write(File.join(P5_ROOT, 'web-editor-external.js'), sketch)
File.write(File.join(P5_ROOT, 'upload', 'sketch.txt'), sketch)
