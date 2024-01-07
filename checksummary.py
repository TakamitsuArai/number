import requests
from variousitems import *
from requests.auth import HTTPDigestAuth

print("送信CGIは")
print('http://'+camera_ip+'/cgi-bin/get_recording_summary')
r = requests.get('http://'+camera_ip+'/cgi-bin/get_recording_summary', auth=HTTPDigestAuth(camera_id, camera_passwd))
print("ステータスコードは")
print(r.status_code)
print("内容は")
print(r.text)
