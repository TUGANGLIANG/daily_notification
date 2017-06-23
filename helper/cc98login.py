TARGET = "cc98"
FILENAME ="../conf/"+TARGET+".py"
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '../conf'))
import importlib
import requests
import hashlib

def load():
    """
    return cookies from FILENAME(../conf/cc98.py)
    """
    if not os.path.exists(FILENAME):
        return []
    else:
        return getattr(importlib.import_module(TARGET),"cookies",[])

def save(cookies):
    """
    save cookies to FILENAME
    """
    open(FILENAME,"w").write("cookies={}".format(repr(cookies)))


def md5(src):
    return hashlib.md5(bytes(src,encoding='utf-8')).hexdigest()

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36","Referer":"http://www.cc98.org/index.asp","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

def get_login_cookie(*k):
    data="a=i&u={}&p={}&userhidden=2".format(*k)
    #print(data)
    x = requests.post("http://www.cc98.org/sign.asp",data=data,headers=HEADERS)
    header_cookie = x.headers["Set-Cookie"]
    aspsky = header_cookie.split("aspsky=")[1].split(";")[0]
    username = aspsky.split("username=")[1].split("&")[0]
    if username == "":
        return False
    else:
        return aspsky

def run():
    username = input("Username:")
    password = input("Password:")
    x=get_login_cookie(username,md5(password))
    cookies = load()
    if x:
        print("Login Success!")
        if x not in cookies:
            cookies.append(x)
            save(cookies)
            print("new cookies saved! len(cookies)=%d"%(len(cookies)))
        else:
            print("no need to write")
    else:
        print("Login failed!")

if __name__ == "__main__":
    run()
