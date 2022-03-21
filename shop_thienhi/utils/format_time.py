from datetime import datetime

def format_time_filter():
    start_time = datetime.now().utcnow().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    end_time = datetime.utcnow().replace(second=0, microsecond=0).timestamp()
    data = {
        "start_time": start_time,
        "end_time": end_time
    }
    return data
