import os
from bs4 import BeautifulSoup
from constants import *
import requests
import re


class Scraper:
    data_type_url_mappings = {
        DATA_TYPE_TRAINING: {
            "input": [],
            "output": TRAIN_DATASET_FILE
        },
        DATA_TYPE_TESTING: {
            "input": [],
            "output": TEST_DATASET_FILE
        }
    }

    urls_file = None
    data_type = None

    def __init__(self, data_type=DATA_TYPE_TRAINING):
        self.data_type = data_type
        if data_type == DATA_TYPE_TRAINING:
            self.urls_file = TRAIN_URLS_FILE
        elif data_type == DATA_TYPE_TESTING:
            self.urls_file = TEST_URLS_FILE

        with open(self.urls_file, 'r') as f:
            urls = f.readlines()
            self.data_type_url_mappings[self.data_type]["input"] = urls

    def get_js_soup(self, url):
        resp = None
        try:
            resp = requests.get(url, timeout=5)
        except Exception:
            scheme = url.split('://')[0]
            if scheme not in ['http', 'https']:
                try:
                    print '-' * 5, 'Scraping url : ', 'http://' + url, '-' * 5
                    resp = requests.get('http://' + url, timeout=5)
                except Exception:
                    try:
                        print '-' * 5, 'Scraping url : ', 'https://' + url, '-' * 5
                        resp = requests.get('https://' + url, timeout=5)
                    except Exception:
                        try:
                            print '-' * 5, 'Scraping url : ', 'www.' + url, '-' * 5
                            resp = requests.get('www.' + url, timeout=5)
                        except Exception:
                            print '-' * 5, 'Returning none for url : ', url, '-' * 5
                            return None
            else:
                print '-' * 5, 'Returning none for url : ', url, '-' * 5
                return None

        if resp == None:
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        return soup

    def remove_script(self, soup):
        for script in soup(['script', 'style']):
            script.decompose()
        return soup

    def get_url_text(self, url):
        print '-' * 5, 'Scraping url : ', url, '-' * 5
        soup = self.get_js_soup(url)
        # soup = self.remove_script(soup)
        if not soup:
            return ""
        return soup.get_text(strip=True)

    def extract_url_contents(self):
        output_file = self.data_type_url_mappings[self.data_type]["output"]
        # if not os.path.exists(output_file):
        open(output_file, 'w').close()

        for url in self.data_type_url_mappings[self.data_type]["input"]:
            if self.data_type == DATA_TYPE_TRAINING:
                line_parts = url.split('\t')
                tag = line_parts[0]
                url = line_parts[1]
            url = url.strip()
            data = self.get_url_text(url)
            data_string = self.convert_string_to_ascii(data)
            data_string = re.sub(' +', ' ', data_string)
            data_string = data_string.replace('\n', ' ').replace('\r', ' ').replace('\r\n', ' ')
            if re.findall("403 Forbidden", data_string) or \
                    re.findall("404 Component not found", data_string) or \
                    re.findall("404 Not Found", data_string) or \
                    not data_string:
                data_string = ERROR_CONTENT
            if self.data_type == DATA_TYPE_TRAINING:
                data_string = tag + '\t' + data_string
            output_file = self.data_type_url_mappings[self.data_type]["output"]
            # # if not os.path.exists(output_file):
            # open(output_file, 'w').close()

            with open(output_file, 'a') as f:
                f.write(data_string.encode('utf-8'))
                f.write('\n')
                print "Wrote contents of url : ", url

    def convert_string_to_ascii(self, input_string):
        output_string = input_string
        try:
            output_string = "".join(c for c in input_string if ord(c) < 128)
            if output_string != input_string:
                print "Converted non-ascii string to ascii"
        except Exception:
            print "Couldn't convert non-ascii string to ascii"

        return output_string