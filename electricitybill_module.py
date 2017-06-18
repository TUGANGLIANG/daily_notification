from base import DailyNotification_Base
from EasyLogin import EasyLogin
import pickle
import time, datetime

__all__ = ["electricitybill"]

def now():
    return int(time.time())

def timestamp2str(timestamp=now()):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")

def storage_get(key=None):
    """
    以后应该改为读数据库，现在简单读文件
    
    规定格式：
    [timestamp, amount] #上次查询的时间戳，电表余额
    """
    try:
        raw = open("conf/electricity.pickle","rb").read()
    except:
        return [0, 0]
    return pickle.loads(raw)

def storage_set(data):
    open("conf/electricity.pickle","wb").write(pickle.dumps(data))

a = None
def login(username, password):
    global a
    assert isinstance(a, EasyLogin)
    x=a.post("http://service.chinasinew.com/zjuauth.ashx","authtype=zjuauth&uid={username}&upwd={password}&syscode=zjuserv".format(**locals())).json()
    login_code = x["code"]
    x=a.post("http://service.chinasinew.com/login.ashx",data="code={login_code}".format(**locals()))
    assert x.headers["location"]=="/main.aspx", "Login Failed"
    
DOMAIN = "http://service.chinasinew.com"
class electricitybill(DailyNotification_Base):
    conf_name = "zuinfo"
    def work(self):
        assert self.conf.xh and self.conf.password
        
        global a
        status_file = "conf/chinasinew_{}.stauts".format(self.conf.xh)
        a = EasyLogin.load(status_file)
        """
        Check Login Status, if login status is valid, no need for login
        """
        x = a.get(DOMAIN + "/home.aspx",o=True)
        if x.status_code != 200:
            login(self.conf.xh,self.conf.password)
            x = a.get(DOMAIN + "/home.aspx",o=True)
            assert x.status_code == 200
            a.save(status_file)
        
        getkey = lambda name:a.s.cookies["zjuservweb"].split(name + "=")[1].split("&",2)[0]
        xiaoqu = getkey("xq")
        sushelou = getkey("ssl")
        qinshihao = getkey("qsh")
        
        """
        Query Ammeter data
        """
        x = a.post(DOMAIN + "/zndbdata.ashx","datatype=getsyje&xq={xiaoqu}&ssl={sushelou}&qsh={qinshihao}".format(**locals()),result=False).json()
        assert x["errmsg"]=="", "Query Failure"
        amount_now = float(x["bzye"]) + float(x["yffye"]) # 补助余额，预付费余额
        
        time_last, amount_last = storage_get()
        time_now = now() # 现在的时间戳
        storage_set([time_now, amount_now])
        
        """
        Notification to User
        """
        
        amount_spent = "%.2f"%(amount_last - amount_now) # 消费了多少
        time_now_str = timestamp2str(time_now)
        time_last_str = timestamp2str(time_last)
        time_past = "%.3f Days"%((time_now - time_last) / 86400) # 上次查询过去了多少天
        guess = "%.1f"%((amount_last - amount_now)/((time_now - time_last) / 86400))
        
        title = "[电表] 使用{amount_spent}".format(**locals())
        content = "余额 {amount_now}元\n\n Now Time: {time_now_str}\n\n Last Time: {time_last_str}\n\n Past: {time_past}\n\n\n\n 预估每天 {guess}元".format(**locals())
        return True, title, content

if __name__ == "__main__":
    electricitybill().run()