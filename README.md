

# Tiaoji_Tellme

🏫研究生复试调剂,信息邮件提醒




作者 | River |
---------|----------|
 邮箱| laolei@forkway.cn |




<!-- ![20210307124009](https://cdn.jsdelivr.net/gh/Leizhenpeng/picbed@master/markdown/pictures/20210307124009.png) -->

## 如何运行

下载压缩包MAILME

1. 在user.config中,配置发送和接受邮件信息以及关键词参数

2. 在target.csv中,配置需要监控的学科名称,学校名称,以及网址

3. 双击运行MAILME.exe即可

4.可结合win定时任务反复执行




### 如何配置发送方参数

这里以QQ邮箱为例

USERMAIL:填写你的qq邮箱地址

SMTPPASSWORD: 设置-账户-开启POP3/SMTP服务-点击开启-获取密码

HOST:smtp.qq.com

### 如何配置收件方参数

TOMAILADDRESS:填写需要接受邮件的地址即可

### 如何配置关键词参数

SEARCH:默认为调剂,理论上可以更换其他需要监控的关键词

**注意 传入参数不能携带双引号**

### 如何配置定时任务

- 在windows中找到`任务计划程序`
- 参数部分:程序和脚本参照`python.exe`,添加参数填写`代码绝对路径`;起始于填写`python.exe所在环境`
- 在编写python代码的时候,不能使用相对路径

多使用下面的路径写法
```python
import os

home_path = os.path.dirname(os.path.abspath(__file__))
fileNamePath = f"{home_path}/data/crawlData/{fileName}.csv"
```

## 效果图

每次运行存在三种结果

* 找到新的调剂信息
* 暂无新的调剂信息
* 暂无调剂信息

其中只有在`找到新的调剂信息`时,才会对设定邮件进行提醒.

