import socket,pickle,json,requests,sqlite3
import subprocess
import datetime
import socket
import threading
import os
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time

h_gakuban=datetime.datetime.now()
h_time=datetime.datetime.now()

andip1 = 'IPAdress'
andport1 = 'port'
andip2 = 'IPAdress'
andport2 = 'port'

with open ('private.pem','rb') as f:
    private_pem = f.read()
    private_key = RSA.import_key(private_pem)
    print(private_key.export_key().decode('utf-8'))

def Logoutput(ER):
    FORMAT='%(asctime)-15s %(message)s'
    now=datetime.datetime.now()
    logging.basicConfig(filename='Logputfile.log',level=logging.DEBUG,format=FORMAT)
    logging.error(ER)

def Logtuuka(OK):
    
    FORMAT='%(asctime)-15s %(message)s'
    logging.basicConfig(filename='Logputfile.log',level=logging.DEBUG,format=FORMAT)
    logging.error(OK+'tuukashimashita')

def andronoti1(date):
    try:
        socketand1=(andip1,andport1)
        andsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        andsocket1.connect(socketand1)
        massage=date[0]+'   '+date[1]
        andsocket1.sendall(massage.encode("utf-8"))
        andsocket1.close()
    except Exception as e:
        Logoutput('andronoti1 Error')
        print(e)

def andronoti2(date):
    try:
        socketand2=(andip2,andport2)
        andsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        andsocket2.connect(socketand2)
        massage=date[0]+'   '+date[1]
        andsocket2.sendall(massage.encode("utf-8"))
        andsocket2.close()
    except Exception as e:
        Logoutput('andronoti2 Error')
        print(e)

def  tuti(date):
    if __name__=="__main__":
        thread_1=threading.Thread(target=andronoti1(date))
        thread_2=threading.Thread(target=andronoti2(date))

        thread_1.start()
        thread_2.start()
def database(data):
    try:
     t=datetime.datetime.today()
     line1=(str(t)[6:19])
     print(line1)
     date=[line1,data[0],data[1]]
     dbname='' 
     global h_gakuban
     global h_time
     print(abs((t-h_time).total_seconds()))
     timedata=abs((t-h_time).total_seconds())
     if data[0]!=h_gakuban or int(timedata)>=60:
         conn = sqlite3.connect(dbname)
         cur = conn.cursor()
         cur.execute("CREATE TABLE IF NOT EXISTS mytable(id integer primary key autoincrement ,column1 TEXT, column2 TEXT, column3 TEXT)")
         cur.execute('replace into mytable (column1, column2, column3) values(?,?,?)',date)
         h_gakuban = data[0]
         h_time=t
         cur.execute('SELECT * FROM tablename')
         conn.commit()
         conn.close()
         Logtuuka('databasetuuka')

    except Exception as e:
     Logoutput('database')
     print(e)
    
try:
    os.system("nmcli device wifi hotspot")
    host1 = 'IPAdress'
    port1 = 'port'
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.bind((host1, port1))
    socket1.listen(2)
    Logtuuka('netOK')
except Exception as e:
    Logoutput('netosetuzoku')
    os.system("sudo reboot")

print('クライアントからの入力待ち状態')

while True:
    try:
     # コネクションとアドレスを取得
        connection, address = socket1.accept()
        print("setuzoku")
     # クライアントからデータを受信
        number = connection.recv(4096)
        print("jyushinn")
        name = connection.recv(4096)
        decipher1_rsa = PKCS1_OAEP.new(private_key)
        number = decipher1_rsa.decrypt(number).decode("utf-8")
        decipher2_rsa = PKCS1_OAEP.new(private_key)
        name = decipher2_rsa.decrypt(name).decode("utf-8")
        print(number)
        print(name)
        t=datetime.datetime.today()
        chek='カードリーダー'
        date=[number,name]
        if(chek in str(number)):
            tuti(data)
        else:
            tuti(date)
            database(date)
            #break
    except Exception as e:
        Logoutput('sockettuushin Error')
        print(e)
connection.close()
socket1.close()
Logtuuka('sa-ba-tuuka')
print('サーバー側終了です')
