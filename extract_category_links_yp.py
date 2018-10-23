from bs4 import BeautifulSoup
import re
import json
import requests
import csv
import sys
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import os

# append the "?page=1" so on
# website_category_listpage = 'https://www.yellowpages.com/san-diego-ca/auto-repair'
# website_category_listpage = 'https://www.yellowpages.com/san-diego-ca/oil-change'


def print_usage():
    print ('\nusage: \n\n>>>python3 ' + sys.argv[0] + '  {category lists webpage}\n\n')

if len(sys.argv) < 2:
    print_usage()
    exit()

website_category_listpage = sys.argv[1]

# output file is the same name with extension .json
json_out_file = website_category_listpage.split("/")[-1] + ".json"


def page_list_scan(webpage_url):

    link_parts = urlsplit(webpage_url)
    website_base = "{0.scheme}://{0.netloc}".format(link_parts)

    biz_records = []

    while True:
        try:
            print (webpage_url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            }

            response = requests.get(webpage_url, headers=headers, verify=True, timeout=10)
            # print (response.text)

        except Exception as e:
            print('FAILURE : unable to process website : ' + websitename + '\n' + str(e))
            break

        bsObj = BeautifulSoup(response.text, "html.parser")

        for result in bsObj.find_all('div', {'class': 'result'}):
            # print ("FOUND : result")
            for vcard in result.find_all('div', {'class': 'v-card'}):
                # print ('FOUND v-card')
                for info in vcard.find('div', {'class': 'info'}):
                     #print ("FOUND : info")
                    if info.find('a', {'class': 'business-name'}):
                        #print ('found business-name')
                        bizlink = info.find('a', {'class': 'business-name'})['href']

                        biz_link_parts = urlsplit(bizlink)
                        biz_link_base = "{0.scheme}://{0.netloc}".format(biz_link_parts)

                        if biz_link_base == "://":
                            # print (website_base + bizlink)
                            biz_records.append(website_base + bizlink)

        # check if there is next page
        pagination = bsObj.find('div', {'class': 'pagination'})
        if pagination.find('a', {'class':'next ajax-page'}):
            webpage_url = website_base + pagination.find('a', {'class': 'next ajax-page'})['href']
        else:
            break

    return biz_records


record_links = page_list_scan (website_category_listpage + '?page=1')
print(json.dumps(record_links, indent=4))

with open(json_out_file, 'w') as outfile:
    json.dump(record_links, outfile, indent=4, sort_keys=True)
outfile.close()
