// main.js - common functions used across pages
function qs(sel){return document.querySelector(sel)}
function qsa(sel){return document.querySelectorAll(sel)}
// show toast (simple)
function toast(msg, time=2500){
  let t = document.createElement('div')
  t.textContent = msg
  Object.assign(t.style, {
    position:'fixed', right:'20px', bottom:'20px', background:'#0b1320', padding:'10px 14px',
    borderRadius:'8px', boxShadow:'0 6px 18px rgba(0,0,0,0.6)', color:'white', zIndex:9999
  })
  document.body.appendChild(t)
  setTimeout(()=>t.style.opacity=0, time-400)
  setTimeout(()=>t.remove(), time)
}

// helper for fetch with JSON error handling
async function postJSON(url, data){
  const res = await fetch(url, {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)
  })
  if(!res.ok) throw new Error('Network response not ok')
  return res.json()
}
