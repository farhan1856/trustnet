from fastapi import FastAPI

app = FastAPI()

users = []

@app.get("/")
def home():
    return {"message": "API working"}

# Register user with trust score
@app.post("/register")
def register(user: dict):
    user["trust_score"] = 50   # default score
    users.append(user)
    return {"message": "User added", "user": user}

# Get user by phone
@app.get("/user/{phone}")
def get_user(phone: str):
    for u in users:
        if u["phone"] == phone:
            return u
    return {"detail": "Not Found"}

# Increase trust score
@app.post("/trust/increase/{phone}")
def increase_trust(phone: str):
    for u in users:
        if u["phone"] == phone:
            u["trust_score"] += 10
            return {"message": "Trust increased", "trust_score": u["trust_score"]}
    return {"detail": "User not found"}

# Decrease trust score
@app.post("/trust/decrease/{phone}")
def decrease_trust(phone: str):
    for u in users:
        if u["phone"] == phone:
            u["trust_score"] -= 10
            return {"message": "Trust decreased", "trust_score": u["trust_score"]}
    return {"detail": "User not found"}