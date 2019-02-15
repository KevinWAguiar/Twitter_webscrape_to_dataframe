import pandas as pd
import time
import re
import requests
import plotly
import html

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime

hash_or_handle = input("Would you like to scrape a hashtag twitter webpage, \n or a handle's twitter webpage?\n Please respond 'hashtag' or 'handle':\n")
browser_var = input("What browser would you like selenium to work with?\n The options are:\n 1. Chrome \n 2. Firefox \n 3. Safari:\n")

if browser_var == 'Chrome':
    browser = webdriver.Chrome()
elif browser_var == 'Firefox':
    browser = webdriver.Firefox()
else:
    browser = webdriver.Safari()


if hash_or_handle == 'hashtag':

    hashtag = input("What hashtag's twitter webpage would you like to scrape?\n Please do not include the '#' in your response.\n")

    browser.get("https://twitter.com/hashtag/" + hashtag + "?lang=en")

    # Selenium script to scroll to the bottom of webpage,
    # wait 1 second for the next batch of data to load,
    # then continue scrolling.  It will continue to do this until the page stops loading new data.
    page_len = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
    end_page=False
    while(end_page==False):
            last_count = page_len
            time.sleep(1)
            page_len = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
            if last_count==page_len:
                end_page=True

    # The page has been fully scrolled.
    # Now it is ready to actually scrape and store the data.
    data = browser.page_source

    # Use BeautifulSoup to Parse code.
    data = bs(data, 'lxml')

    num_tweets = len(list(data.find_all('p', {'class': 'TweetTextSize js-tweet-text tweet-text'})))

    # Print number of tweets scraped for reference:
    print("{} tweets have been scraped.".format(num_tweets))

    master_list = []

    #--------------------------------------------------------------------------------------------------#
    # Transform scraped data into a list of dictionaries:

    # For loop through each tweet scraped above:
    #for i in range(num_tweets):
    for i in range(41):

        # Use BeautifulSoup to sort through raw tweets (not cleaned, still containing HTML, etc.):
        tweets = data.find_all('p', {'class': 'TweetTextSize js-tweet-text tweet-text'})

        # Create empty, temporary dictionary where each tweet's info will be stored:
        temp_dict = {}

        # Extract the handle of the tweet:
        temp_dict['handle']     = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('href="/')[1].split('/status')[0]

        # Clean up/extract the cleaned tweet; if IndexError, just return an empty string (discard later on):
        try:
            temp_dict['tweet']      = str(tweets[i].get_text()).replace("\n", " ")
        except IndexError:
            temp_dict['tweet']      = ""

        # Organize the dictionary to include when (date and time) the tweet was sent out:
        temp_dict['day']        = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[0]
        temp_dict['month']      = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[1]
        temp_dict['year']       = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[2]
        temp_dict['time']       = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split(' - ')[0]

        # Create a datetime object to be added to the dictionary:
        datetime_object = datetime.strptime(temp_dict['month'] + ' ' + temp_dict['day'] + ' ' + temp_dict['year'] + ' ' + temp_dict['time'].replace(" ", ""), '%b %d %Y %I:%M%p')

        # Add the tweet's datetime of when it was sent out:
        temp_dict['datetime']   = datetime_object

        # Append the temporary dictionary containing the tweet's information to the master_list:
        master_list.append(temp_dict)

        # Print i at every 5th tweet to show the status of the code:
        if i % 5 == 0:
            print(i)
        else:
            continue


    # Turn the 'master_list' into a Pandas DataFrame, and assign to variable 'df':

    df = pd.DataFrame(master_list)

    # Rearrange columns in a more logical order:

    df = df[['handle', 'tweet', 'datetime', 'day', 'month', 'year', 'time']]

    # Save the Pandas DataFrame to a .csv file:

    df.to_csv('twitter_scraped_' + hashtag + '_df.csv', index=False, sep=",")


elif hash_or_handle == 'handle':

    handle = input("Which handle's twitter webpage would you like to scrape?\n Please do not include the '@' in your response.\n")

    browser.get("https://twitter.com/" + handle)

    # Selenium script to scroll to the bottom of webpage,
    # wait 1 second for the next batch of data to load,
    # then continue scrolling.  It will continue to do this until the page stops loading new data.
    page_len = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
    end_page=False
    while(end_page==False):
            last_count = page_len
            time.sleep(1)
            page_len = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var page_len=document.body.scrollHeight;return page_len;")
            if last_count==page_len:
                end_page=True

    # The page has been fully scrolled.
    # Now it is ready to actually scrape and store the data.
    data = browser.page_source

    # Use BeautifulSoup to Parse code.
    data = bs(data, 'lxml')

    num_tweets = len(list(data.find_all('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})))

    # Print number of tweets scraped for reference:
    print("{} tweets have been scraped.".format(num_tweets))

    master_list = []

    #--------------------------------------------------------------------------------------------------#
    # Transform scraped data into a list of dictionaries:

    # For loop through each tweet scraped above:
    #for i in range(num_tweets):
    for i in range(51):

        # Use BeautifulSoup to sort through raw tweets (not cleaned, still containing HTML, etc.):
        tweets = data.find_all('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})

        # Create empty, temporary dictionary where each tweet's info will be stored:
        temp_dict = {}

        # Extract the handle of the tweet:
        #temp_dict['handle']     = str(handle)
        temp_dict['handle']     = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('href="/')[1].split('/status')[0]


        # Clean up/extract the cleaned tweet; if IndexError, just return an empty string (discard later on):
        try:
            temp_dict['tweet']      = str(tweets[i].get_text()).replace("\n", " ")
        except IndexError:
            temp_dict['tweet']      = ""

        # Organize the dictionary to include when (date and time) the tweet was sent out:
        temp_dict['day']        = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[0]
        temp_dict['month']      = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[1]
        temp_dict['year']       = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split('-')[1].lstrip().split(' ')[2]
        temp_dict['time']       = str(list(data.find_all('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}))[i]).split('title="')[1].split('"><span ')[0].split(' - ')[0]

        # Create a datetime object to be added to the dictionary:
        datetime_object = datetime.strptime(temp_dict['month'] + ' ' + temp_dict['day'] + ' ' + temp_dict['year'] + ' ' + temp_dict['time'].replace(" ", ""), '%b %d %Y %I:%M%p')

        # Add the tweet's datetime of when it was sent out:
        temp_dict['datetime']   = datetime_object

        # Append the temporary dictionary containing the tweet's information to the master_list:
        master_list.append(temp_dict)

        # Print i at every 5th tweet to show the status of the code:
        if i % 5 == 0:
            print(i)
        else:
            continue


    # Turn the 'master_list' into a Pandas DataFrame, and assign to variable 'df':

    df = pd.DataFrame(master_list)

    # Rearrange columns in a more logical order:

    df = df[['handle', 'tweet', 'datetime', 'day', 'month', 'year', 'time']]

    # Save the Pandas DataFrame to a .csv file:

    df.to_csv('twitter_scraped_' + handle + '_df.csv', index=False, sep=",")
