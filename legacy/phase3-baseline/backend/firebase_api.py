from fastapi import APIRouter,Depends,HTTPException,Response
from auth_api import current_user
from firebase_pool import summary,request_link,approved_url
router=APIRouter(prefix='/firebase',tags=['firebase'])

@router.get('/status')
def status(response:Response,user=Depends(current_user)):
    response.headers['Cache-Control']='no-store'
    if user[3]=='owner':return {'role':'owner','status':'owner_not_assigned'}
    return summary(user[0])

@router.post('/request-link')
def request(response:Response,user=Depends(current_user)):
    response.headers['Cache-Control']='no-store'
    if user[3]!='user':raise HTTPException(403,'Customer account required')
    state=request_link(user[0])
    if state=='not_eligible':raise HTTPException(403,'Customer subscription inactive')
    return {'status':state}

@router.get('/approved-link')
def approved(response:Response,user=Depends(current_user)):
    response.headers['Cache-Control']='no-store'
    if user[3]!='user':raise HTTPException(403,'Customer account required')
    url=approved_url(user[0])
    if url is None:raise HTTPException(403,'Owner approval required')
    # Reveals only approved database URL, NEVER admin credentials.
    # Firebase Rules must enforce access independently of this API.
    return {'database_url':url}
