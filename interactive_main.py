import random
import sys
import io
from recommender import SmartRecommender
from auth_system import AuthenticationSystem

# إصلاح encoding للعربية
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class InteractiveRecommendationApp:
    def __init__(self):
        self.auth = AuthenticationSystem()
        self.recommender = SmartRecommender()
        self.load_existing_users()
    
    def load_existing_users(self):
        """تحميل المستخدمين المسجلين مسبقاً"""
        for username, user_data in self.auth.users.items():
            user_id = user_data["user_id"]
            self.recommender.add_user(user_id, username)
    
    def display_menu(self):
        """عرض القائمة الرئيسية"""
        print("\n" + "="*50)
        print("نظام التوصية الذكي التفاعلي")
        print("="*50)
        
        if self.auth.current_user:
            print(f"المستخدم الحالي: {self.auth.current_user['username']}")
            print("1. عرض التوصيات")
            print("2. تصفح المحتوى")
            print("3. تفاعل مع محتوى عشوائي")
            print("4. احصائياتي")
            print("5. تحديث الملف الشخصي")
            print("6. تسجيل الخروج")
            print("7. خروج من البرنامج")
        else:
            print("1. تسجيل جديد")
            print("2. تسجيل الدخول")
            print("3. تصفح كمزور")
            print("4. خروج من البرنامج")
        
        print("="*50)
    
    def register_user(self):
        """تسجيل مستخدم جديد"""
        print("\nتسجيل مستخدم جديد")
        print("-"*30)
        
        username = input("اسم المستخدم: ").strip()
        password = input("كلمة المرور: ").strip()
        email = input("البريد الإلكتروني (اختياري): ").strip() or None
        
        success, message = self.auth.register(username, password, email)
        print(f"\n{'✅' if success else '❌'} {message}")
        
        if success:
            # إضافة المستخدم لنظام التوصية
            user_data = self.auth.users[username]
            self.recommender.add_user(user_data["user_id"], username)
            
            # جمع بيانات الملف الشخصي
            self.collect_profile_info(username)
    
    def collect_profile_info(self, username):
        """جمع معلومات الملف الشخصي"""
        print("\nاخبرنا المزيد عنك:")
        
        full_name = input("الاسم الكامل: ").strip()
        age = input("العمر: ").strip()
        country = input("البلد: ").strip()
        
        print("\nاختر اهتماماتك (ادخل الأرقام مفصولة بفاصلة):")
        categories = self.recommender.database.get_categories()
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        interests_input = input("\nاهتماماتك: ").strip()
        selected_interests = []
        
        if interests_input:
            try:
                indices = [int(x.strip()) - 1 for x in interests_input.split(',')]
                selected_interests = [categories[i] for i in indices if 0 <= i < len(categories)]
            except:
                print("❌ صيغة غير صحيحة. تم تخطي اختيار الاهتمامات.")
        
        # تحديث الملف الشخصي
        self.auth.update_profile(username,
            full_name=full_name,
            age=age if age else None,
            interests=selected_interests,
            country=country
        )
        
        # إضافة تفاعلات أولية بناء على الاهتمامات
        if selected_interests:
            self.add_initial_interactions(username, selected_interests)
        print("✅ تم حفظ معلومات الملف الشخصي")
    
    def add_initial_interactions(self, username, interests):
        """إضافة تفاعلات أولية بناء على اهتمامات المستخدم"""
        user_data = self.auth.users[username]
        user_id = user_data["user_id"]
        
        for interest in interests[:3]:  # أول 3 اهتمامات فقط
            items = self.recommender.database.get_items_by_category(interest)
            if items:
                # إضافة 2-3 تفاعلات لكل اهتمام
                for _ in range(random.randint(2, 3)):
                    item = random.choice(items)
                    action = random.choice(["view", "like"])
                    duration = random.randint(30, 120) if action == "watch" else None
                    self.recommender.record_interaction(user_id, item, action, duration)
        
        print("✅ تم إضافة تفاعلات أولية بناء على اهتماماتك")
    
    def login_user(self):
        """تسجيل دخول مستخدم"""
        print("\nتسجيل الدخول")
        print("-"*30)
        
        username = input("اسم المستخدم: ").strip()
        password = input("كلمة المرور: ").strip()
        
        success, message = self.auth.login(username, password)
        print(f"\n{'✅' if success else '❌'} {message}")
        
        return success
    
    def browse_content(self):
        """تصفح المحتوى المتاح"""
        print("\nتصفح المحتوى")
        print("-"*30)
        
        categories = self.recommender.database.get_categories()
        
        while True:
            print("\nالتصنيفات المتاحة:")
            for i, cat in enumerate(categories, 1):
                items_count = len(self.recommender.database.get_items_by_category(cat))
                print(f"{i}. {cat} ({items_count} عنصر)")
            print(f"{len(categories)+1}. العودة للقائمة الرئيسية")
            
            try:
                choice = int(input("\nاختر تصنيفاً: "))
                if 1 <= choice <= len(categories):
                    category = categories[choice-1]
                    self.show_category_items(category)
                elif choice == len(categories) + 1:
                    break
                else:
                    print("❌ اختيار غير صحيح")
            except ValueError:
                print("❌ الرجاء إدخال رقم")
    
    def show_category_items(self, category):
        """عرض عناصر تصنيف معين"""
        items = self.recommender.database.get_items_by_category(category)
        
        print(f"\nعناصر تصنيف '{category}':")
        print("-"*40)
        
        for i, item in enumerate(items, 1):
            info = self.recommender.database.items[item]
            tags = ", ".join(info["tags"][:3])  # أول 3 وسوم فقط
            difficulty = info.get("difficulty", "غير محدد")
            duration = info.get("duration_min", "غير معروف")
            
            print(f"{i}. {item}")
            print(f"   الصعوبة: {difficulty} | المدة: {duration} دقيقة")
            print(f"   الوسوم: {tags}")
            
            if self.auth.current_user:
                print(f"   [1] مشاهدة  [2] اعجاب  [3] مشاركة")
        
        if self.auth.current_user:
            self.handle_item_interaction(items, category)
    
    def handle_item_interaction(self, items, category):
        """معالجة تفاعل المستخدم مع عنصر"""
        try:
            item_choice = int(input("\nاختر رقم العنصر للتفاعل (0 للرجوع): "))
            if item_choice == 0:
                return
            
            if 1 <= item_choice <= len(items):
                item = items[item_choice-1]
                
                print(f"\nتفاعل مع: {item}")
                print("1. مشاهدة")
                print("2. اعجاب")
                print("3. مشاركة")
                print("4. رجوع")
                
                action_choice = input("\nاختر الإجراء: ").strip()
                
                actions = {"1": "watch", "2": "like", "3": "share"}
                
                if action_choice in actions:
                    action = actions[action_choice]
                    duration = None
                    
                    if action == "watch":
                        # استخدام المدة المخزنة إذا موجودة
                        item_info = self.recommender.database.items.get(item, {})
                        if "duration_min" in item_info:
                            duration = item_info["duration_min"] * 60  # تحويل للثواني
                        else:
                            duration = random.randint(60, 300)
                    
                    user_id = self.auth.current_user["user_id"]
                    self.recommender.record_interaction(user_id, item, action, duration)
                    
                    # تحديث الشعبية في قاعدة البيانات
                    if hasattr(self.recommender.database, 'update_popularity'):
                        self.recommender.database.update_popularity(item, action)
                    
                    print(f"✅ تم تسجيل تفاعل: {action} على {item}")
                elif action_choice == "4":
                    return
                else:
                    print("❌ اختيار غير صحيح")
            else:
                print("❌ رقم عنصر غير صحيح")
        except ValueError:
            print("❌ الرجاء إدخال رقم")
    
    def show_recommendations(self):
        """عرض التوصيات للمستخدم الحالي"""
        if not self.auth.current_user:
            print("❌ يجب تسجيل الدخول أولاً")
            return
        
        user_id = self.auth.current_user["user_id"]
        username = self.auth.current_user["username"]
        
        print(f"\nالتوصيات الشخصية لـ {username}")
        print("="*50)
        
        # عرض اهتمامات المستخدم
        user_profile = self.auth.users[username]["profile"]
        if user_profile.get("interests"):
            print(f"اهتماماتك: {', '.join(user_profile['interests'])}")
        
        # الحصول على التوصيات
        recs = self.recommender.recommend(user_id, num=8)
        
        if recs:
            print("\nنوصي لك بـ:")
            for i, rec in enumerate(recs, 1):
                if rec in self.recommender.database.items:
                    info = self.recommender.database.items[rec]
                    category = info["category"]
                    tags = ", ".join(info["tags"][:2])  # أول وسمين فقط
                    difficulty = info.get("difficulty", "")
                    
                    print(f"{i}. {rec}")
                    print(f"   التصنيف: {category} | الوسوم: {tags}")
                    if difficulty:
                        print(f"   الصعوبة: {difficulty}")
        else:
            print("🤔 لا توجد توصيات بعد. جرب التفاعل مع المزيد من المحتوى!")
        
        # العناصر الشائعة
        if hasattr(self.recommender, 'trending_items') and self.recommender.trending_items:
            print("\nالعناصر الشائعة حالياً:")
            for i, (item, score) in enumerate(self.recommender.trending_items[:3], 1):
                print(f"{i}. {item} (نقاط: {score})")
    
    def show_user_stats(self):
        """عرض إحصائيات المستخدم"""
        if not self.auth.current_user:
            print("❌ يجب تسجيل الدخول أولاً")
            return
        
        username = self.auth.current_user["username"]
        user_data = self.auth.users[username]
        user_id = user_data["user_id"]
        
        if user_id in self.recommender.users:
            user = self.recommender.users[user_id]
            
            print(f"\nاحصائيات {username}")
            print("="*40)
            print(f"تاريخ التسجيل: {user_data.get('created_at', 'غير معروف')[:10]}")
            print(f"عدد التفاعلات: {len(user.events)}")
            print(f"المشاهدات: {len(user.watch_history)}")
            print(f"الاهتمامات: {', '.join(user.interests) if user.interests else 'لم تكتشف بعد'}")
            
            # تفاعلات حديثة
            if user.events:
                print(f"\nاخر التفاعلات:")
                for event in user.events[-3:]:  # آخر 3 تفاعلات
                    action_arabic = {"view": "مشاهدة", "like": "اعجاب", "share": "مشاركة", "watch": "مشاهدة"}
                    action_text = action_arabic.get(event['action'], event['action'])
                    print(f"   • {event['item']} ({action_text})")
        else:
            print("❌ لا توجد بيانات تفاعل للمستخدم")
    
    def update_profile(self):
        """تحديث الملف الشخصي"""
        if not self.auth.current_user:
            print("❌ يجب تسجيل الدخول أولاً")
            return
        
        username = self.auth.current_user["username"]
        
        print(f"\nتحديث الملف الشخصي لـ {username}")
        print("-"*40)
        
        print("ما الذي تريد تحديثه؟")
        print("1. الاسم الكامل")
        print("2. العمر")
        print("3. البلد")
        print("4. الاهتمامات")
        print("5. كل شيء")
        print("6. رجوع")
        
        try:
            choice = int(input("\nاختر: "))
            
            if choice == 1:
                full_name = input("الاسم الكامل الجديد: ").strip()
                self.auth.update_profile(username, full_name=full_name)
                print("✅ تم تحديث الاسم")
            
            elif choice == 2:
                age = input("العمر الجديد: ").strip()
                self.auth.update_profile(username, age=age if age else None)
                print("✅ تم تحديث العمر")
            
            elif choice == 3:
                country = input("البلد الجديد: ").strip()
                self.auth.update_profile(username, country=country)
                print("✅ تم تحديث البلد")
            
            elif choice == 4:
                print("\nاختر اهتماماتك الجديدة:")
                categories = self.recommender.database.get_categories()
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                
                interests_input = input("\nادخل أرقام الاهتمامات (مفصولة بفاصلة): ").strip()
                
                if interests_input:
                    try:
                        indices = [int(x.strip()) - 1 for x in interests_input.split(',')]
                        selected_interests = [categories[i] for i in indices if 0 <= i < len(categories)]
                        self.auth.update_profile(username, interests=selected_interests)
                        print("✅ تم تحديث الاهتمامات")
                    except:
                        print("❌ صيغة غير صحيحة")
            
            elif choice == 5:
                self.collect_profile_info(username)
            
            elif choice == 6:
                return
            
            else:
                print("❌ اختيار غير صحيح")
        
        except ValueError:
            print("❌ الرجاء إدخال رقم")
    
    def browse_as_guest(self):
        """التصفح كمستخدم زائر"""
        print("\nأنت تتصفح كمزور")
        print("-"*30)
        
        # إنشاء مستخدم مؤقت للزائر
        temp_id = "guest_" + str(random.randint(1000, 9999))
        temp_name = "زائر"
        
        if temp_id not in self.recommender.users:
            self.recommender.add_user(temp_id, temp_name)
        
        # عرض بعض المحتوى
        categories = self.recommender.database.get_categories()
        print("\nالتصنيفات المتاحة:")
        for i, cat in enumerate(categories[:5], 1):  # أول 5 تصنيفات فقط
            items_count = len(self.recommender.database.get_items_by_category(cat))
            print(f"{i}. {cat} ({items_count} عنصر)")
        
        # عرض بعض العناصر الشائعة
        if hasattr(self.recommender.database, 'get_popular_items'):
            popular_items = self.recommender.database.get_popular_items(3)
            if popular_items:
                print("\nالعناصر الشائعة:")
                for i, item in enumerate(popular_items, 1):
                    print(f"{i}. {item}")
        
        print("\nسجل دخول للحصول على توصيات شخصية!")
    
    def run(self):
        """تشغيل التطبيق"""
        print("بدء نظام التوصية الذكي التفاعلي")
        
        while True:
            self.display_menu()
            
            try:
                if self.auth.current_user:
                    choice = input("\nاختر من 1-7: ").strip()
                    
                    if choice == "1":
                        self.show_recommendations()
                    elif choice == "2":
                        self.browse_content()
                    elif choice == "3":
                        # التفاعل مع محتوى عشوائي
                        if self.auth.current_user:
                            user_id = self.auth.current_user["user_id"]
                            items = list(self.recommender.database.items.keys())
                            if items:
                                item = random.choice(items)
                                action = random.choice(["view", "like", "watch"])
                                duration = None
                                
                                if action == "watch":
                                    item_info = self.recommender.database.items.get(item, {})
                                    if "duration_min" in item_info:
                                        duration = item_info["duration_min"] * 60
                                    else:
                                        duration = random.randint(30, 180)
                                
                                self.recommender.record_interaction(user_id, item, action, duration)
                                
                                # تحديث الشعبية
                                if hasattr(self.recommender.database, 'update_popularity'):
                                    self.recommender.database.update_popularity(item, action)
                                
                                print(f"✅ تفاعلت مع: {item} ({action})")
                    elif choice == "4":
                        self.show_user_stats()
                    elif choice == "5":
                        self.update_profile()
                    elif choice == "6":
                        success, message = self.auth.logout()
                        print(message)
                    elif choice == "7":
                        print("\nشكراً لاستخدامك النظام. إلى اللقاء!")
                        break
                    else:
                        print("❌ اختيار غير صحيح")
                
                else:  # لم يسجل دخول
                    choice = input("\nاختر من 1-4: ").strip()
                    
                    if choice == "1":
                        self.register_user()
                    elif choice == "2":
                        if self.login_user():
                            # بعد تسجيل الدخول الناجح
                            self.show_recommendations()
                    elif choice == "3":
                        self.browse_as_guest()
                    elif choice == "4":
                        print("\nشكراً لزيارتك. إلى اللقاء!")
                        break
                    else:
                        print("❌ اختيار غير صحيح")
            
            except KeyboardInterrupt:
                print("\nتم إيقاف البرنامج")
                break
            except Exception as e:
                print(f"\n❌ حدث خطأ: {e}")

if __name__ == "__main__":
    app = InteractiveRecommendationApp()
    app.run()