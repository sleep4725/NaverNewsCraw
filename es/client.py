from elasticsearch import Elasticsearch
import yaml 


## ==============
# 2021-12-01
# 작성자 : 김준현
## ==============
class ElasticClusterHealthBad(Exception):
    def __init__(self):
        super().__init__('Elastic Cluster가 건강하지 않습니다.')

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
            es_hosts = [f"http://{h}:{es_config['esPort']}" for h in es_config["esHosts"]]
            es = Elasticsearch(hosts=es_hosts)
            
            resp = es.cluster.health()
            
            if resp["status"] == "green" or resp["status"] == "yellow":
                return es
            else:
                raise ElasticClusterHealthBad
