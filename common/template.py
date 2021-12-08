"""
https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=265&sid1=100&date=20211130&page=2
"""
import urllib.parse

## ==============
# 2021-12-01
# 작성자 : 김준현
## ==============

class NewsTemplate:

    def __init__(self, sid1=None, sid2=None):
        self.req_url = "https://news.naver.com"
        self.req_url_path = "/main/list.naver"
        self.req_params = urllib.parse.urlencode({
            "mode": "LS2D",
            "mid": "shm",
            "sid1": sid1,
            "sid2": sid2
        })

        self.url = self.url_assembly()

    def url_assembly(self)-> str:
        """

        :return:
        """
        return self.req_url + self.req_url_path + "?" + self.req_params

