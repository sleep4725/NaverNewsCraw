import os, sys
sys.path.insert(1, os.environ.get("PROJ_ROOT"))
import json 

from common.template import NewsTemplate
from code.sampleCode import Code
from common.urlheader import UrlHeader
from es.client import ES
import requests
from bs4 import BeautifulSoup 
from elasticsearch.helpers import bulk 

##
# 작성일 : 2021-12-09
# 작성자 : 김준현 
## ===========================
class NewsDataGet(UrlHeader):

    def __init__(self, filepath):
        UrlHeader.__init__(self)
        self.filepath = filepath
        self.es_action_list = []
        self.es_client = ES.ret_es_client()
        self.es_index = "naver_news"
        self.config = NewsDataGet.ret_url_config() 

    def data_bulk_indexing(self):
        
        try:
        
            print(len(self.es_action_list))
            bulk(client= self.es_client, actions=self.es_action_list)
        except:
            pass
        else:
            print("적재 성공 !!")


    def news_data_get(self):
        """
        """
        f = open(self.filepath, "r", encoding="utf-8")
        url_list = f.readlines()
        f.close()

        for url in url_list:

            data = json.loads(url)

            url = data["url"].rstrip("\n")
            response = requests.get(url, headers = self._headers)
            print(response.status_code) 
            if response.status_code == 200:
                
                try:
                    bs_object = BeautifulSoup(response.text, "html.parser")
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
                                                      article_category_lv1_eng=data["k"],
                                                      article_category_lv2_eng=data["subk"],
                                                      article_category_lv1_kor=self.config[data["k"]]["kor"],
                                                      article_category_lv2_kor=self.config[data["k"]]["sub_url"][data["subk"]]["kor"])
                                    
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
            else:
                print(response.status_code)
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
