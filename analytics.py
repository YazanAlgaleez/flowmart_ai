import json
from datetime import datetime, timedelta

class AnalyticsDashboard:
    def __init__(self, recommender):
        self.recommender = recommender
        self.analytics_data = {
            "daily_interactions": {},
            "user_engagement": {},
            "popular_categories": {},
            "recommendation_performance": []
        }
    
    def track_interaction(self, user_id, item_name, action):
        """تتبع التفاعلات"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.analytics_data["daily_interactions"]:
            self.analytics_data["daily_interactions"][today] = {}
        
        if action not in self.analytics_data["daily_interactions"][today]:
            self.analytics_data["daily_interactions"][today][action] = 0
        
        self.analytics_data["daily_interactions"][today][action] += 1
        
        # تحديث تفاعل المستخدم
        if user_id not in self.analytics_data["user_engagement"]:
            self.analytics_data["user_engagement"][user_id] = {
                "total_interactions": 0,
                "last_active": datetime.now().isoformat()
            }
        
        self.analytics_data["user_engagement"][user_id]["total_interactions"] += 1
        self.analytics_data["user_engagement"][user_id]["last_active"] = datetime.now().isoformat()
    
    def get_popular_items(self, days=7):
        """الحصول على العناصر الشائعة خلال فترة محددة"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        item_counts = defaultdict(int)
        
        for uid, user in self.recommender.users.items():
            for event in user.events:
                event_date = datetime.now()  # في النسخة الحقيقية، يتم تخزين التاريخ
                if start_date <= event_date <= end_date:
                    item_counts[event["item"]] += 1
        
        return sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def export_analytics(self, filename="analytics_report.json"):
        """تصدير البيانات التحليلية"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_users": len(self.recommender.users),
            "total_interactions": sum(len(user.events) for user in self.recommender.users.values()),
            "popular_categories": self._get_category_stats(),
            "user_engagement_stats": self._get_engagement_stats()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def _get_category_stats(self):
        """إحصاءات التصنيفات"""
        category_counts = defaultdict(int)
        
        for user in self.recommender.users.values():
            for event in user.events:
                category_counts[event["category"]] += 1
        
        return dict(category_counts)
    
    def _get_engagement_stats(self):
        """إحصاءات تفاعل المستخدمين"""
        stats = {
            "high_engagement": 0,
            "medium_engagement": 0,
            "low_engagement": 0
        }
        
        for user_id, data in self.analytics_data["user_engagement"].items():
            interactions = data["total_interactions"]
            
            if interactions > 20:
                stats["high_engagement"] += 1
            elif interactions > 5:
                stats["medium_engagement"] += 1
            else:
                stats["low_engagement"] += 1
        
        return stats