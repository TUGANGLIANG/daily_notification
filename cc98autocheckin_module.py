from base import DailyNotification_Base
from EasyLogin import EasyLogin

__all__ = ["cc98autocheckin"]

def checkin(cookie):
    a=EasyLogin(cookie={"aspsky":cookie})
    a.get("http://www.cc98.org/signin.asp",result=False)
    x=a.post("http://www.cc98.org/signin.asp?action=save",data="Expression=face7.gif&content=%E7%AD%BE%E5%88%B0%E7%AD%BE%E5%88%B0")
    if "/dispbbs.asp?boardid=326&id=4635712" in x.text:
        return True
    else:
        return False

def get_amount(cookie):
    a=EasyLogin(cookie={"aspsky":cookie})
    x=a.get("http://www.cc98.org/usermanager.asp",result=False)
    amount=x.split("用户财富： ")[1].split("<")[0]
    return int(amount)

class cc98autocheckin(DailyNotification_Base):
    conf_name = "cc98"
    def work(self):
        assert isinstance(self.conf.cookies,list) # "conf/cc98.py" should contain a list of cookie (only aspsky part) named cookies
        title = "[CC98] "
        content = ""
        for cookie in self.conf.cookies:
            username = cookie.split("username=")[1].split("&",2)[0]
            oldamount = get_amount(cookie)
            checkin_status = checkin(cookie)
            newamount = get_amount(cookie)
            gained = newamount-oldamount
            title += "{username}: {gained}, ".format(username=username,gained=gained)
            content += "{username}: {newamount}\n\n".format(username=username,newamount=newamount)
        return True, title, content

if __name__ == "__main__":
    cc98autocheckin().run()