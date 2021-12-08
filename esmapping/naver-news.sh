#!/bin/bash


#!/bin/bash

curl -XPUT "http://:9200/naver_news?pretty=true" -H "Content-Type: application/json" -d '
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "article_category_lv1_eng": {"type": "keyword"},
            "article_category_lv2_eng": {"type": "keyword"},
            "article_category_lv1_kor": {"type": "keyword"},
            "article_category_lv2_kor": {"type": "keyword"},
            "newspaper_name": {"type": "keyword"},
            "article_title": {"type": "keyword"},
            "article_content": {"type": "text"},
            "publish_date": {"type": "date", "format": "yyyy.MM.dd. HH:mm"},
            "cllct_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:SS"},
            "url": {"type": "text"}
        }
    }
}'
