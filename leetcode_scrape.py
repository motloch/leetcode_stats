"""
For users listed in usernames.txt this code scrapes Leetcode for statistics about 
1) the number of solved problems and 
2) percentage of users 'beaten'
and saves the results into results.csv.
"""

from seleniumwire.webdriver import Chrome
from seleniumwire import webdriver
import time
import json
import brotli
import pandas as pd

options = webdriver.ChromeOptions() # Do not open the browser window
options.add_argument("--headless")

usernames = open('usernames.txt').read().splitlines()

results = []

for username in usernames:
    print(username)

    # Open the website and wait sufficiently long to make sure everything is downloaded.
    # We decide to open a new connection for each user, to avoid filtering requests
    # later.
    driver = Chrome(options = options)
    driver.get("https://leetcode.com/" + username)
    time.sleep(6)
    
    # Find the appropriate Graphql request
    for request in driver.requests:
        if str(request) == 'https://leetcode.com/graphql/':
            if 'userProblemsSolved' in str(request.body):

                # extract dictionaries with numbers of solved problems and percentages
                response_body = request.response.body
                decompressed_response_body = brotli.decompress(response_body)
                unpacked_info = json.loads(decompressed_response_body)['data']['matchedUser']
                dict_beats = unpacked_info['problemsSolvedBeatsStats']
                dict_nums  = unpacked_info['submitStatsGlobal']['acSubmissionNum']

                # combine the user information into a single dictionary and store the result
                current = {'username': username}
                for d in dict_beats:
                    current[d['difficulty']+ '_pct'] = d['percentage']
                for d in dict_nums:
                    current[d['difficulty']+ '_num'] = d['count']
                results.append(current)

    driver.quit() # To avoid too many opened connections

# Save the results into a file
pd.DataFrame(results).to_csv('results.csv', index=False)
