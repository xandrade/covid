import twitter
import maya
import datetime
import re
import csv
from pushbullet import Pushbullet
import sched, time
import sys

PUSHBULLET_KEY = 'o.TRIjBEQtbsnkYeKLkgFbtpFR2iQtKjyH'

def check_for_tweet():
    api = twitter.Api(consumer_key='VGMEA0wDjnPEavVVKXtKCqWEY',
                    consumer_secret='Vq5VSEv33tnd4voNn9gUjIGsXHwC7PeksUQVRW2bScC7AEIDXL',
                    access_token_key='28278105-kYcdSzL1EtwzYd9YdomYveHEz1ZbZ7naiUuj0W1P5',
                    access_token_secret='kO5C9UhKGeeSlCZxptXws5cGzmSTf2Y9TVv27QLX6smch')

    user = api.GetUser(screen_name='OmaniMOH')

    for tweet in api.GetUserTimeline(user_id=user.id, exclude_replies=True, count=200, include_rts=False):
        if '\u062a\u0639\u0644\u0646 #\u0648\u0632\u0627\u0631\u0629_\u0627\u0644\u0635\u062d\u0629 \u0639\u0646 \u062a\u0633\u062c\u064a\u0644' in tweet.text:
            # Automatically parse datetime strings and generate naive datetimes.
            scraped = tweet.created_at
            #print(maya.parse(scraped).datetime(naive=True) + datetime.timedelta(hours=4))
            #print(tweet.text)
            found = re.search('\([0-9]{1,}\)', tweet.text)
            #print(found.group(0).replace('(', '').replace(')', ''))
            
            in_file = False
            with open('./OmaniMOH.csv', newline='', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter='|')
                for row in spamreader:
                    #print(','.join(row))
                    if ','.join(row) ==  ','.join([str(maya.parse(scraped).datetime(naive=True) + datetime.timedelta(hours=4)),
                                                found.group(0).replace('(', '').replace(')', ''),tweet.text]):
                        in_file = True
            if not in_file:
                with open('./OmaniMOH.csv', 'a+', newline='', encoding='utf-8') as wcsvfile:
                    spamwriter = csv.writer(wcsvfile, delimiter='|')
                    spamwriter.writerow([str(maya.parse(scraped).datetime(naive=True) + datetime.timedelta(hours=4)),
                                            found.group(0).replace('(', '').replace(')', ''),tweet.text])
                print('new record found',  ','.join([str(maya.parse(scraped).datetime(naive=True) + datetime.timedelta(hours=4)),
                                                found.group(0).replace('(', '').replace(')', ''),tweet.text]))
                return str(maya.parse(scraped).datetime(naive=True) + datetime.timedelta(hours=4)), found.group(0).replace('(', '').replace(')', ''), tweet.text
    return None

def push_notification(title, body):
    # push the message
    pb = Pushbullet(PUSHBULLET_KEY)
    push = pb.push_note(title, body)

if __name__ == "__main__":

    s = sched.scheduler(time.time, time.sleep)

    def do_something(sc): 
        print("Running Task", datetime.datetime.now(), end='\r')
        
        tweet = check_for_tweet()
        if tweet is not None:
            created_at, number_infected, text = tweet
            push_notification(f"COVID-19: {number_infected}", created_at + '\n' + text)

        #sys.stdout.write("\033[K") # Clear to the end of line
        print("Last Run Time", datetime.datetime.now(), flush=True)

        s.enter(59, 1, do_something, (sc,))

    s.enter(0, 1, do_something, (s,))
    s.run()

