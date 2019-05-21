import os
import time
from typing import Dict
from urllib.parse import urlparse

import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

webdriver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
chromium_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'headless-chromium')

chrome_options = Options()
chrome_options.binary_location = chromium_path
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920x1080')


def load_conf() -> Dict[str, Dict]:
    """
    Loads a yaml file of sites with js as key-value pairs

    Returns:
        A dictionary, site and tag key-value pairs.
    """
    js_tags = {}
    base_path = os.path.dirname(__file__)

    with open(os.path.join(base_path, 'sites.yaml'), 'r') as conf:
        sites = yaml.load(conf, Loader=yaml.FullLoader)

        for site, data in sites['sites'].items():
            js_tags[site] = data

    return js_tags


def format_url(url: str) -> str:
    """
    Removes query strings and scheme from a url or any leading slashes if given a relative url

    Args:
        url: A url string

    Returns:
        The processed url string
    """

    parsed_url = urlparse(url)

    return parsed_url.netloc + parsed_url.path


def scrape_site(url: str) -> Dict[str, str]:
    """
    Scrapes a url and returns a set of sites with matching tags in the document

    Args:
        url: The site to be scraped

    Returns:
        A set of strings of sites with matching tags in the scraped site
    """

    matched_sites = {}
    js_conf = load_conf()
    browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
    browser.get(url)
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()
    scripts = [format_url(script.attrs['src']) for script in soup('script') if script.attrs.get('src')]

    for site, data in js_conf.items():

        for script in data['scripts']:
            if script in scripts:
                matched_sites[data['name']] = data['homepage']

    return matched_sites


if __name__ == '__main__':
    sites = scrape_site('https://mossy.jp/')
    print(sites)
