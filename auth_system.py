import hashlib
import json
import os
from datetime import datetime

class AuthenticationSystem:
    def __init__(self, users_file="users_data.json"):
        self.users_file = users_file
        self.users = self.load_users()
        self.current_user = None
    
    def load_users(self):
        """تحميل المستخدمين من ملف JSON"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_users(self):
        """حفظ المستخدمين في ملف JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username, password, email=None):
        """تسجيل مستخدم جديد"""
        if username in self.users:
            return False, "اسم المستخدم موجود مسبقاً!"
        
        user_id = f"user_{len(self.users) + 1:03d}"
        
        self.users[username] = {
            "user_id": user_id,
            "password_hash": self.hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "profile": {
                "full_name": "",
                "age": None,
                "interests": [],
                "country": ""
            }
        }
        
        self.save_users()
        return True, f"تم تسجيل {username} بنجاح! (ID: {user_id})"
    
    def login(self, username, password):
        """تسجيل الدخول"""
        if username not in self.users:
            return False, "اسم المستخدم غير موجود!"
        
        user = self.users[username]
        
        if user["password_hash"] != self.hash_password(password):
            return False, "كلمة المرور غير صحيحة!"
        
        # تحديث وقت آخر دخول
        user["last_login"] = datetime.now().isoformat()
        self.save_users()
        
        self.current_user = {
            "username": username,
            "user_id": user["user_id"],
            "profile": user["profile"]
        }
        
        return True, f"مرحباً بعودتك {username}!"
    
    def logout(self):
        """تسجيل الخروج"""
        if self.current_user:
            username = self.current_user["username"]
            self.current_user = None
            return True, f"تم تسجيل خروج {username}"
        return False, "لا يوجد مستخدم مسجل دخول"
    
    def update_profile(self, username, **kwargs):
        """تحديث بيانات المستخدم"""
        if username not in self.users:
            return False, "المستخدم غير موجود"
        
        if "profile" in kwargs:
            self.users[username]["profile"].update(kwargs["profile"])
        else:
            self.users[username]["profile"].update(kwargs)
        
        self.save_users()
        return True, "تم تحديث الملف الشخصي"
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        return list(self.users.keys())