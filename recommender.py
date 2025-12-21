from collections import defaultdict
from user_behavior import UserBehavior
from content_database import ContentDatabase

class SmartRecommender:
    def __init__(self):
        self.users = {}
        self.database = ContentDatabase()
        self.trending_items = []
        self.interaction_history = defaultdict(list)
    
    def add_user(self, user_id, username):
        self.users[user_id] = UserBehavior(user_id, username)
    
    def record_interaction(self, user_id, item_name, action, duration=None):
        if user_id in self.users and item_name in self.database.items:
            category = self.database.items[item_name]["category"]
            self.users[user_id].add_event(item_name, category, action, duration)
            self.interaction_history[item_name].append(action)
            self.update_trending()
    
    def update_trending(self):
        scores = defaultdict(int)
        for item, actions in self.interaction_history.items():
            for action in actions:
                if action == "view":
                    scores[item] += 1
                elif action == "like":
                    scores[item] += 3
                elif action == "share":
                    scores[item] += 5
                elif action == "watch":
                    scores[item] += 2
        
        self.trending_items = sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )
    
    def recommend(self, user_id, num=5):
        if user_id not in self.users:
            return []
        
        user = self.users[user_id]
        recommendations = []
        
        for interest in user.interests:
            items = self.database.get_items_by_category(interest)
            for item in items:
                recommendations.append(item)
        
        for item, _ in self.trending_items:
            if item not in recommendations:
                recommendations.append(item)
        
        return recommendations[:num]