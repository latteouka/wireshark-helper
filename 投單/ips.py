#! python3

# -*- coding: utf-8 -*-
import sys
import time
import csv
from datetime import datetime
import re
from ipwhois import IPWhois
from pprint import pprint


def which_isp(ip):

    is_twm = False

    if '49.214.' in ip:
        is_twm = True
    elif '49.215.' in ip:
        is_twm = True
    elif '49.216.' in ip:
        is_twm = True
    elif '49.217.' in ip:
        is_twm = True
    elif '49.218.' in ip:
        is_twm = True
    elif '49.219.' in ip:
        is_twm = True
    elif '175.96.' in ip:
        is_twm = True
    else:
        is_twm = False
    
    #print(ip)
    results = IPWhois(ip).lookup_rdap(asn_methods=['dns', 'whois', 'http'])

    print(results['network']['name'])
    

    if is_twm:
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'HINET-NET':
        return '中華電信網路', '使用者資料'
    elif results['network']['name'] == 'EMOME-NET':
        return '中華電信行動', '使用者資料'
    elif results['network']['name'] == 'taiwanmobile-net':
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'TAIWANMOBILE-NET':
        return '台灣大哥大', '使用者資料'
    elif results['network']['name'] == 'FETNET-NET':
        return '遠傳電信股份有限公司', '使用者資料'
    elif results['network']['name'] == 'FEG-MPLS-NETWORK-NET':
        return '遠傳電信股份有限公司', '使用者資料'
    elif results['network']['name'] == 'VIBO-NET':
        return '台灣之星', '使用者資料'
    elif results['network']['name'] == 'VEETIME-TW':
        return '大台中數位有線電視股份有限公司', '歷史查詢'
    elif results['network']['name'] == 'APT':
        return '亞太電信', '歷史查詢'
    elif results['network']['name'] == 'APOL-NET':
        return '亞太電信', '歷史查詢'
    elif results['network']['name'] == 'TFN-NET':
        return '台灣固網', '歷史查詢'
    elif results['network']['name'] == 'NCICNET-NET':
        return '新世紀資通請發文', '使用者資料'
    else:
        return '不能投單的業者', '使用者資料'
        

    
    
    

'''
CSV批次匯入調取條件功能，可用格式如下
使用CSV檔案，即逗號分隔之文字檔案。
第一欄：調取類別，條列如下：行動電話、市內電話、IP
第二欄：電信業者名稱，行動與市話將自動使用號碼可攜資料庫取得服務業者，輸入"-"即可；IP需指定業者，條列如下：中華電信網路、亞太電信、台灣大哥大、台灣之星、台灣固網、遠傳電信股份有限公司、大台中數位有線電視股份有限公司、安源通訊股份有限公司
第三欄：調取內容，行動電話須為8869xxxxxxxx，市話須為02-xxxxxxxx，IP為x.x.x.x。
第四欄：調取開始時間。格式為：yyyymmddhhmiss，意義如下yyyy:四碼西元年；mm:兩碼月份；dd:兩碼日期；hh:24小時制兩碼時；mi:兩碼分；ss:兩碼秒。
第五欄：調取結束時間。格式同上。
第六欄：調取種類：通信紀錄:雙向、通信紀錄:發話、通信紀錄:網路、使用者資料、歷史查詢。各業者可調取項目同網頁新增方式。

使用者資料：中華電信網路、中華電信行動、台灣大哥大、遠傳電信股份有限公司、台灣之星
歷史查詢：大台中數位有線電視股份有限公司、亞太電信、台灣固網、安源通訊股份有限公司

name:
中華電信網路:HINET-NET
中華電信行動:EMOME-NET
台灣大哥大:TAIWANMOBILE-NET
遠傳電信股份有限公司:FETNET-NET
台灣之星:VIBO-NET
大台中數位有線電視股份有限公司:VEETIME-TW
亞太電信:APT
台灣固網:TFN-NET
安源通訊股份有限公司:????

'''
ips = []
times = []
ports = []

with open('ips.txt', newline='') as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)

  # 以迴圈輸出每一列
  for row in rows:

    l = len(row)

    if l == 3:
        #彙整IP
        ips.append(row[0])
        print(row[0])
        #彙整時間
        time = datetime.strptime(row[1], "%Y%m%d%H%M")
        times.append(time)
        #彙整port
        ports.append(row[2])
        
    elif l == 2:
        #彙整IP
        ips.append(row[0])
        print(row[0])
        #彙整時間
        time = datetime.strptime(row[1], "%Y%m%d%H%M")
        times.append(time)
        #彙整port
        ports.append('0')

    else:
        print("格式有誤")
        


pprint(ips)
pprint(times)
pprint(ports)

with open('ips_output.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    
    i = 0
    import datetime
    for ip in ips:

        isp, lookup = which_isp(ip)

        '''
        if isp == '遠傳電信股份有限公司':

            start_time = times[i] - datetime.timedelta(minutes=60)
            start_time_format = start_time.strftime('%Y%m%d%H%M%S')
            end_time = times[i]
            end_time_format = end_time.strftime('%Y%m%d%H%M%S')
        

        else:
        '''
        start_time = times[i] - datetime.timedelta(minutes=10)
        start_time_format = start_time.strftime('%Y%m%d%H%M%S')
        end_time = times[i] + datetime.timedelta(minutes=10)
        end_time_format = end_time.strftime('%Y%m%d%H%M%S')


        if ports[i] != '0':
            ip_port = ip + ":" + ports[i]
            writer.writerow(["IP", isp, ip_port, start_time_format, end_time_format, lookup])
            print(["IP", isp, ip_port, start_time_format, end_time_format, lookup])
            i = i + 1
        else:
            writer.writerow(["IP", isp, ip, start_time_format, end_time_format, lookup])
            print(["IP", isp, ip, start_time_format, end_time_format, lookup])
            i = i + 1


'''
results = IPWhois('219.87.61.8').lookup_rdap(asn_methods=['dns', 'whois', 'http'])
#results = target.lookup_whois()
#pprint(target)
pprint(results['network']['name'])

'''



'''
#取日期
print("抓取日期")
today = datetime.datetime.now()
time_start = today - datetime.timedelta(days=8)
time_end = today - datetime.timedelta(days=1)

time_start_format =  time_start.strftime('%Y%m%d%H%M%S')
time_end_format = time_end.strftime('%Y%m%d%H%M%S')
print(time_start_format)
print(time_end_format)




#從檔案抓網址
f_phones = open('phones.txt','r')
phones = []
for phone in f_phones.readlines():
    if re.findall(r"-", phone):
        phones.append(phone)
    else:
        phones.append("886"+ phone.split("\n")[0][1:])
f_phones.close
print(phones)



    


with open('phones_output.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)

    for phone in phones:
        if re.findall(r"-", phone):
            writer.writerow(["市內電話", "-", phone, time_start_format, time_end_format, "使用者資料"])
        else:
            writer.writerow(["行動電話", "-", phone, time_start_format, time_end_format, "使用者資料"])

'''
