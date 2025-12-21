import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AdvancedRecommender:
    def __init__(self):
        self.user_profiles = {}
        self.item_features = {}
        self.user_item_matrix = {}
        self.tfidf_vectorizer = TfidfVectorizer()
        
    def build_item_features(self, items_data):
        """بناء خصائص العناصر باستخدام TF-IDF"""
        item_descriptions = {}
        for item_name, info in items_data.items():
            # دمج التصنيف والوسوم في نص واحد
            text = f"{info['category']} {' '.join(info['tags'])}"
            item_descriptions[item_name] = text
        
        # تحويل النصوص إلى متجهات
        if item_descriptions:
            texts = list(item_descriptions.values())
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            
            for idx, item_name in enumerate(item_descriptions.keys()):
                self.item_features[item_name] = tfidf_matrix[idx]
    
    def update_user_profile(self, user_id, interactions):
        """تحديث ملف المستخدم باستخدام التعلم الآلي"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = defaultdict(float)
        
        for interaction in interactions:
            item = interaction["item"]
            action = interaction["action"]
            weight = self._get_action_weight(action)
            
            if item in self.item_features:
                # ترجيح اهتمامات المستخدم بناء على التفاعل
                self.user_profiles[user_id][item] += weight
    
    def _get_action_weight(self, action):
        """تعيين أوزان مختلفة للإجراءات"""
        weights = {
            "view": 1.0,
            "like": 3.0,
            "share": 5.0,
            "watch": 4.0,
            "rating_high": 5.0,
            "rating_low": 0.5
        }
        return weights.get(action, 1.0)
    
    def collaborative_filtering(self, user_id, k=3):
        """تصفية تعاونية مبسطة"""
        recommendations = []
        similar_users = self._find_similar_users(user_id)
        
        for similar_user in similar_users[:k]:
            # الحصول على عناصر أعجب بها المستخدم المشابه
            user_items = self.user_profiles.get(similar_user, {})
            top_items = sorted(user_items.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for item, score in top_items:
                if item not in recommendations:
                    recommendations.append(item)
        
        return recommendations
    
    def _find_similar_users(self, user_id):
        """إيجاد مستخدمين مشابهين"""
        # في النسخة الحقيقية، يتم حساب التشابه باستخدام cosine similarity
        # هنا نستخدم نسخة مبسطة
        all_users = list(self.user_profiles.keys())
        all_users.remove(user_id)  # إزالة المستخدم الحالي
        return all_users[:5]  # إرجاع أول 5 مستخدمين
    
    def hybrid_recommendation(self, user_id, content_based_recs, num=10):
        """توصية هجينة تجمع بين عدة طرق"""
        collaborative_recs = self.collaborative_filtering(user_id)
        
        # دمج التوصيات مع إعطاء أولوية للتوصيات القائمة على المحتوى
        hybrid = []
        
        # إضافة توصيات المحتوى أولاً
        for rec in content_based_recs:
            if rec not in hybrid:
                hybrid.append(rec)
        
        # إضافة التوصيات التعاونية
        for rec in collaborative_recs:
            if rec not in hybrid and len(hybrid) < num:
                hybrid.append(rec)
        
        return hybrid[:num]