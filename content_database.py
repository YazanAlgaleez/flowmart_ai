
class ContentDatabase:
    def __init__(self):
        self.items = {
            "Python Tutorial": {
                "category": "Programming",
                "tags": ["python", "programming", "coding", "tutorial", "beginner"],
                "difficulty": "beginner",
                "duration_min": 45
            },
            "Machine Learning Crash Course": {
                "category": "AI & ML",
                "tags": ["machine learning", "ai", "data science", "algorithms"],
                "difficulty": "intermediate",
                "duration_min": 120
            },
            "Web Development Full Course": {
                "category": "Web Development",
                "tags": ["html", "css", "javascript", "web", "frontend"],
                "difficulty": "beginner",
                "duration_min": 180
            },
            "React Native Mobile Apps": {
                "category": "Mobile Development",
                "tags": ["react", "mobile", "apps", "javascript"],
                "difficulty": "intermediate",
                "duration_min": 95
            },
            
            # 🎮 الألعاب والتسلية
            "Gaming Laptop Review 2024": {
                "category": "Gaming",
                "tags": ["gaming", "laptop", "review", "tech", "hardware"],
                "difficulty": "beginner",
                "duration_min": 25
            },
            "Valorant Gameplay Tips": {
                "category": "Gaming",
                "tags": ["valorant", "fps", "gaming", "esports", "tips"],
                "difficulty": "intermediate",
                "duration_min": 18
            },
            "Best RPG Games 2024": {
                "category": "Gaming",
                "tags": ["rpg", "games", "review", "entertainment"],
                "difficulty": "beginner",
                "duration_min": 32
            },
            
            # 🎵 الموسيقى
            "Pop Music Mix 2024": {
                "category": "Music",
                "tags": ["pop", "music", "mix", "entertainment", "charts"],
                "difficulty": "beginner",
                "duration_min": 60
            },
            "Arabic Music Classics": {
                "category": "Music",
                "tags": ["arabic", "music", "classic", "nostalgia"],
                "difficulty": "beginner",
                "duration_min": 45
            },
            "Jazz Relaxation Playlist": {
                "category": "Music",
                "tags": ["jazz", "relax", "music", "study"],
                "difficulty": "beginner",
                "duration_min": 90
            },
            
            # 🏋️ الرياضة واللياقة
            "Full Body Workout": {
                "category": "Fitness",
                "tags": ["workout", "fitness", "exercise", "health"],
                "difficulty": "intermediate",
                "duration_min": 40
            },
            "Yoga for Beginners": {
                "category": "Fitness",
                "tags": ["yoga", "meditation", "health", "wellness"],
                "difficulty": "beginner",
                "duration_min": 30
            },
            "Nutrition Guide": {
                "category": "Fitness",
                "tags": ["nutrition", "diet", "health", "food"],
                "difficulty": "beginner",
                "duration_min": 35
            },
            
            # 📱 الجوالات
            "iPhone 15 Review": {
                "category": "Mobile",
                "tags": ["iphone", "apple", "review", "mobile", "tech"],
                "difficulty": "beginner",
                "duration_min": 22
            },
            "Android vs iOS Comparison": {
                "category": "Mobile",
                "tags": ["android", "ios", "comparison", "mobile"],
                "difficulty": "beginner",
                "duration_min": 28
            },
            "Smartphone Camera Tips": {
                "category": "Mobile",
                "tags": ["camera", "photography", "mobile", "tips"],
                "difficulty": "intermediate",
                "duration_min": 19
            },
            
            # 🎬 الأفلام والمسلسلات
            "Netflix Top 10 Series": {
                "category": "Entertainment",
                "tags": ["netflix", "series", "entertainment", "movies"],
                "difficulty": "beginner",
                "duration_min": 15
            },
            "Marvel Movies Timeline": {
                "category": "Entertainment",
                "tags": ["marvel", "movies", "superhero", "comics"],
                "difficulty": "beginner",
                "duration_min": 38
            },
            "Arabic Drama Review": {
                "category": "Entertainment",
                "tags": ["arabic", "drama", "series", "ramadan"],
                "difficulty": "beginner",
                "duration_min": 20
            },
            
            # 💰 المال والأعمال
            "Stock Market Basics": {
                "category": "Finance",
                "tags": ["stocks", "investment", "finance", "money"],
                "difficulty": "beginner",
                "duration_min": 50
            },
            "Freelancing Guide 2024": {
                "category": "Business",
                "tags": ["freelancing", "work", "online", "business"],
                "difficulty": "intermediate",
                "duration_min": 55
            },
            "E-commerce Tutorial": {
                "category": "Business",
                "tags": ["ecommerce", "business", "online", "shop"],
                "difficulty": "intermediate",
                "duration_min": 70
            },
            
            # 🍳 الطبخ
            "Arabic Food Recipes": {
                "category": "Cooking",
                "tags": ["cooking", "food", "recipes", "arabic"],
                "difficulty": "intermediate",
                "duration_min": 40
            },
            "Healthy Breakfast Ideas": {
                "category": "Cooking",
                "tags": ["healthy", "food", "breakfast", "nutrition"],
                "difficulty": "beginner",
                "duration_min": 25
            },
            "Dessert Recipes": {
                "category": "Cooking",
                "tags": ["dessert", "sweet", "recipes", "baking"],
                "difficulty": "intermediate",
                "duration_min": 35
            }
        }
        
        # إحصائيات لكل عنصر
        for item in self.items:
            self.items[item]["views"] = 0
            self.items[item]["likes"] = 0
            self.items[item]["popularity"] = 0.5  # درجة شعبية ابتدائية

    def get_items_by_category(self, category):
        """الحصول على عناصر حسب التصنيف"""
        return [
            item for item, info in self.items.items()
            if info["category"] == category
        ]
    
    def get_items_by_tag(self, tag):
        """الحصول على عناصر حسب الوسم"""
        return [
            item for item, info in self.items.items()
            if tag in info["tags"]
        ]
    
    def get_popular_items(self, limit=10):
        """الحصول على العناصر الأكثر شعبية"""
        sorted_items = sorted(
            self.items.items(),
            key=lambda x: x[1]["popularity"],
            reverse=True
        )
        return [item for item, _ in sorted_items[:limit]]
    
    def search_items(self, query):
        """بحث في العناصر"""
        query = query.lower()
        results = []
        
        for item, info in self.items.items():
            score = 0
            
            # البحث في العنوان
            if query in item.lower():
                score += 3
            
            # البحث في التصنيف
            if query in info["category"].lower():
                score += 2
            
            # البحث في الوسوم
            for tag in info["tags"]:
                if query in tag.lower():
                    score += 1
            
            if score > 0:
                results.append((item, score, info))
        
        # ترتيب النتائج حسب النقاط
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def update_popularity(self, item_name, action):
        """تحديث درجة الشعبية"""
        if item_name in self.items:
            if action == "view":
                self.items[item_name]["views"] += 1
                self.items[item_name]["popularity"] += 0.01
            elif action == "like":
                self.items[item_name]["likes"] += 1
                self.items[item_name]["popularity"] += 0.05
            elif action == "share":
                self.items[item_name]["popularity"] += 0.1
            
            # تقييد درجة الشعبية بين 0 و 1
            self.items[item_name]["popularity"] = max(0, min(1, self.items[item_name]["popularity"]))
    
    def get_recommendations_by_item(self, item_name, num=5):
        """الحصول على توصيات بناء على عنصر معين"""
        if item_name not in self.items:
            return []
        
        target_item = self.items[item_name]
        similarities = []
        
        for other_item, other_info in self.items.items():
            if other_item == item_name:
                continue
            
            similarity = 0
            
            # تشابه التصنيف
            if target_item["category"] == other_info["category"]:
                similarity += 2
            
            # تشابه الوسوم
            common_tags = set(target_item["tags"]) & set(other_info["tags"])
            similarity += len(common_tags) * 0.5
            
            # إضافة درجة الشعبية
            similarity += other_info["popularity"] * 0.3
            
            similarities.append((other_item, similarity))
        
        # ترتيب حسب التشابه
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [item for item, _ in similarities[:num]]
    
    def get_categories(self):
        """الحصول على جميع التصنيفات"""
        categories = set()
        for info in self.items.values():
            categories.add(info["category"])
        return list(categories)
    
    def get_stats(self):
        """إحصائيات قاعدة البيانات"""
        total_items = len(self.items)
        total_views = sum(item["views"] for item in self.items.values())
        total_likes = sum(item["likes"] for item in self.items.values())
        
        return {
            "total_items": total_items,
            "total_views": total_views,
            "total_likes": total_likes,
            "categories_count": len(self.get_categories()),
            "avg_popularity": sum(item["popularity"] for item in self.items.values()) / total_items
        }