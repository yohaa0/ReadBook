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
import time
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
   
sys.stdout = Logger(sys.path[0]+'ceshi.log', sys.stdout)
sys.stderr = Logger(sys.path[0]+'ceshi.log_file', sys.stderr)

droid = androidhelper.Android()

class MainScreen(Layout):
    def __init__(self):
        super(MainScreen,self).__init__(str("""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#ff895544"
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
		android:layout_weight="70">
		

<ScrollView
    android:id="@+id/sv_show"
    android:fillViewport="true"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:id="@+id/text1"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:hint="Display text here"
        android:textSize="8dp"
        android:scrollbars="vertical"
        android:singleLine="false"
        android:textColor="#ffffffff"
        android:background="#ff895544"
/>
</ScrollView>
    </LinearLayout>
	<ListView
		android:id="@+id/data_list"
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:layout_weight="1"/>

	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="0px"
		android:orientation="horizontal"
		android:layout_weight="7">
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="Speech"
			android:id="@+id/but_load"
			android:textSize="8dp"
			android:background="#ffEFC802"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
			<View
			android:layout_width="2dip"
			android:layout_height="fill_parent"
			android:layout_gravity="center_horizontal"
			android:background="@android:color/gold"
			/>
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="Read"
			android:id="@+id/but_read"
			android:textSize="8dp"
			android:background="#ff06AF00"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
		<View
			android:layout_width="2dip"
			android:layout_height="fill_parent"
			android:layout_gravity="center_horizontal"
			android:background="@android:color/gold"
			/>			
		<Button
			android:layout_width="fill_parent"
			android:layout_height="fill_parent"
			android:text="Exit"
			android:id="@+id/but_exit"
			android:textSize="8dp"
			android:background="#ffEFC802"
			android:textColor="#ffffffff"
			android:layout_weight="1"
			android:gravity="center"/>
	</LinearLayout>
</LinearLayout>
"""),"SL4AApp")

    def on_show(self):
        self.views.but_exit.add_event(click_EventHandler(self.views.but_exit, self.exit))
        self.views.but_load.add_event(click_EventHandler(self.views.but_load, self.load))
        self.views.but_read.add_event(click_EventHandler(self.views.but_read, self.read))

        pass

    def on_close(self):
        pass
    def select_file():
        make_list=[]#文档列表
        with open(sys.path[0]+"语音测试.txt","r+", encoding="utf-8")as obj:
     #一行一行读取文件内容到list 并去掉_行结束符
             make_list = [l.strip() for l in obj.readlines()]
             print(make_list)
        return make_list
    def load(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Load")

        #saved_logo = qpy.tmp+"/qpy.logo"
        #ur.urlretrieve("https://www.qpython.org/static/img_logo.png", saved_logo)
        self.views.logo.src = "file:///storage/emulated/0/qpython/projects3/语音输入/yuyin.png"
        #droid.dialogCreateSeekBar(1,1000,"选择开始位置","fgfghghhhh")
        #droid.dialogSetPositiveButtonText('OK')  
        #droid.dialogShow()
        #time.sleep(5)
        #droid.dialogDismiss()
      
        droid.ttsSpeak("开始语音输入")
        time.sleep(2)
        while True:
              say=droid.recognizeSpeech(None,None,"测试")
              with open(sys.path[0]+"语音测试.txt","a+")as obj:
                   if say.result=="停止" or say.result=="退出" or say.result=="结束":
                      droid.ttsSpeak(say.result+"语音输入")
                      break
                   elif say.result=="清空所有输入" or say.result=="清除所有输入" :
                      obj.seek(0)
                      obj.truncate()
                      obj.write('语音输入，请继续…'+'\n')
                      break
                   elif say.result:
                      obj.write((say.result)+'\n')
                      
            
              #if say.result=="停止" or say.result=="退出" or say.result=="结束":
               #  droid.ttsSpeak(say.result+"语音输入")
              #   break
        make_list=MainScreen.select_file()
        print(make_list)
        dayintxt=',\n'.join(make_list)
        
        self.views.text1.text=dayintxt
    def read(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Read")
        make_list=MainScreen.select_file()
        print(make_list)
        
        for p in range(0,len(make_list)):
    #Rdtext="%s"%(line)
         Rdtext=make_list[p]
         
         droid.ttsSpeak(Rdtext)
        
    def exit(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Exit")
        FullScreenWrapper2App.close_layout()

if __name__ == '__main__':
    FullScreenWrapper2App.initialize(droid)
    FullScreenWrapper2App.show_layout(MainScreen())
    FullScreenWrapper2App.eventloop()
