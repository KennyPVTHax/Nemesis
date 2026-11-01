"""Narrow tenant-derived gateway. No device, SMS, monitoring or arbitrary Firebase paths."""
import os
from fastapi import Depends,HTTPException,Response
from pydantic import BaseModel,Field,ConfigDict
from account_store import connect
from auth_api import current_user
from firebase_api import router
from firebase_pool import approved_url
from firebase_cloud import GoogleFirebase
import firebase_config as cfg

class Preferences(BaseModel):
    model_config=ConfigDict(extra='forbid')
    theme:str=Field(max_length=40,pattern=r'^[A-Za-z0-9_-]*$')
    locale:str=Field(max_length=20,pattern=r'^[A-Za-z0-9_-]*$')

def context(user):
    if not cfg.enabled() or os.environ.get('NEMESIS_FIREBASE_GATEWAY_ENABLED')!='1':raise HTTPException(503,'Firebase gateway unavailable')
    if user[3]!='user':raise HTTPException(403,'Customer account required')
    url=approved_url(user[0])
    if not url:raise HTTPException(403,'Approved verified assignment required')
    with connect() as db:
        r=db.execute('SELECT m.alias,m.resource FROM firebase_instances i JOIN firebase_manager_instances m ON m.instance_id=i.id WHERE i.assigned_user_id=?',(user[0],)).fetchone()
    try:
        p=cfg.profile(r[0]);url,dbid,region=cfg.identity(url)
        if r[1]!=f'projects/{p["project_number"]}/locations/{region}/instances/{dbid}':raise ValueError()
        return url,p
    except Exception:raise HTTPException(503,'Firebase configuration unavailable') from None

@router.get('/preferences')
def get_preferences(response:Response,user=Depends(current_user)):
    response.headers['Cache-Control']='no-store';url,p=context(user);provider=None
    try:
        provider=GoogleFirebase(p);provider.preflight();provider.validate(url);return {'preferences':provider.preferences(url)}
    except Exception:raise HTTPException(503,'Firebase operation unavailable') from None
    finally:
        if provider:provider.close()

@router.put('/preferences')
def put_preferences(body:Preferences,response:Response,user=Depends(current_user)):
    response.headers['Cache-Control']='no-store';url,p=context(user);provider=None
    try:
        provider=GoogleFirebase(p);provider.preflight();provider.validate(url);provider.preferences(url,body.model_dump(),write=True);return {'status':'saved'}
    except Exception:raise HTTPException(503,'Firebase operation unavailable') from None
    finally:
        if provider:provider.close()
