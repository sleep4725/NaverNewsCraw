import os, sys
import requests
import time
from bs4 import BeautifulSoup
import unicodedata
import re

sys.path.insert(0, os.environ.get("PROJ_ROOT"))

from es.client import ES
from common.urlheader import UrlHeader
from nature_analyzer.nature import Nature


## ==============
# 2021-12-01
# 작성자 : 김준현
## ==============

class Code(UrlHeader):

    def __init__(self, url,
                 article_category_lv1_eng: None,
                 article_category_lv2_eng: None,
                 article_category_lv1_kor: None,
                 article_category_lv2_kor: None):
        UrlHeader.__init__(self)
        self._url = url
        # ==================
        self.data = {
            "article_category_lv1_eng": article_category_lv1_eng,
            "article_category_lv2_eng": article_category_lv2_eng,
            "article_category_lv1_kor": article_category_lv1_kor,
            "article_category_lv2_kor": article_category_lv2_kor,
            "newspaper_name": "",  # 기사를 낸 언론사 이름
            "article_title": "",   # 기사 제목
            "article_content": "", # 기사 내용
            "publish_date": time.strftime("%Y.%m.%d. %H:%M", time.localtime()),  # 기사 발행 시각 2021.12.02.10:45
            "cllct_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), # 데이터 적재 시각
            "nng_list": [],
            "url": self._url # 요청 url
        }
        self._es_client = ES.ret_es_client()


    def article_body_parcing(self, article_body):
        """
        :return:
        """
        #self.data["article_content"] = str(re.sub('\s+', ' ', unicodedata.normalize("NFKD",article_body.text))).strip()
        article_content = str(article_body.text).\
                lstrip("\n\n\n\n\n// flash").\
                lstrip("오류를 우회하기 위한 함수 추가").\
                lstrip("\\nfunction _flash_removeCallback() {}\n\n").\
                strip()
                
        #self.data["article_content"] = str(article_body.text).replace("\n\n\n\n\n// flash", "").replace("\nfunction _flash_removeCallback() {}\n\n", " ").strip()
        self.data["article_content"] = article_content 
        nature_object = Nature(plaintext=self.data["article_content"])
        self.data["nng_list"].extend(nature_object.get_nng())


    def article_header_parcing(self, article_header)-> dict:
        """

        :param article_header:
        :return:
        """

        # ================
        # 신문사 이름
        # ================
        if article_header.find("div", {"class": "press_logo"}):
            press_logo = article_header.select_one("div.press_logo")
            if press_logo.find("a").find("img"):
                newspaper_name = press_logo.select_one("a > img").attrs["title"]
                self.data["newspaper_name"] = newspaper_name
            else:
                print("not find img a_tag")
        else:
            print("not find div.press_logo")
        

        # ==============================
        # 뉴스 기사 타이틀 및 기사 발행 시각
        # ==============================
        if article_header.find("div", {"class": "article_info"}):
            article_info = article_header.select_one("div.article_info")
            if article_info.find("h3", {"id": "articleTitle"}):
                article_title = article_info.select_one("h3#articleTitle")
                self.data["article_title"] = article_title.string
            else:
                print("not find h3#id_articleTitle")

            if article_info.find("div", {"class": "sponsor"}).find_next("span", {"class": "t11"}):
                article_t11 = article_info.select_one("div.sponsor > span.t11")
                article_t11 = str(article_t11.string).replace(" ", "").replace("오전", " ").replace("오후", " ")

                if article_t11:
                    # 2021.11.30. 8:29
                    time_string = article_t11.split(" ")
                    hour, minute = time_string[1].split(":")
                    hour = "%02d"%(int(hour))
                    minute = "%02d"%(int(minute)) 
                    
                    article_t11 = f"{time_string[0]} {hour}:{minute}"
                    self.data["publish_date"] = article_t11
        else:
            print("not find div.article_info tag")

        return self.data

    def get_news_data(self):
        """

        :return:
        """
        resp = requests.get(self._url, headers = self.headers)
        if resp.status_code == 200:
            print("응답 코드 200 입니다.")
            bs_object = BeautifulSoup(resp.text, "html.parser")

            if bs_object.find("td", {"class": "content"}):
                print("td content exists")
                td_content = bs_object.select_one("td.content")
                if td_content.find("div", {"class": "article_header"}):
                    print("div article_header exists")
                    article_header = td_content.select_one("div.article_header")
                    self.article_header_parcing(article_header= article_header)
                else:
                    print("not tag article_header")

                if td_content.find("div", {"id": "articleBody"}):
                    article_body = td_content.select_one("div#articleBody")
                    if article_body.find("div", {"id": "articleBodyContents"}):
                        article_body_contents = article_body.select_one("div#articleBodyContents")
                        self.article_body_parcing(article_body=article_body_contents)
                else:
                    print("not tag articleBody")
            else:
                print("not td content")
        else:
            print("요청 에러")
        
        print(self.data)

    def data_check(self):
        """

        :return:
        """
        print(self.data)

    def __del__(self):
        try:
            self._es_client.transport.close()
        except:
            pass

#if __name__ == "__main__":
#    o = Code(url="https://news.naver.com/main/read.naver?mode=LS2D&mid=shm&sid1=101&sid2=259&oid=015&aid=0004644329")
#    o.get_news_data()

