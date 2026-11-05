import {contextFor, instructions} from '../museum-site/lib/abraham.mjs';

window.askAbrahamDirect = async function (body) {
  const key = window.ABRAHAM_API_KEY?.trim();
  if (!key) throw Error('Abraham’s live chat hasn’t opened yet.');
  const response = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {'Content-Type':'application/json', Authorization:'Bearer '+key},
    signal: AbortSignal.timeout(30000),
    body: JSON.stringify({model:'gpt-4.1-mini', instructions, input:JSON.stringify(contextFor(body)), max_output_tokens:300, store:false})
  });
  if (response.status === 401 || response.status === 403) {
    throw Error('Abraham’s live chat is unavailable. Please try again later.');
  }
  if (response.status === 429) throw Error('Abraham’s live chat is busy. Please try again later.');
  if (!response.ok) throw Error('Abraham couldn’t connect ('+response.status+'). Please try again.');
  const data = await response.json();
  const text = (data.output || []).filter(item => item.type === 'message').flatMap(item => item.content || []).filter(part => part.type === 'output_text').map(part => part.text).join('').trim();
  if (!text) throw Error('No reply came through. Please try again.');
  return {source:'ai',text};
};
