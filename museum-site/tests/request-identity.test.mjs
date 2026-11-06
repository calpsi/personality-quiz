import test from 'node:test';
import assert from 'node:assert/strict';
import {isSameSiteRequest,publicVisitorId} from '../lib/request-identity.mjs';

test('public visitor buckets are stable and do not expose the raw address',()=>{
  const headers=new Headers({'x-forwarded-for':'203.0.113.42, 10.0.0.1','user-agent':'Museum Test'});
  const first=publicVisitorId(headers),second=publicVisitorId(headers);
  assert.equal(first,second);
  assert.match(first,/^web-[a-z0-9]+$/);
  assert.doesNotMatch(first,/203\.0\.113\.42/);
});

test('public conversation accepts its own site and rejects cross-site browser calls',()=>{
  const same=new Request('https://museum.example/api/abraham',{headers:{origin:'https://museum.example','sec-fetch-site':'same-origin'}});
  const cross=new Request('https://museum.example/api/abraham',{headers:{origin:'https://elsewhere.example','sec-fetch-site':'cross-site'}});
  assert.equal(isSameSiteRequest(same),true);
  assert.equal(isSameSiteRequest(cross),false);
});
