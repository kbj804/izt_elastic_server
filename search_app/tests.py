#-*- coding:utf-8 -*-
import requests
import json
import ast

import urllib3

#openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
#accessKey = "aac4fba1-db31-4078-96d9-f21671d9ed9b"


url = 'http://localhost:8000/search_app/?'
method = 'search_content'
word = 'igate'
query = url + method + '=' + word

res = requests.get(query)

# ast => String 타입을 Dic 으로 변환
docs = ast.literal_eval(res.text)

print(json.dumps(docs, indent=4,  ensure_ascii=False)) # json 파일 이쁘게 출력

### 
# print("[responseCode] " + str(response.status))
# print("[responBody]")
# print(str(response.data,"utf-8"))
###


if method == 'search_content':
    string_contents =[]
    for hit in docs['hits'][0:5]:
        #print(hit['_source'])
        content = hit['_source']['content']
        if hit['_source']['data_type'] == 'table':
            for coulm in hit['_source']['content']:
                #print(coulm)
                pass
        
        # String - content
        else:
            for line in content:
                string_contents.append(line)
    passage = '. '.join(string_contents)


#question = "adapter 설정에 대해 알려줘"

    # requestJson = {
    # "access_key": accessKey,
    #     "argument": {
    #         "question": question,
    #         "passage": passage
    #     }
    # }
    
    # http = urllib3.PoolManager()
    # response = http.request(
    #     "POST",
    #     openApiURL,
    #     headers={"Content-Type": "application/json; charset=UTF-8"},
    #     body=json.dumps(requestJson)
    # )

    #print(str(response.data,"utf-8"))
    # p = str(response.data,"utf-8")
    # d = ast.literal_eval(p)
    
    #print(d)
    # print(question)
    # print(d['return_object']['MRCInfo']['answer'] + '합니다')


