import requests

url = "https://covid-193.p.rapidapi.com/statistics"

querystring = {"country":"oman"}

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "q13nuq8wLYmshCEEWAakAav4RoRZp1wnRw3jsnvampnyiBxcsG"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
