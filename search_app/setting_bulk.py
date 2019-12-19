from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

with open(r"./search_app/menual_data.json", encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())

es.indices.create(
    index='menual',
    #doc_type='menual_datas',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "menual_datas": {
                "properties": {
                    "data_type": {
                        "type": "text"
                    },
                    "main_title": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },
                    "sub_title": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "my_analyzer"
                    }
                }
            }
        }
    }
)

body =""
for i in json_data:
    body = body + json.dumps({"index": {"_index": "menual", "_type": "menual_datas"}}) + '\n'
    body = body + json.dumps(i, ensure_ascii=False) + '\n'

es.bulk(body)
