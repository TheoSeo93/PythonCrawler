# PythonCrawler, Heroku X Pyrebase X Apscheduler
## Python Crawler for "SBU Foodies" on Google Playstore 
Initially, I tried to make a web crawler & scraper that uploads the data to the Google Drive and Firebase.

Then, I became lazy to update the menu by running the python script on my laptop.

So I deployed the python script to Heroku, run by python apscheduler. 

I manipulated the web driver options to make this headless browser that looks like a human browsing website. This file name is automated.py



## Step 1
Stony Brook Campus website was directing this address to show what the daily menu of dining halls were.
https://cafes.compass-usa.com/StonyBrook/SitePages/Menu.aspx?lid=a1

However, the address was fake!
It was impossible to crawl the data because the actual menu data was hidden from iframe html element.
So I had to find the real address from which the website was getting data.
As you can see from this image, the iframe was directing the real web address.

![alt txt](https://github.com/TheoSeo93/PythonCrawler/blob/master/crawl_2.PNG)


## Step 2
After finding out the "real" address to crawl, I began to write a python script that crawls all the data looping through to select each date, places, and time slots during the day.

![alt txt](https://github.com/TheoSeo93/PythonCrawler/blob/master/crawl_1.png)


## Step 3
So this is it!
![alt txt](https://github.com/TheoSeo93/PythonCrawler/blob/master/giphy.gif)

      
