#!/usr/bin/env python3
"""Run locally in Terminal; never paste API keys into chat or source code."""
from pathlib import Path
import getpass,os,re
root=Path(__file__).resolve().parents[1]
target=root/'.env.local'
print('This saves OPENAI_API_KEY to '+str(target)+' (ignored by Git).')
if input('Save your existing key here? [y/N] ').lower()!='y': raise SystemExit('Cancelled.')
if target.is_symlink():raise SystemExit('Refusing a symlink destination.')
key=getpass.getpass('Existing OpenAI API key (hidden): ').strip()
if not key.startswith('sk-') or any(c.isspace() for c in key):raise SystemExit('That does not look like an API key; nothing saved.')
old=target.read_text() if target.exists() else ''
lines=[line for line in old.splitlines() if not re.match(r'^\s*OPENAI_API_KEY\s*=',line)]
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f:f.write('\n'.join(lines+['OPENAI_API_KEY='+key])+'\n')
os.chmod(target,0o600)
print('Saved securely. Restart the local development server. This does not configure hosted production secrets.')
