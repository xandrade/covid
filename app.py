import requests
import json
import os
import sys
import sched
import datetime
import time
from pushbullet import Pushbullet

CACHE = None
FIRST_NOTIFICATION = True

PUSHBULLET_KEY = os.environ.get('PUSHBULLET_KEY')
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

if None in (PUSHBULLET_KEY, RAPIDAPI_KEY):
    print('Error: Please set your KEYs under confg')
    sys.exit(0)


def call_api():

    global CACHE

    url = "https://covid-193.p.rapidapi.com/statistics"

    querystring = {"country":"oman"}

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:

            data = json.loads(response.text)

            rc = {
                'New Cases': data['response'][0]['cases']['new'],
                'Active Cases': data['response'][0]['cases']['active'],
                'Critical Cases': data['response'][0]['cases']['critical'],
                'Recovered Cases': data['response'][0]['cases']['recovered'],
                'Total Cases': data['response'][0]['cases']['total'],
                'New Deaths': data['response'][0]['deaths']['new'],
                'Total Deaths': data['response'][0]['deaths']['total'],
                'Total Tests': data['response'][0]['tests']['total'],
            }

            hashed = hash(frozenset(rc.items()))

            rc['Updated Time'] = data['response'][0]['time']
            rc['Date'] = data['response'][0]['day']

            if CACHE != hashed:
                CACHE = hashed
                print(data)
                return rc

        else:
            print('rapidapi responded code', response.status_code)

        return None
        
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print(f'Error: {e}')
        return None

    
def push_notification(title, body):
    # push the mes*sage
    print('Pushing message')
    pb = Pushbullet(PUSHBULLET_KEY)
    push = pb.push_note(title, body)


if __name__ == "__main__":

    s = sched.scheduler(time.time, time.sleep)

    def do_something(sc): 
        
        global FIRST_NOTIFICATION
        
        print("Running Task", datetime.datetime.now(), end='\r')

        data = call_api()
        if data is not None:
            value = ""
            for k, v in data.items():
                if k != 'Date':
                    value += f'{k}: {v}\n'
            else:
                if FIRST_NOTIFICATION:
                    push_notification(f"COVID-19: {data['Date']}", value)
                else:
                    FIRST_NOTIFICATION = True
                
                #message = f"[chatbot] #COVID-19 *{number_infected}* new cases recorded on {created_at} - {text}"
                #dist_list = ('Test', ) #'PDO LOWIS/ForeSite', 'RTO Story telling' 'Martes de CERVEZA online')
                #for to in dist_list:
                #    wa.send_wa_message(to, message)

        print("Last Run Time", datetime.datetime.now(), flush=True)

        s.enter(60*5, 1, do_something, (sc,))  # 60*2

    s.enter(0, 1, do_something, (s,))
    s.run()