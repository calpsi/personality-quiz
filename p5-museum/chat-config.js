// This file is public. Only the Vercel function reads the OpenAI key.
// Testers can use written dialogue by cancelling the pass prompt.
window.MUSEUM_CHAT_ENDPOINT = 'https://personality-quiz-abraham.vercel.app/api/abraham';
window.museumTestPass = async function () {
  try {
    const saved = sessionStorage.getItem('museum-test-pass');
    if (saved) return saved;
  } catch {}
  const dialog = document.createElement('dialog');
  dialog.innerHTML = '<form method="dialog"><label>Museum testing pass <input type="password" autocomplete="off"></label> <button value="live">Talk live</button> <button value="written">Use written dialogue</button></form>';
  document.body.append(dialog);
  const closed = new Promise(resolve => dialog.addEventListener('close', resolve, {once:true}));
  dialog.showModal();
  await closed;
  const pass = dialog.returnValue === 'live' ? dialog.querySelector('input').value.trim() : '';
  dialog.remove();
  if (pass) {
    try { sessionStorage.setItem('museum-test-pass', pass); } catch {}
  }
  return pass;
};
