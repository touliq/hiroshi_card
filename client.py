import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

import datetime
import binascii
import nfc
import sqlite3
#from Crypto.Random import get_random_bytes
#key = get_random_bytes(16)
#cipher = AES.new(key, AES.MODE_EAX)

#ライト
import RPi.GPIO as GPIO
PNO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)
#ソケット
import socket,json
import os
ip1 = 'IP'#サーバのip
port1 = 'port'


with open ('receiver.pem','rb') as f:
    public_pem = f.read()
    public_key = RSA.import_key(public_pem)
    print(public_key.export_key().decode('utf-8'))

def Logoutput(ER):
     FORMAT='%(asctime)-15s %(message)s'
     now=datetime.datetime.now()
     logging.basicConfig(filename='Logputfile.log',level=logging.DEBUG,format=FORMAT)
     logging.error(ER)

def Logtuuka(OK):
    FORMAT='%(asctime)-15s %(message)s'
    now=datetime.datetime.now()
    logging.basicConfig(filename='Logputfile.log',level=logging.DEBUG,format=FORMAT)
    logging.error(OK+'tuukashimashita')
def main2(number,name):
#無限ループ
    while True:
        try:
            print("aaa")
            server1 = (ip1, port1)
            socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           # socket2=socket1
            socket1.connect(server1)#サーバにつなげる
            print("setuzoku")
            #socket2.connect(server1)#サーバにつなげ 
            print("setuzoku2")
            break#ループ終了
        except Exception as e:#例外処理
            Logoutput('sa-banitunagarimasendeshita ERROR')
            print(e)
            os.system("nmcli device wifi connect Hotspot-ubuntu password saVLNDK1")#サーバのホットスポットに接続
            time.sleep(5)
    print(time)
    print(number)
    print(name)

    
    cipher1_rsa = PKCS1_OAEP.new(public_key)
    print("tukareta")
    number = cipher1_rsa.encrypt(number.encode())
   # print(number.encode())
    print(number)
    cipher2_rsa = PKCS1_OAEP.new(public_key)
    name = cipher2_rsa.encrypt(name.encode())
   # print(name.encode())

#データ送信
    socket1.send(number)
    print("1")
    socket1.send(name)
    socket1.close()

    print('クライアント側終了です')


# 学生証のサービスコード
service_code = 0x09CB

def sakujo(sakujomae):#不必要なデータを削除
    try:
        sakujogo1=sakujomae.replace('\\x','').replace(' 00','').replace(' ','').replace('bytearray(b','').replace(')','')
        sakujogo2=sakujogo1.strip("'")
        sakujogo3=sakujogo2[:-2]

    except Exception as e:

        Logoutput('toridashinishippaishimashita ERROR')

    return sakujogo3

def henkan(henkanmae):#16進数から文字列に変換
    try:
        bs=bytes.fromhex(henkanmae)
        henkango=bs.decode('sjis')
    except Exception as e:
        Logoutput('henkannishippaishimashita ERROR')
    return henkango

def jikan():#現在時刻を表示
    try:
     t=datetime.now()
     now=str(t)[:-7]
     #print(now)
    except Exception as e:
        Logoutput('genzaijikokunohyoujinishippaishimashita ERROR')
    return now

def on_connect_nfc(tag):# タグのIDなどを出力する
  if isinstance(tag, nfc.tag.tt3.Type3Tag):
      try:
         # sc = nfc.tag.tt3.ServiceCode(service_code >> 6 ,service_code & 0x3f)
          sc =[ nfc.tag.tt3.ServiceCode(0x09CB >> 6 ,0x09CB & 0x3f)]
       # now=jikan()#現在時刻を表示

          bc_id = [nfc.tag.tt3.BlockCode(0)]
          bc_name = [nfc.tag.tt3.BlockCode(1)]
          name = tag.read_without_encryption(sc,bc_name)
          id = tag.read_without_encryption(sc, bc_id)
          number=id.decode('utf-8')
          name1=name.decode('sjis')
          number=number[2:10]
          main2(number, name1)

      except Exception as e:
          Logoutput('Type3Tagshippaishimashita ERROR')
          print( "error: %s" % e)
  else:
      print ("error: tag isn't Type3Tag")

def main():
#無限ループ
    while True:
        try:
#No such device対策
            os.system("sudo -p: echo -n 1-1 > /sys/bus/usb/drivers/usb/unbind")#バス１のポート1を開放　USBポートにつながっているデバイス無効化
            os.system("sudo -p: echo -n 1-1 > /sys/bus/usb/drivers/usb/bind")#バス１のポート1を結ぶ　　USBポートにつながっているデバイス有効化
            time.sleep(5)#5秒待つ　　　5秒以内にnfcリーダをつなぎなおせば例外処理は、実行されない

#カードリーダ読み取り&サーバに送信
            clf = nfc.ContactlessFrontend('usb')#nfcリーダのポートをclf変数に代入
            clf.connect(rdwr={'on-connect': on_connect_nfc})#on_connect関数実行する　clfはnfcリーダを指す
            print(clf)
            GPIO.output(PNO,0)# GPIO.HIGH)  #消灯
            time.sleep(1)#1秒ごとに読み取り
            GPIO.output(PNO,1)# GPIO.LOW) # 点灯
            print("OK")
        except Exception as e:#例外処理　　No such　device対策
	    #エラーメッセージを送信する
            Logoutput('No such Device ERROR')
            server1 = (ip1, port1)
            socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket1.connect(server1)

	    #送る内容
            number="カードリーダー1"
            name="再起動中"
            print(type(number))
           #line2 = json.dumps({"b":number,"c":name})#jsonにしてline2に代入する
            socket1.send(number.encode())#メッセージを送信する
            socket1.send(name.encode())
            os.system("sudo reboot")#再起動する
os.system("sudo python3 wificon.py")
os.system("nmcli device wifi connect Hotspot-ubuntu password saVLNDK1") #サーバのホットスポットに接続する
#time.sleep(5)
if __name__ == "__main__":
    main()
