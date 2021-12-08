from elasticsearch import Elasticsearch
import yaml 


## ==============
# 2021-12-01
# 작성자 : 김준현
## ==============
class ES:

    @classmethod
    def ret_es_client(cls)-> Elasticsearch:
        """

        :return:
        """
        try:

            f=open("/home/kim/my_proj/config/es_config.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
        else:
            es_config = yaml.safe_load(f)
            f.close()
            es = Elasticsearch(hosts=es_config["esHosts"])
            return es
