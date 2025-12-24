import os
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 1. إعداد التطبيق
app = FastAPI()

# 2. إعدادات CORS (ضرورية جداً عشان تطبيقك وفلاتر يقدروا يتصلوا بالسيرفر)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يسمح بالاتصال من أي مكان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. الاتصال بـ Firebase
# السيرفر سيبحث عن ملف المفتاح، تأكد أنه مرفوع معه
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

# 4. الرابط الرئيسي (Health Check)
@app.get("/")
def home():
    return {"status": "Online", "message": "AI Recommender Server is Running!"}

# 5. رابط التوصيات
@app.get("/recommend/{user_id}")
def recommend_products(user_id: str):
    try:
        # جلب بيانات المستخدم من Firestore
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {"status": "error", "message": "User not found in Database"}

        user_data = user_doc.to_dict()
        interests = user_data.get("interests", [])
        
        # فلترة المنتجات حسب الاهتمامات
        recommended_items = []
        if interests:
            recommended_items = [p for p in products_db if p["category"] in interests]
        
        # إذا لم نجد تطابق، نرجع منتجات افتراضية
        if not recommended_items:
            recommended_items = products_db[:3]

        return {
            "status": "success",
            "source": "Live Server Data",
            "user_id": user_id,
            "user_interests": interests,
            "recommendations": recommended_items
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# 6. تشغيل السيرفر (التعديل المهم للاستضافة)
if __name__ == "__main__":
    # يأخذ المنفذ من بيئة الاستضافة، أو يستخدم 8085 إذا كنت تجربه محلياً
    port = int(os.environ.get("PORT", 8085))
    uvicorn.run(app, host="0.0.0.0", port=port)