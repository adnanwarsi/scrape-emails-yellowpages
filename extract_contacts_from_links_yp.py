"""
Yellow Pages Scraper

This script extracts business information from the Yellow Pages website using a JSON file containing the
list of URLs and outputs the information to a CSV file.

Usage:
    python3 yellow_pages_scraper.py {json_file_with_links}
"""

import csv
import json
import re
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlsplit


def print_usage():
    print('\nusage: \n\n>>>python3 ' + sys.argv[0] + '  {json file with links}\n\n')


if len(sys.argv) < 2:
    print_usage()
    exit()

json_file = sys.argv[1]
csv_file = json_file.split(".")[0] + ".csv"


def extract_business_info(page: str) -> dict:
    bs_obj = BeautifulSoup(page, "html.parser")

    biz_record = {
        "biz_name": "",
        "address": "",
        "url": "",
        "email": "",
        "phone": ""
    }

    biz_card = bs_obj.find("article", class_=re.compile("business-card clearfix ", re.I))

    if biz_card:
        sales_info = biz_card.find('div', {'class': 'sales-info'})
        if sales_info:
            biz_record['biz_name'] = sales_info.text.strip()

        primary_info = biz_card.find('section', {'class': 'primary-info'})
        if primary_info:
            address = primary_info.find('p', {'class': 'address'})
            phone = primary_info.find('p', {'class': 'phone'})
            if address and phone:
                biz_record['address'] = address.text.strip()
                biz_record['phone'] = phone.text.strip()

    card_footer = bs_obj.find('div', {'class': 'business-card-footer'})
    if card_footer:
        email = card_footer.find("a", href=re.compile(r"^mailto:"))
        website = card_footer.find("a", class_=re.compile("secondary-btn website-link", re.I))

        if email:
            biz_record['email'] = email['href'].split(':')[1]

        if website:
            biz_record['url'] = website['href']

    return biz_record


def extract_business_info_from_url(url: str) -> dict:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        response = requests.get(url, headers=headers, verify=True, timeout=10)
        page = response.text
    except Exception as e:
        print(e)
        return {}

    return extract_business_info(page)


with open(json_file) as f:
    data = json.load(f)

for link in data:
    try:
        biz_record = extract_business_info_from_url(link)
        print(json.dumps(biz_record, indent=4))

        if len(biz_record) > 0:
            with open(csv_file, "a", newline='') as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow([biz_record['biz_name'], biz_record['address'], biz_record['phone'], biz_record['url'], biz_record['email']])

    except Exception as e:
        print(e)
