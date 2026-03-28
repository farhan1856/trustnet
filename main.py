from fastapi import FastAPI

app = FastAPI()

users = []

@app.get("/")
def home():
    return {"message": "API working"}

@app.post("/register")
def register(user: dict):
    users.append(user)
    return {"message": "User added"}

@app.get("/user/{phone}")
def get_user(phone: str):
    for u in users:
        if u["phone"] == phone:
            return u
    return {"detail": "Not Found"}