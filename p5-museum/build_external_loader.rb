#!/usr/bin/env ruby

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

runtime = absolute_assets(File.read(File.join(P5_ROOT, 'museum.js')))
styles = absolute_assets(File.read(File.join(P5_ROOT, 'museum.css')))
File.write(File.join(PUBLIC_ROOT, 'p5-runtime.js'), runtime)
File.write(File.join(PUBLIC_ROOT, 'p5-runtime.css'), styles)

safe_source = File.read(File.join(P5_ROOT, 'web-editor-p5-safe.js'))
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
