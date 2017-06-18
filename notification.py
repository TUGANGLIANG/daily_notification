import conf.sc as conf
assert conf.SCKEY # http://sc.ftqq.com/?c=code

import requests

session = requests.session()

def send(title, content=""):
    x = session.post("http://sc.ftqq.com/"+conf.SCKEY+".send",data={"text":title, "desp":content}).json()
    return x["errmsg"]=="success"