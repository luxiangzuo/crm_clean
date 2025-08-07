from fastapi import FastAPI
from hubspot.router import router as hubspot_router
from ai.router import router as ai_router

app = FastAPI()

app.include_router(hubspot_router)
app.include_router(ai_router)
