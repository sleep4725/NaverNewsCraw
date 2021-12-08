#!/usr/bin/python3

import os, sys
import json
import requests
from bs4 import BeautifulSoup
import pandas
import datetime, time
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

    def __init__(self, day):
        UrlHeader.__init__(self)
        self.config = NewsUrlGet.ret_url_config()
        self.file_generate_date = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.target_day = day

    def news_data_req(self):
        """

        :return:
        """
        key = [k for k in self.config.keys()]
        for k in key:
            for subk in dict(self.config[k]["sub_url"]).keys():
                news_object = NewsTemplate(sid1=self.config[k]["sid1"], sid2=self.config[k]["sub_url"][subk]["sid2"])
                
                f = open(f"/home/kim/my_proj/file/naver_news_{k}_{subk}_{self.file_generate_date}.log", "a", encoding="utf-8")
                
                for page in range(1, 10):
                    url = news_object.url + "&date={_arg_day_}&page={_arg_page_}".format(_arg_day_= self.target_day, _arg_page_ = page)
                    f.write(url + "\n")
                
                f.close()

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
    # ===========================
    #
    # ===========================
    days_ago = datetime.datetime.now() - datetime.timedelta(days=1)
    days_ago = days_ago.strftime("%Y%m%d")
    o = NewsUrlGet(day= days_ago)
    o.news_data_req()
