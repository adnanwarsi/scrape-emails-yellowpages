"""
Yellow Pages Scraper

This script scrapes business listings from Yellow Pages based on a given category webpage.
It extracts the links for individual businesses and saves them in a JSON file.

Usage:
    python3 yellow_pages_scraper.py {category_list_webpage}

Example:
    python3 yellow_pages_scraper.py https://www.yellowpages.com/san-diego-ca/auto-repair
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from typing import List


def print_usage() -> None:
    """
    Print the script usage message.
    """
    print(f'\nusage: \n\n>>>python3 {sys.argv[0]}  {{category lists webpage}}\n\n')


def get_website_base(url: str) -> str:
    """
    Return the base URL for a given URL.

    Args:
        url: The URL to get the base from.

    Returns:
        The base URL as a string.
    """
    link_parts = urlsplit(url)
    return f"{link_parts.scheme}://{link_parts.netloc}"


def scan_page_list(webpage_url: str) -> List[str]:
    """
    Scan a Yellow Pages category webpage and extract business listing URLs.

    Args:
        webpage_url: The URL of the category webpage.

    Returns:
        A list of business listing URLs.
    """
    website_base = get_website_base(webpage_url)
    business_records = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }

    while True:
        print(webpage_url)

        try:
            response = requests.get(webpage_url, headers=headers, verify=True, timeout=10)
        except Exception as e:
            print(f'FAILURE : unable to process website : {webpage_url}\n{e}')
            break

        bsObj = BeautifulSoup(response.text, "html.parser")

        for result in bsObj.find_all('div', {'class': 'result'}):
            for vcard in result.find_all('div', {'class': 'v-card'}):
                info = vcard.find('div', {'class': 'info'})

                if info and info.find('a', {'class': 'business-name'}):
                    business_link = info.find('a', {'class': 'business-name'})['href']
                    business_link_base = get_website_base(business_link)

                    if business_link_base == "://":
                        business_records.append(website_base + business_link)

        # Check if there is a next page
        pagination = bsObj.find('div', {'class': 'pagination'})
        next_page_link = pagination.find('a', {'class': 'next ajax-page'})
        if next_page_link:
            webpage_url = website_base + next_page_link['href']
        else:
            break

    return business_records


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        exit()

    website_category_listpage = sys.argv[1]
    json_out_file = f"{website_category_listpage.split('/')[-1]}.json"

    record_links = scan_page_list(website_category_listpage + '?page=1')
    print(json.dumps(record_links, indent=4))

    with open(json_out_file, 'w') as outfile:
        json.dump(record_links, outfile, indent=4, sort_keys=True)
