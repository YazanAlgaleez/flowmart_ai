import os
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 1. إعداد التطبيق
app = FastAPI()

# 2. إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. الاتصال بـ Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

db = firestore.client()

# --- بيانات المنتجات (الاحتياطية) ---
products_db = [
    {"id": "1", "name": "Gaming Laptop HP", "category": "tech", "price": 1200.0},
    {"id": "2", "name": "Wireless Mouse", "category": "tech", "price": 25.0},
    {"id": "3", "name": "Men T-Shirt", "category": "fashion", "price": 15.0},
    {"id": "4", "name": "Running Shoes", "category": "fashion", "price": 50.0},
    {"id": "5", "name": "iPhone 15 Case", "category": "tech", "price": 15.0},
    {"id": "6", "name": "Smart Watch", "category": "tech", "price": 200.0},
]

# 4. الرابط الرئيسي
@app.get("/")
def home():
    return {"status": "Online", "message": "AI Recommender Server is Running!"}

# 5. رابط التوصيات (النسخة الذكية والمعدلة)
@app.get("/recommend/{user_id}")
def recommend_products(user_id: str):
    try:
        # أ. جلب بيانات المستخدم من Firestore
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {"status": "error", "message": "User not found in Database"}

        user_data = user_doc.to_dict()
        
        # ب. تنظيف الاهتمامات (تحويلها لحروف صغيرة وإزالة المسافات)
        raw_interests = user_data.get("interests", [])
        clean_interests = []
        
        # نتأكد أنها قائمة وننظف كل كلمة فيها
        if isinstance(raw_interests, list):
            clean_interests = [str(i).lower().strip() for i in raw_interests]
        
        # ج. فلترة المنتجات (مقارنة ذكية تتجاهل حالة الأحرف)
        recommended_items = []
        if clean_interests:
            recommended_items = [
                p for p in products_db 
                if p["category"].lower() in clean_interests
            ]
        
        # د. الخطة البديلة: إذا لم نجد تطابق نرجع منتجات افتراضية
        if not recommended_items:
            recommended_items = products_db[:3]

        # هـ. الرد مع معلومات التصحيح لنعرف السبب
        return {
            "status": "success",
            "source": "Live Server Data",
            "user_id": user_id,
            "found_interests_in_db": raw_interests,  # شو لقينا في الداتا بيس
            "cleaned_interests": clean_interests,    # شو فهم الكود
            "recommendations": recommended_items
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# 6. تشغيل السيرفر
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run(app, host="0.0.0.0", port=port)