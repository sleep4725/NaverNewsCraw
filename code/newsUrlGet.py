#!/usr/bin/python3

import os, sys
import json
import requests
from bs4 import BeautifulSoup
import pandas
from elasticsearch.helpers import bulk

sys.path.append(os.environ.get("PROJ_ROOT"))

from common.template import NewsTemplate
from common.urlheader import UrlHeader
from sampleCode import Code
from es.client import ES

## ==============
# 2021-12-01
# 작성자 : 김준현
## ==============

class NewsUrlGet(UrlHeader):

    def __init__(self):
        UrlHeader.__init__(self)
        self.config = NewsUrlGet.ret_url_config()
        self.es_action_list = []
        self.es_client = ES.ret_es_client()
        self.es_index = "naver_news"

    def news_data_req(self):
        """

        :return:
        """
        key = [k for k in self.config.keys()]
        for k in key:
            for subk in dict(self.config[k]["sub_url"]).keys():
                news_object = NewsTemplate(sid1=self.config[k]["sid1"], sid2=self.config[k]["sub_url"][subk]["sid2"])
                for page in range(1, 2):
                    url = news_object.url + "&date=20211130&page={_arg_page_}".format(_arg_page_ = page)
                    response = requests.get(url, headers = self._headers)

                    if response.status_code == 200:
                        bs_object = BeautifulSoup(response.text, "html.parser")
                        
                        try:

                            if bs_object.find("td", {"class": "content"}).\
                                    find_next("div", {"class": "content"}).\
                                    find_next("div", {"class": "list_body"}).\
                                    find_next("ul", {"class": "type06_headline"}):
                                type06_headline = bs_object.select_one("td.content > div.content > div.list_body > ul.type06_headline")
                                if type06_headline.find("li"):
                                    for li in type06_headline.select("li"):
                                        if li.find("dl").find_next("dt"):
                                            a_tag = li.select_one("dl > dt > a")
                                            c = Code(url= a_tag.attrs["href"],
                                                     article_category_lv1_eng=k,
                                                     article_category_lv2_eng=subk,
                                                     article_category_lv1_kor=self.config[k]["kor"],
                                                     article_category_lv2_kor=self.config[k]["sub_url"][subk]["kor"])
                                            
                                            c.get_news_data()
                                            self.es_action_list.append(
                                                {
                                                    "_index": self.es_index,
                                                    "_source": c.data
                                                })
                                        
                                    if self.es_action_list:
                                        print("데이터 적재 시작") 
                                        self.data_bulk_indexing()
                                        self.es_action_list.clear()
                        except:
                            print(url)
                            pass
                        else:
                            print("데이터 적재 성공!!")

    def data_bulk_indexing(self):
        """

        :return:
        """
        try:

            print(len(self.es_action_list))
            bulk(client= self.es_client, actions=self.es_action_list)
        except:
            pass
        else:
            print("적재 성공 !!")

    @classmethod
    def ret_url_config(cls)->dict:
        """

        :return:
        """
        config = "../config/url_config.json"
        if os.path.exists(config):
            f = open(config, "r", encoding="utf-8")
            config_json_data = json.load(f)
            f.close()
            return dict(config_json_data)
        else:
            raise FileNotFoundError
    
    def __del__(self):
        try:

            self.es_client.transport.close()
        except:
            pass
### ===========================
# project main function
### ===========================
if __name__ == "__main__":
    o = NewsUrlGet()
    o.news_data_req()
