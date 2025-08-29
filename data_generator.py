import json
import random
from datetime import datetime, timedelta

# Generate synthetic logs
num_users = 20
event_types = ["login", "logout", "purchase", "view", "click"]
logs = []

start_date = datetime.now() - timedelta(days=29)

for day in range(30):
    day_date = start_date + timedelta(days=day)
    for _ in range(random.randint(5, 15)):  # 5–15 events per day
        log = {
            "user_id": random.randint(1, num_users),
            "event_type": random.choice(event_types),
            "timestamp": (day_date + timedelta(seconds=random.randint(0, 86400))).isoformat()
        }
        logs.append(log)

# Save to file
with open("activity_logs.json", "w") as f:
    json.dump(logs, f, indent=2)

print("✅ Dataset saved as activity_logs.json")
