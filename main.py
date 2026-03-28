from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = []
reviews = []

@app.get("/")
def home():
    return {"message": "API working"}

# 🔐 Register
@app.post("/register")
def register(user: dict):
    user["trust_score"] = 50
    users.append(user)
    return {"message": "User registered"}

# 🔐 Login
@app.post("/login")
def login(data: dict):
    for u in users:
        if u["phone"] == data["phone"]:
            return {"message": "Login success", "user": u}
    return {"message": "User not found"}

# 👤 Get user
@app.get("/user/{phone}")
def get_user(phone: str):
    for u in users:
        if u["phone"] == phone:
            return u
    return {"detail": "Not Found"}

# 💬 Add review
@app.post("/review")
def add_review(review: dict):
    reviews.append(review)

    for u in users:
        if u["phone"] == review["phone"]:
            if review["rating"] >= 4:
                u["trust_score"] += 5
            else:
                u["trust_score"] -= 5

    return {"message": "Review added"}

# 💬 Get reviews
@app.get("/reviews/{phone}")
def get_reviews(phone: str):
    return [r for r in reviews if r["phone"] == phone]