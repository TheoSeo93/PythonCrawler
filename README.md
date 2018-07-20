# PythonCrawler
Python Crawler for "SBU Foodies" on Google Playstore 

Initially, I tried to make a web crawler & scraper that uploads the data to the Google Drive, but because of the fact that the data should be accessed without any authentication process from the users, I changed the crawler to upload the file into Firebase storage.

Then, I became lazy to update the menu by running the python script on my laptop.

So I deployed the python script to Heroku, ran by python apscheduler. I manipulated the web driver options to look this headless browser like a human browsing website. This file name is automated.py
