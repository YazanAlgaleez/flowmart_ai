import os
import random  # مكتبة العشوائية
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

db = firestore.client()

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
    return {"status": "Online", "message": "AI Recommender Server is Running!"}

@app.get("/recommend/{user_id}")
def recommend_products(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        interests = []
        if user_doc.exists:
            user_data = user_doc.to_dict()
            raw_interests = user_data.get("interests", [])
            if isinstance(raw_interests, list):
                interests = [str(i).lower().strip() for i in raw_interests]

        recommended_items = []
        if interests:
            recommended_items = [
                p for p in products_db 
                if p["category"].lower() in interests
            ]

        # --- التعديل الذي طلبته (عشوائي) ---
        if not recommended_items:
            # يختار 3 منتجات عشوائية بدلاً من أول 3
            # min يضمن عدم حدوث خطأ لو كان عدد المنتجات أقل من 3
            count = min(len(products_db), 3)
            recommended_items = random.sample(products_db, count)

        return {
            "status": "success",
            "source": "Live Server Data",
            "user_id": user_id,
            "found_interests": interests,
            "recommendations": recommended_items
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run(app, host="0.0.0.0", port=port)