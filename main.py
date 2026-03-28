from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from jose import jwt
from passlib.context import CryptContext

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
client = MongoClient("YOUR_MONGO_URL")
db = client["trustnet"]
users = db["users"]
reviews = db["reviews"]

# JWT
SECRET = "mysecretkey"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Register
@app.post("/register")
def register(user: dict):
    user["password"] = pwd_context.hash(user["password"])
    user["trust_score"] = 50
    users.insert_one(user)
    return {"message": "User registered"}

# Login
@app.post("/login")
def login(data: dict):
    user = users.find_one({"phone": data["phone"]})

    if not user or not pwd_context.verify(data["password"], user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"phone": user["phone"]}, SECRET)
    return {"token": token}

# Get user
@app.get("/user/{phone}")
def get_user(phone: str):
    user = users.find_one({"phone": phone}, {"_id": 0})
    if not user:
        return {"detail": "Not Found"}
    return user

# Add review
@app.post("/review")
def add_review(review: dict):
    reviews.insert_one(review)

    if review["rating"] >= 4:
        users.update_one({"phone": review["phone"]}, {"$inc": {"trust_score": 5}})
    else:
        users.update_one({"phone": review["phone"]}, {"$inc": {"trust_score": -5}})

    return {"message": "Review added"}

# Get reviews
@app.get("/reviews/{phone}")
def get_reviews(phone: str):
    return list(reviews.find({"phone": phone}, {"_id": 0}))

# 🤖 Simple AI Fraud Detection
@app.get("/fraud-check/{phone}")
def fraud_check(phone: str):
    user_reviews = list(reviews.find({"phone": phone}))
    
    bad = sum(1 for r in user_reviews if r["rating"] <= 2)
    total = len(user_reviews)

    if total == 0:
        return {"risk": "Unknown"}

    score = bad / total

    if score > 0.5:
        return {"risk": "High Risk 🚨"}
    elif score > 0.2:
        return {"risk": "Medium Risk ⚠️"}
    else:
        return {"risk": "Low Risk ✅"}