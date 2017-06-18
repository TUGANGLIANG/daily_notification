import os
import importlib
from notification import send
#import logging as _logging
#logging = _logging.getLogger(__name__)
#logging.setLevel(_logging.DEBUG)
class DailyNotification_Base():
    conf_name = None

    def __init__(self):
        """
        import conf file to self.conf
        """
        self.conf = self.conf_check()
        #print([i for i in dir(conf) if not i.startswith("_")])

    def work(self):
        """
        should return (should_send, title, message)
        """
        raise NotImplementedError
    
    def worktime(self):
        """
        should return the list of hour wanna to run the module, e.g. [22], or [7,23]
        """
        raise NotImplementedError
    
    def conf_check(self):
        if self.conf_name is None:
            #logging.warning("no conf")
            return None
        filename = "conf/{conf_name}.py".format(conf_name=self.conf_name)
        #logging.info("filename:"+filename)
        if os.path.exists(filename):
            return importlib.import_module("conf.{conf_name}".format(conf_name=self.conf_name))
        else:
            raise FileNotFoundError
    
    def run(self):
        should_send, title, message = self.work()
        if should_send:
            status = send(title,message)
            print(title,status)
    