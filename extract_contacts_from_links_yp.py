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

def print_usage():
    print ('\nusage: \n\n>>>python3 ' + sys.argv[0] + '  {json file with links}\n\n')

if len(sys.argv) < 2:
    print_usage()
    exit()

json_file = sys.argv[1]

# output file is the same as script name with extension .csv
csvfile = json_file.split(".")[0] + ".csv"

# websitename = 'https://www.yellowpages.com/san-diego-ca/mip/aamco-transmissions-total-car-care-464649561?lid=1000786841226'
# websitename = 'https://www.yellowpages.com/san-diego-ca/mip/rapid-transmissions-6445956?lid=6445956'
# websitename = 'https://www.yellowpages.com/san-diego-ca/mip/ace-muffler-shop-532191566?lid=1001059678328'

def biz_info_extract_from_page_extracted(page):
    bsObj = BeautifulSoup(page, "html.parser")

    # return_record = {}
    biz_record = {
        "biz_name":"",
        "address":"",
        "url":"",
        "email":"",
        "phone": ""

    }


    # if bsObj.find(itemtype=re.compile("http://schema.org/LocalBusiness", re.I)):
    # emaple page 'https://www.mysandiego.org/business/3275/game-design-schools/internet-online-consulting/san-diego-california/'


    # if bsObj.find('article', {'class': 'business-card clearfix non-paid-listing'}):
    if bsObj.find("article", class_=re.compile("business-card clearfix ", re.I)):
        # print ("\n\n\nfound biz_card")
        # biz_card = bsObj.find('article', {'class': 'business-card clearfix non-paid-listing'}) # print (biz_card)
        biz_card = bsObj.find("article", class_=re.compile("business-card clearfix ", re.I)) # print (biz_card)

        if biz_card.find('div', {'class': 'sales-info'}):
            # print ("\n\n\nfound sales_info")
            biz_record['biz_name'] = biz_card.find('div', {'class': 'sales-info'}).text.strip()

        if biz_card.find('section', {'class': 'primary-info'}):
            # print ("\n\n\nfound primary_info")
            primary_info = biz_card.find('section', {'class': 'primary-info'})
            # print (primary_info)
            if primary_info.find('p', {'class': 'phone'}):
                biz_record['address'] = primary_info.find('p', {'class': 'address'}).text.strip()
                biz_record['phone'] = primary_info.find('p', {'class': 'phone'}).text.strip()

    if bsObj.find('div', {'class': 'business-card-footer'}):
        card_footer = bsObj.find('div', {'class': 'business-card-footer'})

        if card_footer.find("a", class_=re.compile("email-business", re.I)):
            biz_record['email'] = card_footer.find("a", href=re.compile(r"^mailto:"))['href'].split(':')[1]

        if card_footer.find("a", class_=re.compile("secondary-btn website-link", re.I)):
            biz_record['url'] = card_footer.find("a", class_=re.compile("secondary-btn website-link", re.I))['href']

    return biz_record


def biz_info_extract_from_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        r = requests.get(url, headers=headers, verify=True, timeout=10)
        page = r.text
    except Exception as e:
        print (e)
        return data

    return biz_info_extract_from_page_extracted(page)



# read the json records
with open(json_file) as f:
    data = json.load(f)

# open the csv file

for link in data:
    try:
        biz_record = biz_info_extract_from_url(link)

        print(json.dumps(biz_record, indent=4))

        if len(biz_record) > 0:
            with open(csvfile, "a", newline='') as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow([biz_record['biz_name'],biz_record['address'],biz_record['phone'],biz_record['url'],biz_record['email']])
            output.close()

    except Exception as e:
        print (e)

