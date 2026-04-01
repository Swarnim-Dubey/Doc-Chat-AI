from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routes import router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)