import requests
import datetime
import sys
import os
from variousitems import *
from requests.auth import HTTPDigestAuth

args = sys.argv
nfst_flg = 0

os.makedirs(savedir, exist_ok=True)
while True:
    if 3 <= len(args) and nfst_flg == 0:
        print('args[1]:'+args[1])
        print('args[2]:'+args[2])

        ddatafrom_datetime = datetime.datetime(int(args[1][0:4]),int(args[1][4:6]), int(args[1][6:8]), \
                                int(args[1][9:11]), int(args[1][11:13]), int(args[1][13:15]), \
                                    0)
        print(ddatafrom_datetime)

        ddatato_datetime = datetime.datetime(int(args[2][0:4]),int(args[2][4:6]), int(args[2][6:8]), \
                                int(args[2][9:11]), int(args[2][11:13]), int(args[2][13:15]), \
                                    0)
        print(ddatato_datetime)

        datafrom=args[1]
        datato=args[2]
    elif nfst_flg == 0:
        print('古いデータから全ダウンロード')
        ddatafrom_datetime = datetime.datetime(2023,1,1,0,0,0,0)
        ddatato_datetime = datetime.datetime(2027,1,1,0,0,0,0)
        datafrom='20230101T000000Z'
        datato='20270101T000000Z'
    else:
        print('指定開始時刻:'+datafrom)
        print('指定終了時刻:'+datato)
    r = requests.get('http://'+camera_ip+'/cgi-bin/get_mp4_list?Datafrom='+datafrom+\
                    '&Datato='+datato, auth=HTTPDigestAuth(camera_id, camera_passwd))
    nfst_flg = 1
    print('CGI配信実施')
    print('ステータスコード(200だと成功):'+str(r.status_code))
    if r.status_code != 200:
        print('Error')
        break
#    print("ダウンロードファイルは")
#    print(r.content)
    print('今回のダウンロードファイル個数(100この場合は継続有):' + str(int(r.text[r.text.find('Mp4fileNum=')+11:])) + '個')
    l = r.text.replace('\r\n',',')
    m = l.split(',')
    if m[0].find('file') != -1:
        print('SD録画 終了です')
        break
    print('今回ダウンロードファイル開始時刻:'+m[1])
    print('今回ダウンロードファイル終了時刻:'+m[-4])
    # 繰り返しダウンロードする
    for (x,y,z) in zip(m[::3],m[1::3],m[2::3]):
        if(x.find('file') == -1):
            print('実行ファイル名:'+x+', 開始時刻:'+y+', 終了時刻:'+z)
            print('現在時刻:'+str(datetime.datetime.now()))
            #すでにファイルがある場合は処理をしない
            if os.path.isfile(savedir+'/'+y+'_'+z+'_'+x) == False:
                urlData = requests.get('http://'+camera_ip+'/cgi-bin/get_mp4_file?FileName='+x, auth=HTTPDigestAuth(camera_id, camera_passwd)).content
                print('CGI配信実施')
                print('ステータスコード:'+str(r.status_code))
                with open(savedir+'/'+y+'_'+z+'_'+x ,mode='wb') as f: # wb でバイト型を書き込める
                    f.write(urlData)
    #ダウンロードした最後の時刻
    if int(m[-4][13:15]) != 99:
        predatato = datetime.datetime(int(m[-4][0:4]),int(m[-4][4:6]), int(m[-4][6:8]), \
                                      int(m[-4][9:11]), int(m[-4][11:13]), int(m[-4][13:15])+1, \
                                        0)
    else:
        predatato = datetime.datetime(int(m[-4][0:4]),int(m[-4][4:6]), int(m[-4][6:8]), \
                                      int(m[-4][9:11]), int(m[-4][11:13]), int(m[-4][13:15]), \
                                        0)

    if predatato < ddatato_datetime:
        datafrom = predatato.strftime( '%Y%m%dT%H%M%SZ')
        ddatafrom_datetime = predatato
    print('SD録画再要求開始時刻:'+datafrom)

