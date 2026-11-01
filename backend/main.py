from fastapi import FastAPI

app = FastAPI(
    title="NEMESIS Backend",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

@app.get("/health")
def health():
    return {
        "status": "online",
        "service": "NEMESIS Backend",
        "version": "0.1.0"
    }

from auth_api import router as auth_router,init as init_auth
from registration_api import router as registration_router
from registration_store import init as init_registration
init_auth()
init_registration()
app.include_router(auth_router)
app.include_router(registration_router)

# NEMESIS Phase 3A: Firebase instance inventory and assigned-customer status
from firebase_pool import init as init_firebase_pool
from firebase_api import router as firebase_router
init_firebase_pool()
import firebase_gateway
app.include_router(firebase_router)
