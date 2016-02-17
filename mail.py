#! /usr/bin/python2.6
# -*- coding: utf-8 -*-
import sys,os,re,smtplib,mimetypes,pycurl,json,urllib,StringIO,time,traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
leng=len(sys.argv)
#f.writelines(str(leng))
#f.writelines('\n')
#f.writelines(sys.argv[0]+'\n')
#if leng > 1 :
   # f.writelines('arg1 '+sys.argv[1]+'\n')
   # f.writelines('arg2 '+sys.argv[2]+'\n')
   # f.writelines('arg3 '+sys.argv[3]+'\n')
   # f.writelines('test1'+'\n')
   # f.writelines(type(sys.argv[3])
   # temp=sys.argv[3]
   # f.writelines(str(type(temp)))
   # f.writelines('test'+'\n')
#else:
   # f.writelines('no args'+'\n')


#if __name__ == "__main__":
   # autoSendMail()
def log4py(logpath,logtxt):
   f=open(logpath,'a')
   logtime=time.strftime('%Y%m%d%H%M%S',time.localtime())
   f.writelines(logtime+":")
   f.writelines(logtxt)
   f.writelines('\n')
   f.close()

def printmlinestr(mlinestr):
   d=mlinestr.splitlines()
   res=""
   for i in d:
      i="<br>"+i+"</br>"
      res+=i+'\n'
   return res

#getvalue 通过正则表达式获取对应itemID
def getvalue(string,rexp):
    r=re.compile(rexp,re.M)
    #r=re.compile("^ITEMID：[0-9]*",re.M)
    log4py(logpath,'method getvalue')
    log4py(logpath,'string')
    log4py(logpath,string)
    #for i in string:
    d=r.findall(string)
    log4py (logpath,'rexp:')
    log4py (logpath,rexp)
    str1=d[0]
    log4py(logpath, 'rexresult:')
    log4py(logpath,str1)
    print str1
   # arrstr=str.split("\xa3\xba")
    arrstr=str1.split(":")
    result=arrstr[1]
    log4py(logpath,'result:')
    log4py(logpath,result)
    log4py(logpath,'end method getvalue')
    return result


#getpic 获取报警图片，写入文件
def getpic(itemid):
        log4py(logpath,'method getpic')
   # try:
        c = pycurl.Curl()
        pathroot='/etc/zabbix/alert/'
        #path='c:/alert.png'
        #head='Content-Type:application/json'
        global stime
        endtime=time.strftime('%Y%m%d%H%M%S',time.localtime())
        tmptime=int(endtime)-10000
        stime = repr(tmptime)
        post_data_dic={"itemids":itemid,"period":"3600","stime":stime}
	picpath=(pathroot)+(stime)+(itemid)+'.png'
	print 'picpath:'+picpath
        str=file(picpath,'wb')
        c.setopt(pycurl.URL, "http://10.75.19.23/zabbix/chart.php")
        c.setopt(pycurl.WRITEFUNCTION, str.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        #c.setopt(pycurl.HEADER, True)
        c.setopt(c.POSTFIELDS,urllib.urlencode(post_data_dic))
        c.perform()
        log4py(logpath,'end method getpic')
	return picpath
   # except Exception,e:
   #     f.writelines('expforgetpic:\n')
   #     f.writelines(e)

def SendMail(receivers,subject,data,picpath,itemid):
    msg = MIMEMultipart()
    msg['From'] = "zbx@xxx.com"
    #msg['To'] = "zgyan@xxx.com"
    receives=receivers
    msg['To'] = receivers
    msg['Subject'] = subject
    body=printmlinestr(data)
    file1 = picpath
    image = MIMEImage(open(file1,'rb').read())
    image.add_header('Content-ID','<image1>')
    msg.attach(image)
    #print txt
    #print 'txt end'
    #print type (txt)
    url="http://10.75.19.23/zabbix/history.php?action=showgraph&itemid="+itemid+"&period=3600"+"&stime="+stime
    url2="http://10.75.19.23/zabbix/history.php?action=showgraph&itemid="+itemid+"&period=1209600"+"&stime="+stime
    #msg.attach(txt)
    html =  """
    <html>
      <body>
    """

    html+=body
    html+="<br><img src=cid:image1></br>"
    html+="<p><a href="+url+">URLLINK</a></p>"
    html+="<p><a href="+url2+">14DaysHistroyURLLINK</a></p>"
    html+="""
        </body>
    </html>
    """

    htm = MIMEText(html,'html','gb2312')
    msg.attach(htm)
    server = smtplib.SMTP()
    server.connect('mailhost.xxx.com')
    #server.login('htinns\qinlaw','~liuqing0530')
    #server.sendmail(msg['From'],msg['To'],msg.as_string())
    server.sendmail(msg['From'],receives,msg.as_string())
    server.quit()

#if __name__ == "__main__":



#def main
#获取zbx的传入参数 ，参数1-收件人地址，参数2-邮件主题，参数3-报警内容
global logpath
logpath='/etc/zabbix/alert/ts.log'
log4py(logpath,"--------------------------startx")
rece=sys.argv[1]
subject=sys.argv[2]
data=sys.argv[3]
#picpath='c:/alert.png'
#picpath='/etc/zabbix/alert/alert.png'
#\xa3\xba代表中文的冒号
#以后要加上异常处理，如果没有找到ID或者图片
#itemid=getvalue(data,"^ITEMID\xa3\xba[0-9]*")
#itemid=getvalue(data,"^ITEMID:[0-9]*)
#f.writelines(data)
try:
   itemid=getvalue(data,"ITEMID:[0-9]*")
   picpath= getpic(itemid)
   SendMail(rece,subject,data,picpath,itemid)
   os.remove(picpath)
   log4py(logpath,"argvs")
   log4py(logpath,sys.argv[0])
   log4py(logpath,sys.argv[1])
   log4py(logpath,sys.argv[2])
   log4py(logpath,sys.argv[3])
   log4py(logpath,sys.argv[4])
   log4py(logpath,sys.argv[5])
except Exception,e:
   log4py(logpath,e)
   os.system('echo zbxAlertErr|mail -s zbxPythonAlereScripErr itmon@xxx.com')
   #os.system('echo $3|mail -s $2 $1 ')
   shellcmd='echo '+data+'|mail -s '+subject+' '+rece
   print shellcmd
   os.system(shellcmd)
log4py(logpath,"--------------------------end")
