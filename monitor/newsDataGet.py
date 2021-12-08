import os, sys
sys.path.append(os.environ.get("PROJ_ROOT"))

from common.urlheader import UrlHeader
from es.client import ES
import requests
from bs4 import BeautifulSoup 

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
            response = requests.get(url, headers = self._headers)
            
            if response.status_code == 200:
                
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

