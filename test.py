import sys
import base64

ENCODING = sys.stdout.encoding if sys.stdout.encoding else 'utf-8'
#print ('{ "id": 1, \"name": "林喔喔喔", \"price": 12.50, \"tags": ["home", "green"]} ')

#print (('{ "id": 1, \"name": "林喔喔喔", \"price": 12.50, \"tags": ["home", "green"]}').encode("utf-8"))
a = '林宜德! 666!'
print (base64.b64encode(a.encode('utf-8')).decode('utf-8'))
