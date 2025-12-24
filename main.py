from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore
from recommender_ai import get_recommendations # استدعاء ملف الذكاء
import uvicorn

app = FastAPI()

# 1. الاتصال بـ Firebase
# تأكد أن اسم ملف المفتاح صحيح
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json") 
        firebase_admin.initialize_app(cred)
        print("✅ تم الاتصال بـ Firebase بنجاح")
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")

db = firestore.client()

# --- الرابط الرئيسي ---
@app.get("/")
def home():
    return {"message": "Flowmart AI Server is Ready!", "status": "Running"}

# --- رابط التوصية (المهم لـ Flutter) ---
@app.get("/recommend/{user_id}")
def recommend_products(user_id: str):
    print(f"📩 وصل طلب توصية للمستخدم: {user_id}")
    try:
        # استدعاء دالة التوصية من الملف الآخر
        products_list = get_recommendations(user_id, db)
        
        return {
            "status": "success",
            "user_id": user_id,
            "recommendations": products_list
        }
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التوصية: {e}")
        return {"status": "error", "message": str(e), "recommendations": []}

# تشغيل السيرفر على المنفذ 8081
if __name__ == "__main__":
    print("🚀 جاري تشغيل السيرفر على http://127.0.0.1:8081 ...")
    uvicorn.run(app, host="0.0.0.0", port=8081)