import os
import requests
from datetime import timedelta, date

print(os.getcwd())

country = 'oman'
url = "https://covid-193.p.rapidapi.com/history"
headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "q13nuq8wLYmshCEEWAakAav4RoRZp1wnRw3jsnvampnyiBxcsG"
    }

if not os.path.exists(f'./history/{country}/'):
    os.makedirs(f'./history/{country}/')

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2020, 7, 1)
end_date = date(2020, 7, 26)
for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))
    querystring = {"day":single_date.strftime("%Y-%m-%d"),"country":country}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    with open(f'./history/{country}/{single_date.strftime("%Y-%m-%d")}.json', 'w') as f:
        f.write(response.text)  
