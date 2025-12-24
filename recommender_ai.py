import firebase_admin
from firebase_admin import firestore
import random

# دالة لتنظيف بيانات المنتج (Defensive Programming)
# هذه الدالة تحل مشكلة P004 التي رأيناها في الصورة (الاسم الفارغ)
def clean_product_data(doc_id, data):
    # 1. معالجة الاسم الفارغ أو غير الموجود
    product_name = data.get('name', '')
    if not product_name or product_name.strip() == "":
        # إذا الاسم فارغ، نستخدم التصنيف كاسم مؤقت
        category = data.get('category', 'Product')
        product_name = f"{category} Item"

    # 2. معالجة السعر (إذا كان null نعتبره 0)
    price = data.get('price', 0.0)
    if price is None:
        price = 0.0

    # 3. تجهيز الكائن النهائي لـ Flutter
    return {
        "id": doc_id,
        "name": product_name,  # الاسم بعد المعالجة
        "category": data.get('category', 'General'),
        "price": float(price),
        "image_url": data.get('image_url', ''), # رابط صورة فارغ إذا لم يوجد
        "rating": float(data.get('rating', 0.0)),
        "description": data.get('description', 'No description available')
    }

def get_recommendations(user_id, db):
    print(f"--- جاري حساب التوصيات للمستخدم: {user_id} ---")
    
    recommendations = []
    
    try:
        # 1. جلب كل المنتجات من Firebase
        products_ref = db.collection('products')
        docs = products_ref.stream()
        
        all_products = []
        for doc in docs:
            # ننظف كل منتج فوراً
            clean_item = clean_product_data(doc.id, doc.to_dict())
            all_products.append(clean_item)

        # 2. المنطق البسيط للتوصية
        # نرتب المنتجات حسب التقييم (الأعلى أولاً) لضمان ظهور أفضل المنتجات
        sorted_products = sorted(all_products, key=lambda x: x['rating'], reverse=True)
        
        # نأخذ أول 5 منتجات فقط
        recommendations = sorted_products[:5]

    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []

    return recommendations