import json
import urllib2
url = "http://httpbin.org/get"
response = urllib2.urlopen(url)
data = response.read()
values = json.loads(data)
