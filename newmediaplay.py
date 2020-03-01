#-*-coding:utf8;-*-
#qpy:console

import qpy
import androidhelper
import time

droid = androidhelper.Android()

print(droid.mediaPlay("/storage/emulated/0/qpython/gongxi.mp3","test",True).result)
time.sleep(10)
print(droid.mediaPlayList().result)
print(droid.mediaPlayInfo("test").result)
droid.mediaPlayClose("test")