import json
from urllib import request,error,parse

def parse_json(data):
    jsonobj = json.loads(data) # access jsonobj like a dict

    if "title" in jsonobj['metadata']:
        print("*"*50)
        print(jsonobj['metadata']['title'])
    print(jsonobj['metadata']['count'])    

def main():
    urlData = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson'
    webUrl =  request.urlopen(urlData)
    print("Result Code:" + str(webUrl.getcode())) # 200
    if(webUrl.getcode() == 200):
        data=webUrl.read()
        parse_json(data)
        print(data)
    else:
        print("Invalid response.")

if __name__ == '__main__':
    main()
