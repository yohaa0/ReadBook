#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import androidhelper
import time
import os
import sys

print(os.getcwd())
print(sys.path[0])
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
   
sys.stdout = Logger('a.log', sys.stdout)
sys.stderr = Logger('a.log_file', sys.stderr)

droid = androidhelper.Android()
def select_file():
    file_path=[]
    file_list=[]
    for dirname,dirnames,filenames in os.walk('/storage/emulated/0/text'):
      for filename in filenames:
          if os.path.splitext(filename)[1].lower()=='.txt':
             file_path.append(os.path.join(dirname,filename))
             file_list.append(filename)
          elif len(filename)<0:
             droid.makeToast('错误！没有文本文档，目前只支持文本文档')
             
    print(file_path)
    print(file_list)
    droid.dialogCreateAlert('/storage/emulated/0/text')
    droid.dialogSetItems(file_list)
    droid.dialogShow()
    select_file=droid.dialogGetResponse().result
    print(file_list[select_file['item']])
#time.sleep(20)
# 写文件三部曲：创建对象-->操作对象-->关闭对象）
#file_name = "/storage/emulated/0/text/ceshi.txt" 
# （1）创建读文件对象 
    file_name = file_path[select_file['item']]
    return file_name
file_name=select_file()
print(file_name)
file_read = open(file_name, mode="r", encoding="utf-8") 
# （2）一行一行读取文件内容 
#txtlist=txtlist.decode("GBK")
#while True: 	
#txtlist = file_read.readlines() # 去行结束符
txtlist = [l.strip() for l in file_read.readlines()] # 去行结束符
   # 读取一行内容    
txtlistlen=len(txtlist)

#droid.dialogDismiss()

print(txtlistlen)
#关闭文件对象
file_read.close()
message = droid.dialogGetInput('总共'+str(txtlistlen)+'行', '从哪一段开始阅读?').result
starnum=int(message)

message2 = droid.dialogGetInput('还有'+str(txtlistlen-starnum)+"行", '您需要阅读多少行?').result
endnum=int(message2)

readnum=0#结束计数
if starnum>txtlistlen:
   droid.makeToast('输入错误段数，请重新输入')
   
else:
   for p in range(starnum,txtlistlen):
    #Rdtext="%s"%(line)
      Rdtext=txtlist[p]
      readnum=readnum+1
      print(readnum,p,Rdtext)
      dayintxt=str(readnum)+str(p)+Rdtext
      print(dayintxt)
      #print(type(dayintxt))
      droid.makeToast(str(readnum)+str(p)+Rdtext)
      if not Rdtext: 
         break
      else:
         #droid.setTtsPitch(2)
         droid.ttsSpeak(Rdtext)
         time.sleep(1)
         if endnum<=readnum:#到设定次数停止
            break
         else:
             time.sleep(5)
# （3）关闭读文件对象
