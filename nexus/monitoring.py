import time
import psutil
from collections import defaultdict


class Monitor:
    def __init__(self):
        self._metrics = defaultdict(list)
        self._start_time = time.time()
    
    def record(self, metric: str, value: float):
        self._metrics[metric].append({
            "value": value,
            "timestamp": time.time()
        })
        
        if len(self._metrics[metric]) > 1000:
            self._metrics[metric] = self._metrics[metric][-1000:]
    
    def get_system_stats(self):
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "uptime": time.time() - self._start_time
        }
    
    def get_metrics(self, metric: str):
        return self._metrics.get(metric, [])


monitor = Monitor()
