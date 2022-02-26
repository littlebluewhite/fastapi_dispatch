import datetime
import random


def create_event_id(job):
    return job.replace(" ", "_") + "_" + str(datetime.datetime.now()).replace(" ", "_") \
                            + "_" + str(int(random.random() * 1000))
