import pyshark
import time
import pyautogui
import os
from os import path

#簡單確認是否台灣IP位址 192拿掉了
def check_taiwan(ip):
    taiwan_simple_ips = ['111', '210', '36', '42', '134', '123', '180', '221', '218', '58', '1', '220', '59', '113', '116', '223', '110', '140', '125', '60',
                        '202', '114', '115', '120', '182', '122', '101', '106', '61', '117', '159', '150', '27', '222', '124', '163', '39', '219', '121', '168', '118', '112', '211', '119', '139', '175', '203', '49']
    if ip.split(".")[0] in taiwan_simple_ips:
        return True
    else:
        return False
    
#取得選取的Interface
def get_interface():
    interface_file_path = os.path.join(os.path.dirname(__file__), "interface_check","interface.txt")
    f = open(interface_file_path)
    interface_raw = f.readline()
    interface = interface_raw.split(" ")[1]
    return interface

#前置作業
#決定結果、截圖、封包檔名
date = time.strftime("%m%d")
filedate = time.strftime("%Y%m%d")
filetime = time.strftime("%H%M%S")
result_dir_path = os.path.join(os.path.dirname(__file__), "result", date)

if not path.exists(result_dir_path):
    os.mkdir(result_dir_path)

output_filename = "ips_" + filedate + "_" + filetime + ".txt"
output_filepath = os.path.join(os.path.dirname(__file__), "result", date, output_filename)
output_picname = "ips_" + filedate + "_" + filetime + ".png"
output_picpath = os.path.join(os.path.dirname(__file__), "result", date, output_picname)
output_pcapname = "packets_" + filedate + "_" + filetime + ".pcapng"
output_pcappath = os.path.join(os.path.dirname(__file__), "result", date, output_pcapname)
#變數初始化
i = 0

#開始擷取
interface = get_interface()
print(interface)
capture = pyshark.LiveCapture(interface=interface, bpf_filter='udp', output_file=output_pcappath)

with open(output_filepath, 'w') as f:

    for packet in capture.sniff_continuously():
        try:
            #如果是台灣IP才繼續
            if check_taiwan(str(packet["ip"].src)):

                if i < 30:
                    #print用格式
                    datenow = time.strftime("%Y/%m/%d")
                    timenow = time.strftime("%H:%M:%S")
                    #for 投單用格式
                    datenow_f = time.strftime("%Y%m%d")
                    timenow_f = time.strftime("%H%M")
                    timenow =datenow_f + timenow_f
                    
                    print(packet["ip"].src +":" + packet["udp"].srcport + " -> " + packet["ip"].dst + ":" + packet["udp"].dstport + "( " + datenow+" "+timenow + " )")
                    print(packet["ip"].src +"," + timenow + "," +packet["udp"].srcport, file =f )

                    i = i + 1
         
                    myScreenshot = pyautogui.screenshot()
                    myScreenshot.save(output_picpath)
                else:
                    time.sleep(2)
                    capture.close()
                    #超過30個封包就結束
                    break
                
        except:
            pass
