from datetime import datetime
import time


def get_now():
    now = datetime.now()
    return (now.month, now.year)


print("\nStarting up!!!\n")
