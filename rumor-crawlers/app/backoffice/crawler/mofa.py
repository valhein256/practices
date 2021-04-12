import traceback
import requests
import re
import os
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

from . import crawlerProp
from .crawler import Crawler
from utils.settings import Settings
from utils.logger import logger
from models.aws.ddb.rumor_model import RumorModel


def extract_rumor_id(content_soup):
    try:
        link_obj = content_soup.find('a')
        content = link_obj.attrs['href']
        return content.split("typeid=")[1]
    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def extract_rumor_path(content_soup):
    try:
        link_obj = content_soup.find('a')
        content = link_obj.attrs['href']
        return content
    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def extract_rumor_date(content_soup):
    try:
        td_soup = content_soup.find('td', attrs={"class": "CCMS_jGridView_td_Class_0 is-center"})
        rumor_date = td_soup.text
        return rumor_date
    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def extract_clarification(content_soup):
    try:
        div_obj = content_soup.find('div', attrs={"class": "area-essay page-caption-p"})
        clarification = "".join(div_obj.text.split())
        return clarification
    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def extract_title(content_soup):
    try:
        div_obj = content_soup.find('div', attrs={"class": "simple-text title"})
        title = "".join(div_obj.text.split())
        return title
    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def remove_redundant_word(sentence):
    try:
        for word in crawlerProp.REDUNDANT:
            sentence = sentence.replace(word, "")

        if sentence.startswith("，"):
            sentence = sentence[1:]

        for i in range(3):
            sentence = sentence.strip()
            if sentence.endswith("，"):
                sentence = sentence[:-1]

        return sentence

    except Exception:
        msg = traceback.format_exc()
        logger.error(f"Error: {msg}")
        return None


def gen_id(data):
    hash = hashlib.sha1()
    hash.update(data.strip().encode("utf-8"))
    return hash.hexdigest()


class MofaCrawler():
    def __init__(self, setting):
        self.page_url = setting.mofa_page_url
        self.domain = setting.mofa_domain
        self.source = setting.mofa_source

    def source(self):
        return self.source

    def fetch_latest_create_date_of_rumor(self):
        for rumor in RumorModel.source_create_date_index.query(self.source,
                                                               limit = 1,
                                                               scan_index_forward = False):
            return rumor.create_date

    def query(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None

        except Exception:
            msg = traceback.format_exc()
            logger.error(f"Error: {msg}")
            return None

    def parse_rumor_pages(self, date):
        try:
            rumor_infos = []
            done = False
            pn = 1
            while not done:
                url = f"{self.page_url}&page={pn}&PageSize=20"
                print(pn, url)
                html_content = self.query(url)
                html_soup = BeautifulSoup(html_content, 'lxml')
                tbody_soup = html_soup.find('tbody')
                tr_objs = tbody_soup.find_all("tr")
                if tr_objs:
                    for tr in tr_objs:
                        rumor_date = extract_rumor_date(tr)
                        if datetime.strptime(rumor_date, "%Y-%m-%d") >= date:
                            rumor_path = extract_rumor_path(tr)
                            rumor_url = f"{self.domain}/{rumor_path}"
                            rumor_info = (rumor_url, rumor_date)
                            if rumor_info not in rumor_infos:
                                rumor_infos.append((rumor_url, rumor_date))
                            else:
                                done = True
                                break
                        else:
                            done = True
                            break
                    if not done:
                        pn += 1
                else:
                    done = True
            return rumor_infos

        except Exception:
            msg = traceback.format_exc()
            logger.error(f"Error: {msg}")
            return []

    def parse_rumor_content(self, rumor_info):
        try:
            (url, date) = rumor_info
            html_content = self.query(url)
            html_soup = BeautifulSoup(html_content, 'lxml')

            clarification = extract_clarification(html_soup)
            original_title = extract_title(html_soup)
            title = remove_redundant_word(original_title)

            posted_item = {
                "id": gen_id(url),
                "clarification": clarification,
                "create_date": date,
                "title": title,
                "original_title": original_title,
                "rumors": [
                    title,
                ],
                "link": url,
                "source": self.source
            }
            logger.info("MOFA rumor item: {}".format(posted_item))
            return posted_item

        except Exception:
            msg = traceback.format_exc()
            logger.error(f"Error: {msg}")
            raise