"""
🎯 نظام التوصيات مع Firebase - إصدار Windows
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

# ===== 1. استيراد Firebase =====
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # تحميل مفتاح Firebase
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("[SUCCESS] Firebase key loaded")
    FIREBASE_CONNECTED = True
    
except Exception as e:
    print(f"[WARNING] Firebase not connected: {e}")
    print("[INFO] Running in local mode")
    db = None
    FIREBASE_CONNECTED = False

# ===== 2. إنشاء تطبيق FastAPI =====
app = FastAPI(
    title="Smart Recommendation System",
    description="نظام توصيات مع Firebase",
    version="2.0"
)

# ===== 3. بيانات محلية احتياطية =====
LOCAL_USERS = [
    {"id": "user1", "name": "Ahmed", "interests": ["Education", "Tech"]},
    {"id": "user2", "name": "Sara", "interests": ["Music", "Fashion"]},
    {"id": "user3", "name": "Mohammed", "interests": ["Electronics", "Fitness"]}
]

LOCAL_ITEMS = [
    {"id": "1", "title": "Python Tutorial", "category": "Education", "views": 150},
    {"id": "2", "title": "Gaming Laptop", "category": "Electronics", "views": 200},
    {"id": "3", "title": "Pop Music Mix", "category": "Music", "views": 300},
    {"id": "4", "title": "Fitness Course", "category": "Fitness", "views": 120},
    {"id": "5", "title": "Smartphone Review", "category": "Tech", "views": 180}
]

# ===== 4. دوال Firebase =====
def get_firebase_users():
    """جلب المستخدمين من Firebase"""
    if not FIREBASE_CONNECTED:
        return LOCAL_USERS
    
    try:
        users_ref = db.collection('users')
        docs = users_ref.limit(20).stream()
        
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
        
        return users if users else LOCAL_USERS
    except:
        return LOCAL_USERS

def get_firebase_items():
    """جلب العناصر من Firebase"""
    if not FIREBASE_CONNECTED:
        return LOCAL_ITEMS
    
    try:
        items_ref = db.collection('items')
        docs = items_ref.limit(30).stream()
        
        items = []
        for doc in docs:
            item_data = doc.to_dict()
            item_data['id'] = doc.id
            items.append(item_data)
        
        return items if items else LOCAL_ITEMS
    except:
        return LOCAL_ITEMS

# ===== 5. خوارزمية التوصيات =====
def get_trending_items(limit: int = 5):
    """العناصر الرائجة"""
    items = get_firebase_items()
    
    sorted_items = sorted(items, key=lambda x: x.get('views', 0), reverse=True)
    
    trending = []
    for i, item in enumerate(sorted_items[:limit], 1):
        score = item.get('views', 0)
        trending.append({
            "rank": i,
            "item": item['title'],
            "category": item['category'],
            "score": score
        })
    
    return trending

# ===== 6. نهايات API =====
@app.get("/")
def home():
    """الصفحة الرئيسية"""
    return {
        "message": "Welcome to Recommendation System",
        "firebase": "connected" if FIREBASE_CONNECTED else "local",
        "endpoints": {
            "/": "This page",
            "/users": "All users",
            "/items": "All items",
            "/recommend/{user_id}": "Recommendations",
            "/trending": "Trending items",
            "/status": "System status"
        }
    }

@app.get("/status")
def system_status():
    """حالة النظام"""
    users = get_firebase_users()
    items = get_firebase_items()
    
    return {
        "status": "online",
        "firebase": FIREBASE_CONNECTED,
        "users_count": len(users),
        "items_count": len(items),
        "trending_count": len(get_trending_items(3))
    }

@app.get("/users")
def get_users():
    """جميع المستخدمين"""
    users = get_firebase_users()
    return {
        "source": "firebase" if FIREBASE_CONNECTED else "local",
        "count": len(users),
        "users": users
    }

@app.get("/items")
def get_items(category: Optional[str] = None):
    """جميع العناصر"""
    items = get_firebase_items()
    
    if category:
        filtered = [item for item in items if item.get('category') == category]
        return {
            "category": category,
            "count": len(filtered),
            "items": filtered
        }
    
    return {
        "count": len(items),
        "items": items
    }

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str, limit: int = 5):
    """توصيات للمستخدم"""
    users = get_firebase_users()
    items = get_firebase_items()
    
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_interests = user.get('interests', [])
    
    if user_interests:
        recommendations = []
        for interest in user_interests:
            interest_items = [item for item in items if item.get('category') == interest]
            recommendations.extend(interest_items[:2])
    else:
        recommendations = random.sample(items, min(limit, len(items)))
    
    unique_recs = []
    seen_ids = set()
    for item in recommendations:
        if item['id'] not in seen_ids and len(unique_recs) < limit:
            seen_ids.add(item['id'])
            unique_recs.append(item)
    
    return {
        "user_id": user_id,
        "user_name": user.get('name', 'Unknown'),
        "recommendations": unique_recs,
        "count": len(unique_recs),
        "source": "firebase" if FIREBASE_CONNECTED else "local"
    }

@app.get("/trending")
def get_trending(limit: int = 5):
    """العناصر الرائجة"""
    trending = get_trending_items(limit)
    
    print("\n" + "=" * 50)
    print("TRENDING ITEMS:")
    print("=" * 50)
    
    for item in trending:
        print(f"{item['rank']}. {item['item']} (Views: {item['score']})")
    
    print("=" * 50 + "\n")
    
    return {
        "count": len(trending),
        "trending": trending
    }

# ===== 7. التشغيل =====
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("SMART RECOMMENDATION SYSTEM")
    print("=" * 50)
    
    if FIREBASE_CONNECTED:
        print("[SUCCESS] Firebase: CONNECTED")
    else:
        print("[WARNING] Firebase: NOT CONNECTED (Local Mode)")
    
    trending = get_trending_items(3)
    if trending:
        print("\nTRENDING NOW:")
        for item in trending:
            print(f"   {item['rank']}. {item['item']}")
    
    print("=" * 50)
    print("SERVER: http://127.0.0.1:8000")
    print("DOCS: http://127.0.0.1:8000/docs")
    print("STOP: Ctrl+C")
    print("=" * 50 + "\n")
    
    # 🔥 الحل: اضف quotes حول main:app أو خلي reload=False
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)