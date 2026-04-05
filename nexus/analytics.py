import time
from collections import defaultdict, Counter


class Analytics:
    def __init__(self, db):
        self._db = db
        self._session_stats = defaultdict(int)
        self._command_usage = Counter()
    
    def track_command(self, command: str, user_id: int):
        self._command_usage[command] += 1
        
        stats = self._db.get("Analytics", "command_stats", {})
        if command not in stats:
            stats[command] = {"count": 0, "users": set()}
        
        stats[command]["count"] += 1
        stats[command]["users"].add(user_id)
        
        self._db.set("Analytics", "command_stats", stats)
    
    def get_popular_commands(self, limit=10):
        return self._command_usage.most_common(limit)
    
    def get_stats(self):
        return {
            "total_commands": sum(self._command_usage.values()),
            "unique_commands": len(self._command_usage),
            "popular": self.get_popular_commands(5)
        }
