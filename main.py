'''to do today
2. call each of these with a separate instance of praw
2. parameter tuning to track a post, it's score, and it's comments for 24 hours
3. incorporate airflow
4. incorporate twilio
5. dockerize
6. add to aws
7. execute
'''

from pipeline import runUpdate
import threading
import time
import logging
from database import getSession

def threadedRunUpdate(subredditName, session):
    logging.info(f"Now updating {subredditName}: starting")
    runUpdate(subredditName, session)
    logging.info(f"Now updating {subredditName}: finishing")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    threads = list()
    subreddits = ['ProgrammerHumor', 'OMSCS']
    for sr in subreddits:
        logging.info("Main    : before run thread")
        session = getSession()
        x = threading.Thread(target=threadedRunUpdate, args=(sr, session,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)







# runUpdate("ProgrammerHumor")