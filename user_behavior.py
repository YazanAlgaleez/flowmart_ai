class UserBehavior:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.events = []
        self.interests = set()
        self.watch_history = []
    
    def add_event(self, item_name, category, action, duration=None, rating=None):
        event = {
            "item": item_name,
            "category": category,
            "action": action,
            "duration": duration,
            "rating": rating
        }
        self.events.append(event)
        
        if action in ["like", "watch", "share"] and duration and duration > 30:
            self.interests.add(category)
        
        if action == "watch":
            self.watch_history.append(item_name)
    
    def get_interaction_score(self, category):
        score = 0
        for event in self.events:
            if event["category"] == category:
                if event["action"] == "view":
                    score += 1
                elif event["action"] == "like":
                    score += 2
                elif event["action"] == "share":
                    score += 3
                elif event["action"] == "watch":
                    score += (event.get("duration", 0) / 60)
        return score