# covid
Push notificator for COVID-19 statistics in Oman

This app query the rapidapi.com API and push a notifcation if change is detected.


# Linux (Ubuntu-20.04) through WSL 2

1. Go to the project folder, for example: `andrade@dell:/mnt/c/Users/andra$` `cd "/mnt/d/Dropbox/Python Projects/covid"`
2. Create virtual enviroment: `andrade@dell:/mnt/d/Dropbox/Python Projects/covid$` `python3 -m venv .venv`
3. Activte enviroment: `andrade@dell:/mnt/d/Dropbox/Python Projects/covid$` `source .venv/bin/activate`
4. After the virtual environment is active, we are going to want to ensure that a couple of essential Python packages within the virtual environment are up to date: `(.venv) andrade@dell:/mnt/d/Dropbox/Python Projects/covid$` `pip install -U setuptools pip`
5. Install the requirements: `(.venv) andrade@dell:/mnt/d/Dropbox/Python Projects/covid$` `pip install requests pushbullet.py`
6. Open VSCode `(.venv) andrade@dell:/mnt/d/Dropbox/Python Projects/covid$` `code .`


# Git

1. `git config --global user.email "a@gmail.com"`
2. `git config --global user.name "xandrade"`
3. `rm -f ./.git/index.lock`

# Docker container

info for buiding the container and running is available at https://github.com/xandrade/covid/blob/master/Dockerfile