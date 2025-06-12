import os

def load_triggers():
    triggers = {}
    for key, value in os.environ.items():
        if key.startswith("TRIGGER_"):
            trigger = key.replace("TRIGGER_", "").replace("_", " ").lower()
            triggers[trigger] = value
    return triggers
