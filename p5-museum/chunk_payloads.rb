#!/usr/bin/env ruby

path = File.expand_path('web-editor-p5-safe.js', __dir__)
source = File.read(path)

source = source.gsub(/await unpack\('([A-Za-z0-9+\/=]+)'\)/) do
  chunks = Regexp.last_match(1).scan(/.{1,1000}/)
  "await unpack([\n" + chunks.map { |chunk| "    '#{chunk}'" }.join(",\n") + "\n  ].join(''))"
end

File.write(path, source)
File.write(File.expand_path('upload/sketch.txt', __dir__), source)
