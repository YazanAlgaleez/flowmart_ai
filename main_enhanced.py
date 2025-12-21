import random
from datetime import datetime
from recommender import SmartRecommender
from content_database_enhanced import EnhancedContentDatabase
from analytics import AnalyticsDashboard
from recommender_ai import AdvancedRecommender

def simulate_user_activity(system, analytics, num_interactions=20):
    """محاكاة نشاط المستخدمين"""
    users = list(system.users.keys())
    items = list(system.database.items.keys())
    actions = ["view", "like", "watch", "share"]
    
    print("📊 محاكاة نشاط المستخدمين...")
    
    for _ in range(num_interactions):
        user_id = random.choice(users)
        item = random.choice(items)
        action = random.choice(actions)
        duration = random.randint(40, 300) if action == "watch" else None
        
        # تسجيل التفاعل
        system.record_interaction(user_id, item, action, duration)
        
        # تتبع التحليلات
        analytics.track_interaction(user_id, item, action)
        
        # إضافة تقييم عشوائي أحياناً
        if random.random() > 0.7:
            rating = random.randint(1, 5)
            category = system.database.items[item]["category"]
            system.users[user_id].add_event(item, category, f"rating_{rating}", rating=rating)

def display_recommendations(system, user_id):
    """عرض التوصيات للمستخدم"""
    user = system.users[user_id]
    
    print(f"\n👤 المستخدم: {user.username}")
    print("=" * 40)
    
    print("🎯 الاهتمامات المكتشفة:", ", ".join(user.interests) if user.interests else "لا توجد اهتمامات بعد")
    
    print("\n📝 سجل المشاهدة:")
    for item in user.watch_history[-5:]:  # آخر 5 عناصر
        print(f"  - {item}")
    
    print("\n💡 التوصيات المقترحة:")
    recommendations = system.recommend(user_id, num=7)
    for i, rec in enumerate(recommendations, 1):
        category = system.database.items[rec]["category"]
        print(f"  {i}. {rec} ({category})")
    
    return recommendations

def main():
    print("🚀 بدء تشغيل نظام التوصية الذكي")
    print("=" * 50)
    
    # إنشاء النظام الأساسي
    system = SmartRecommender()
    
    # استبدال قاعدة البيانات بالمحسنة
    system.database = EnhancedContentDatabase()
    
    # إضافة لوحة التحليلات
    analytics = AnalyticsDashboard(system)
    
    # إضافة نظام التوصية المتقدم
    ai_recommender = AdvancedRecommender()
    ai_recommender.build_item_features(system.database.items)
    
    # إضافة مستخدمين
    users = [
        ("u1", "أحمد"),
        ("u2", "سارة"),
        ("u3", "محمد"),
        ("u4", "فاطمة")
    ]
    
    for uid, name in users:
        system.add_user(uid, name)
        print(f"✅ تم إضافة المستخدم: {name} ({uid})")
    
    # محاكاة النشاط
    simulate_user_activity(system, analytics, num_interactions=30)
    
    # عرض التوصيات لكل مستخدم
    print("\n" + "=" * 50)
    print("📋 تقرير التوصيات")
    print("=" * 50)
    
    for uid, name in users:
        recs = display_recommendations(system, uid)
        
        # تحديث ملفات المستخدمين في النظام الذكي
        ai_recommender.update_user_profile(uid, system.users[uid].events)
    
    # عرض التحليلات
    print("\n" + "=" * 50)
    print("📈 لوحة التحليلات")
    print("=" * 50)
    
    # العناصر الشائعة
    popular = analytics.get_popular_items(days=1)
    print("\n🔥 العناصر الشائعة اليوم:")
    for item, count in popular[:5]:
        print(f"  - {item}: {count} تفاعل")
    
    # إحصاءات المستخدمين
    engagement_stats = analytics._get_engagement_stats()
    print(f"\n👥 إحصاءات تفاعل المستخدمين:")
    print(f"  - تفاعل عالي: {engagement_stats['high_engagement']} مستخدم")
    print(f"  - تفاعل متوسط: {engagement_stats['medium_engagement']} مستخدم")
    print(f"  - تفاعل منخفض: {engagement_stats['low_engagement']} مستخدم")
    
    # التوصيات المتقدمة
    print("\n" + "=" * 50)
    print("🤖 التوصيات الذكية المتقدمة")
    print("=" * 50)
    
    for uid, name in users[:2]:  # عرض لمستخدمين فقط كمثال
        content_recs = system.recommend(uid, num=5)
        hybrid_recs = ai_recommender.hybrid_recommendation(uid, content_recs)
        
        print(f"\n✨ توصيات هجينة لـ {name}:")
        for i, rec in enumerate(hybrid_recs, 1):
            print(f"  {i}. {rec}")
    
    # تصدير التقرير
    print("\n" + "=" * 50)
    report = analytics.export_analytics()
    print(f"✅ تم تصدير التقرير التحليلي ({report['generated_at']})")
    print(f"   - إجمالي المستخدمين: {report['total_users']}")
    print(f"   - إجمالي التفاعلات: {report['total_interactions']}")
    
    print("\n🎉 اكتمل تشغيل النظام!")

if __name__ == "__main__":
    main()  