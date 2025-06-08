memory = []

def log_to_memory(record: dict):
    from datetime import datetime
    record["timestamp"] = str(datetime.utcnow())
    memory.append(record)
    print("[Memory Log]", record)


def get_memory():
    return memory
