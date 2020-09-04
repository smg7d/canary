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
from database import getSession
import time

if __name__ == "__main__":
    session = getSession()
    while True:
        runUpdate("ProgrammerHumor", session)
        runUpdate("AskReddit", session)
        runUpdate("csCareerQuestions", session)
        time.sleep(60*5)








# runUpdate("ProgrammerHumor")