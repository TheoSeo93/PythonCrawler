# PythonCrawler, Heroku X Pyrebase X Apscheduler
Python Crawler for "SBU Foodies" on Google Playstore 

Initially, I tried to make a web crawler & scraper that uploads the data to the Google Drive and Firebase.

Then, I became lazy to update the menu by running the python script on my laptop.

So I deployed the python script to Heroku, run by python apscheduler. I manipulated the web driver options to make this headless browser look like a human browsing website. This file name is automated.py



This was the steps for crawling data from a website.
Stony Brook Campus website was directing this address to show what the daily menu of dining halls were.
https://cafes.compass-usa.com/StonyBrook/SitePages/Menu.aspx?lid=a1

However, it was not possible because the actual menu data was hidden from iframe html element.
So I had to find the real address from which the website was getting data.
As you can see from this image, the iframe was directing the real web address.
![alt text](https://github.com/TheoSeo93/PythonCrawler/blob/master/crawl_2.png)
      
