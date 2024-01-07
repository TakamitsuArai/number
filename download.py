import requests
import datetime
import sys
from variousitems import *
from requests.auth import HTTPDigestAuth

args = sys.argv
print(len(args))
if 3 <= len(args):
    print('検索時間設定なし')
    print('args[1]='+args[1])
    print('args[2]='+args[2])
    r = requests.get('http://'+camera_ip+'/cgi-bin/get_mp4_list?Datafrom='+args[1]+'&Datato='+args[2], auth=HTTPDigestAuth(camera_id, camera_passwd))
else:
    print('古いデータからダウンロード')
    r = requests.get('http://'+camera_ip+'/cgi-bin/get_mp4_list', auth=HTTPDigestAuth(camera_id, camera_passwd))
print("ステータスコードは")
print(r.status_code)
print("ダウンロードファイルは")
print(r.content)
print("内容は")
l = r.text.replace('\r\n',',')
m = l.split(',')
print(m[::3])
for (x,y,z) in zip(m[::3],m[1::3],m[2::3]):
    if(x.find('file') == -1):
        print("実行ファイル名は")
        print(x)
        print(y)
        print(z)
        print(datetime.datetime.now())
        urlData = requests.get('http://'+camera_ip+'/cgi-bin/get_mp4_file?FileName='+x, auth=HTTPDigestAuth(camera_id, camera_passwd)).content
        print("ステータスコードは")
        print(r.status_code)
        with open(y+'_'+z+'_'+x ,mode='wb') as f: # wb でバイト型を書き込める
            f.write(urlData)