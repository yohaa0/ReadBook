#qpy:quiet
#-*-coding:utf8;-*-
"""
This is a sample project which use SL4A UI Framework,
There is another Sample project: https://github.com/qpython-android/qpy-calcount
"""
import qpy
import androidhelper
import urllib.request as ur
from qsl4ahelper.fullscreenwrapper2 import *
import sys
#输出错误和日志
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
   
sys.stdout = Logger(sys.path[0]+'readbook.log', sys.stdout)
sys.stderr = Logger(sys.path[0]+'readbook.log_file', sys.stderr)

droid = androidhelper.Android()

class MainScreen(Layout):
    def __init__(self):
        super(MainScreen,self).__init__(str("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#ff0E4200"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<ImageView
		android:id="@+id/logo"
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:layout_weight="10"
	/>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="horizontal"
		android:layout_weight="6">

		<TextView
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:textSize="10dp"
			android:text="帮你读书！"
			android:textColor="#fffaff00"
			android:layout_weight="1"
			android:gravity="center"
		/>
		 </LinearLayout>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="horizontal"
		android:layout_weight="50">
		
		<TextView
	 	android:id="@+id/text1"
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:textSize="8dp"
			android:textColor="#ffffffff"
			android:background="#ff05000f"
			android:layout_weight="60"
			android:gravity="left"
		/>
    </LinearLayout>

	<ListView
		android:id="@+id/data_list"
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:layout_weight="25"
		/>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="horizontal"
		android:layout_weight="8">
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="打开"
			android:id="@+id/but_load"
			android:textSize="8dp"
			android:background="#ffE0C832"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="退出"
			android:id="@+id/but_exit"
			android:textSize="8dp"
			android:background="#ff06AF00"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
	</LinearLayout>
</LinearLayout>
"""),"SL4AApp")

    def on_show(self):
        self.views.but_exit.add_event(click_EventHandler(self.views.but_exit, self.exit))
        self.views.but_load.add_event(click_EventHandler(self.views.but_load, self.load))
        pass

    def on_close(self):
        pass
        
    def select_file():
        file_list=[]#文档列表
        file_path=[]#文档路径
        for dirname,dirnames,filenames in os.walk('/storage/emulated/0/text'):
           for filename in filenames:
               if os.path.splitext(filename)[1].lower()=='.txt':
                  file_path.append(os.path.join(dirname,filename))
                  file_list.append(filename)
               #else:
               #   droid.makeToast('错误！没有文本文档，目前只支持文本文档')
                  
        print(file_path)
        droid.dialogCreateAlert('/storage/emulated/0/text')
        droid.dialogSetItems(file_list)
        droid.dialogSetPositiveButtonText('OK')        
        droid.dialogShow()
        #选择文档结果
        set_file=droid.dialogGetResponse().result
        print(file_list[set_file['item']])
        droid.ttsSpeak('您选的是'+file_list[set_file['item']][:-4])
        #获取文档_名字_及全路径
        file_name =file_path[set_file['item']] 
       # 打开文档
        file_read = open(file_name, mode="r", encoding="utf-8") 
     #一行一行读取文件内容到list 并去掉_行结束符
        make_list = [l.strip() for l in file_read.readlines()] 
       # 关闭文档
        file_read.close()
        return make_list
      
    def load(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("请选择UTF-8文本格式小说！")
        droid.ttsSpeak("请选择UTF-8文本格式小说！")
        saved_logo = qpy.tmp+"/qpy.logo"
        ur.urlretrieve("https://www.qpython.org/static/img_logo.png", saved_logo)
        self.views.logo.src = "file://"+saved_logo
        #获取要读的文本文档每一行list
           
        txt_list=[]
        txt_list=MainScreen.select_file()
        txt_list_len=len(txt_list)
        droid.ttsSpeak(('文章共有'+str(txt_list_len)+'行数, 从哪一段开始阅读?请输入行数字。'))
        get_message = droid.dialogGetInput('总共'+str(txt_list_len)+'行', '从哪一段开始阅读?').result 
        start_num=int(get_message)
        #print( start_num)
        droid.ttsSpeak(('还有'+str(txt_list_len-start_num)+'行数,阅读多少行数?请输入。'))
        get_message2 = droid.dialogGetInput('还有'+str(txt_list_len-start_num)+"行", '您需要阅读多少行?').result
        end_num=int(get_message2)
        time.sleep(1)
        read_num=0#结束计数
        if (start_num>txt_list_len):
           droid.makeToast('输入错误行数，请退出')
           droid.ttsSpeak('输入错误行数，请退出')
        else:
           for p in range(start_num,txt_list_len):
               #Rdtext="%s"%(line)
               #self.views.text1.text=""
               Rdtext=txt_list[p]
               read_num=read_num+1
               print(read_num,p,Rdtext)
               dayintxt=str(read_num)+"_"+str(p)+"_"+Rdtext
               self.views.text1.text=dayintxt
               #droid.makeToast(str(read_num)+str(p)+Rdtext)
               
         #droid.setTtsPitch(2)
               droid.ttsSpeak(Rdtext)
               time.sleep(5)
               if end_num<=read_num:#到设定次数停止
                     self.views.text1.text="已读完，请退出！"
                     droid.ttsSpeak(self.views.text1.text)
                     break
               else:
                     time.sleep(1)
         
        self.views.text1.text="已读完，请退出！"
        droid.ttsSpeak(self.views.text1.text)
            
    def exit(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Exit")
        FullScreenWrapper2App.close_layout()

if __name__ == '__main__':
    FullScreenWrapper2App.initialize(droid)
    FullScreenWrapper2App.show_layout(MainScreen())
    FullScreenWrapper2App.eventloop()