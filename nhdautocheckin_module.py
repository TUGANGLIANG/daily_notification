from base import DailyNotification_Base
from EasyLogin import EasyLogin

__all__ = ["nhdautocheckin"]

def checkin(cookie):
    """
    Checkin
    """
    a=EasyLogin(cookiestring=cookie)
    a.post("http://www.nexushd.org/signin.php",data="action=post&content=auto+reply...+%5Bem4%5D+")

def get_casino_speed(cookie):
    """
    return (casino speed, casino points)
    """
    a=EasyLogin(cookiestring=cookie)
    x = a.get("http://www.nexushd.org/mybonus.php", o=True, result=False)
    page = x.text
    casino_points = page.split("""[<a href="mybonus.php">Use</a>]:""")[1].split("<",2)[0].strip()
    casino_speed = page.split("You are currently getting ")[1].split(" ")[0]
    return casino_speed,casino_points

class nhdautocheckin(DailyNotification_Base):
    conf_name = "nhd"
    def work(self):
        if not self.conf.onlyget:
            checkin(self.conf.cookie)
        casino_speed,casino_points = get_casino_speed(self.conf.cookie)
        return True,"[NHD] {casino_points}".format(**locals()),"Speed: {casino_speed}".format(**locals())

if __name__ == "__main__":
    nhdautocheckin().run()