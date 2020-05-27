import requests

r2 = requests.get("https://www.allrecipes.com/recipes/96/salad/")
r1 =requests.get("http://www.example.com/", headers={"content-type":"text"})

print(f'{r1.status_code} status of first request')
print(f'{r2.status_code} status of 2nd request')
print(f'{r2.text} above is the text of 2nd request')
print(f'{r2.encoding}  is the encoding of 2nd request')
print(f'{r2.headers} \n above is the headers of 2nd request')

# headers – (optional) Dictionary of HTTP Headers to send with the Request
print(requests.codes['temporary_redirect'])
print(requests.codes['teapot'])
print(requests.codes['ok'])
