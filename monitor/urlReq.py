#!/usr/bin/python3
import requests
import os
import sys
sys.path.insert(0, os.environ.get("PROJ_ROOT"))
from bs4 import BeautifulSoup
from celery import Celery 

from monitor.newsDataGet import NewsDataGet
# ====================
# 작성일 : 2021-12-09
# 작성자 : 김준현
# ====================

app = Celery("news_data_get", broker='pyamqp://kjh:1234@localhost//')

@app.task(ignore_result=True) 
def news_data_get(filepath: str):
    """ test
    """
    o = NewsDataGet(filepath)
    o.news_data_get()
