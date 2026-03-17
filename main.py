from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend running with uv"}

@app.get("/users")
def get_users():
    return {"message": "This is the users thing "}