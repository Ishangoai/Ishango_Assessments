import requests

r = requests.get('https://coderbyte.com/api/challenges/json/age-counting')

filtered = [s for s in r.json()['data'].split() if 'age=' in s]
final = [''.join(x for x in r if x.isdigit()) for r in filtered]

print(len([x for x in final if int(x)>= 50]))
