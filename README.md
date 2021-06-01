# PybottCryptoSignalBinance
PybottCryptoSignalBinance

## DEVELOPEMENT PURPOSE
- python -m venv venv
- venv\Scripts\activate (To activate virtual environment)
- pip install -r requirements.txt
- python app.py

## PRODUCTION PURPOSE
- git init
- git add .
- git commit -m "add first issue"
- heroku login
- heroku create
- git push heroku master

## ADD BUILDPACK TO HEROKU & ENV VARIABLE 
- heroku buildpacks:add --index 1 heroku/python
- heroku buildpacks:add --index 2 https://github.com/numrut/heroku-buildpack-python-talib

## PRODUCTION LOG
- heroku logs --tail
