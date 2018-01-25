import requests

url = "http://fanyi.sogou.com/reventondc/multiLangTranslate"
hd = {'content-type': "application/x-www-form-urlencoded",
      'Accept': "application/json", }
res = requests.post(url, headers=hd)
