import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# إعدادات CORS عشان التطبيق يحكي مع السيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# الاتصال بـ Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# بيانات المنتجات (مؤقتة)
products_db = [
    {"id": "1", "name": "Gaming Laptop HP", "category": "tech", "price": 1200.0},
    {"id": "2", "name": "Wireless Mouse", "category": "tech", "price": 25.0},
    {"id": "3", "name": "Men T-Shirt", "category": "fashion", "price": 15.0},
    {"id": "4", "name": "Running Shoes", "category": "fashion", "price": 50.0},
    {"id": "5", "name": "iPhone 15 Case", "category": "tech", "price": 15.0},
    {"id": "6", "name": "Smart Watch", "category": "tech", "price": 200.0},
]

@app.get("/")
def home():
    return {"status": "Running", "message": "Server is up!"}

@app.get("/recommend/{user_id}")
def recommend_products(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {"status": "error", "message": "User not found"}

        user_data = user_doc.to_dict()
        interests = user_data.get("interests", [])
        
        recommended_items = []
        if interests:
            recommended_items = [p for p in products_db if p["category"] in interests]
        
        if not recommended_items:
            recommended_items = products_db[:3]

        return {
            "status": "success",
            "source": "Offline Data",
            "user_id": user_id,
            "recommendations": recommended_items
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # هذا الكود اللي زبط معك محلياً
    uvicorn.run(app, host="0.0.0.0", port=8085)