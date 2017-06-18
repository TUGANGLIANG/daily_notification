# daily_notification

适合于 ZJUer 的日常通知，使用方糖气球的 [Server酱](http://sc.ftqq.com/) 作为通知服务, 结合定时任务可以实现每天自动 CC98 签到，寝室电费、校园卡消费推送等功能

## 如何使用

运行本项目需要自行配置一些 `conf` 文件，参见 [conf_example](conf_example/)

首先你需要在[Server酱](http://sc.ftqq.com/)上获取一个`SCKEY` ， 使用 Github 账号 Oauth 登录，绑定你的微信，将获取的 SCKEY 写入到`conf/sc.py`中

目前完成的模块： 

### [CC98 自动签到模块](cc98autocheckin_module.py)

将你的 CC98 Cookie 中 aspsky 的值作为 cookies 数组的一员，写入到 `conf/cc98.py` 后即可运行 `cc98autocheckin_module.py` 啦

预期效果: 签到后推送本次签到获得的 CC98 米和目前拥有的 CC98 米

![](nothing/cc98.png)

----

## 目录结构

base.py : DailyNotification_Base 父类，子类需要重载其 work 方法

notification.py: 调用 Server酱 进行信息推送

EasyLogin.py: 对 requests 和 BeautifulSoup 进一步封装的爬虫模块. 求个 Star [https://github.com/zjuchenyuan/EasyLogin](https://github.com/zjuchenyuan/EasyLogin)

cc98autocheckin_module.py: CC98 自动签到模块，可以直接运行，将对配置的所有账号进行签到
