"""
مكتشف المزاج البسيط
"""

class MoodDetector:
    def detect(self, text):
        """تحليل بسيط لمزاج المستخدم"""
        text = str(text).lower()  # تحويل للنص الصغير
        
        # تحقق من الكلمات العربية
        if any(word in text for word in ["مبسوط", "سعيد", "فرح", "مسرور"]):
            return "سعيد"
        elif any(word in text for word in ["زعلان", "حزين", "تعيس", "محبط"]):
            return "حزين"
        elif any(word in text for word in ["تعبان", "مرهق", "متعب", "إرهاق"]):
            return "مرهق"
        elif any(word in text for word in ["غاضب", "عصبي", "منزعج"]):
            return "غاضب"
        else:
            return "محايد"
    
    def get_mood_based_recommendations(self, mood):
        """توصيات بناءً على المزاج"""
        mood_recommendations = {
            "سعيد": ["موسيقى حماسية", "فيديوهات كوميدية", "ألعاب ممتعة"],
            "حزين": ["موسيقى هادئة", "فيديوهات ملهمة", "نصائح للراحة النفسية"],
            "مرهق": ["موسيقى استرخاء", "تمارين تنفس", "نصائح للنوم"],
            "غاضب": ["موسيقى مهدئة", "تمارين رياضية", "نصائح للهدوء"],
            "محايد": ["فيديوهات تعليمية", "مقالات متنوعة", "محتويات جديدة"]
        }
        return mood_recommendations.get(mood, ["محتويات متنوعة"])