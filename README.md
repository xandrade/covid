# twitter-covid
Twitter Notificator for COVID-19 Oman

This app get the latest tweets from @OmaniMOH, detect if a new case is posted and send a PushBullet notification of new case is detected. Each notification is saved in a csv file.

# Create conda enviroment
1. `conda update conda`
2. `conda create --name twitter-covid python=3.7`
3. `pip install pushbullet.py`
4. `conda install maya python-twitter`
5. `pip install GetOldTweets3`
