from pytz import utc
import datetime
import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def get_now():
    return str(datetime.datetime.now())

def print_job():
    print get_now()+" test"

def get_id():
    return str(random.getrandbits(128))

def test_acheduler():
    scheduler = BackgroundScheduler(executors=executors,
                                    job_defaults=job_defaults,
                                    timezone=utc)
    scheduler.start()
    scheduler.add_job(print_job,
                      'interval',
                      id=get_id(),
                      seconds=1)

def main():
    print "main"
    print get_id()
    print datetime.datetime.now()
    test_acheduler()
    time.sleep(60)

if __name__ == "__main__":
    main()