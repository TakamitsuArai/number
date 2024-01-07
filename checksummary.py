import requests
import datetime
from variousitems import *
from requests.auth import HTTPDigestAuth

print("送信CGIは")
print('http://'+camera_ip+'/cgi-bin/get_recording_summary')
r = requests.get('http://'+camera_ip+'/cgi-bin/get_recording_summary', auth=HTTPDigestAuth(camera_id, camera_passwd))
print("ステータスコードは")
print(r.status_code)
print("内容は")
print(r.text)

datafrom = datetime.datetime(int(r.text[9:13]),int(r.text[13:15]), int(r.text[15:17]), \
                            int(r.text[18:20]), int(r.text[20:22]), int(r.text[22:24]), \
                                int(r.text[25:27])*10000)
print(datafrom)
datato = datetime.datetime(int(r.text[40:44]),int(r.text[44:46]), int(r.text[46:48]), \
                            int(r.text[49:51]), int(r.text[51:53]), int(r.text[53:55]), \
                                int(r.text[56:58])*10000)

print(datato)

