// Rebuild the standalone game bundle using the existing workspace dependencies.
import {build} from '../museum-site/node_modules/esbuild/lib/main.js';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('.',import.meta.url));
await build({
  absWorkingDir:root,entryPoints:['src/main.jsx'],outfile:'museum.js',
  bundle:true,minify:true,jsx:'automatic',legalComments:'eof',
  nodePaths:[fileURLToPath(new URL('../museum-site/node_modules',import.meta.url))],
  external:['assets/*'],define:{'process.env.NODE_ENV':'"production"'}
});
