from fastapi import APIRouter,HTTPException,Response
from pydantic import BaseModel,Field
from registration_store import activate
router=APIRouter()
class Activation(BaseModel):
    token:str=Field(min_length=1,max_length=150)
    password:str=Field(min_length=1,max_length=256)
@router.post('/register/activate')
def register(body:Activation,response:Response):
    response.headers['Cache-Control']='no-store'
    ok,message=activate(body.token,body.password)
    if not ok:raise HTTPException(400,message)
    return {'status':'activated','message':message}
@router.get('/register/',response_class=__import__('fastapi').responses.HTMLResponse)
def page():
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><title>NEMESIS registration</title><style>body{font:16px system-ui;background:#11121b;color:white;max-width:440px;margin:10vh auto;padding:20px}input,button{box-sizing:border-box;width:100%;padding:14px;margin:10px 0;border-radius:8px}button{background:#b21b32;color:white;border:0}input{background:#222435;color:white;border:1px solid #777}</style></head><body><h1>NEMESIS</h1><p>Create your account password</p><form id="f"><input id="p" type="password" minlength="12" maxlength="256" autocomplete="new-password" required placeholder="Password (12+ characters)"><input id="c" type="password" minlength="12" maxlength="256" autocomplete="new-password" required placeholder="Confirm password"><button>Create account</button></form><p id="msg" role="status"></p><script>const token=location.hash.slice(1);history.replaceState(null,'',location.pathname);document.getElementById('f').onsubmit=async e=>{e.preventDefault();const p=document.getElementById('p').value,c=document.getElementById('c').value,m=document.getElementById('msg');if(p!==c){m.textContent='Passwords do not match';return}try{const r=await fetch('/register/activate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token,password:p}),cache:'no-store'});const j=await r.json();m.textContent=r.ok?'Account activated. You can now log in.':(j.detail||'Activation failed');if(r.ok)document.getElementById('f').remove()}catch(_){m.textContent='Connection error'}};</script></body></html>'''
