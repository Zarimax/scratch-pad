# Attempt to start scheduler
# if failed, wait and retry

from scheduler import Scheduler
from log import Log

config = {
    "wake_time": "0500",
    "sleep_time": "2200",
    "logger": Log(),
    "working_dir": r"C:\Users\Black Beast\Desktop\bus-tracker",
    "begin_stop_name": "Haarlem, Emmaplein",
    "end_stop_name": "Haarlem, Centrum/Houtplein",
}

s = Scheduler(config)

while(True):
    s.state()