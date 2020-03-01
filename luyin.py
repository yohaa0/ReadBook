import androidhelper
import time
import os.path
import datetime
import urllib.request
import json

err_msg=['PASS','语音被中断','录音出错','网络错误','你没说话','听不懂你说的','语法错误']

droid = androidhelper.Android()
droid.vibrate()
#droid.ttsSpeak("speak")
#droid.vibrate()
if not os.access('/mnt/sdcard/pyreminder',os.F_OK):
    os.mkdir('/mnt/sdcard/pyreminder')
now=datetime.datetime.now()
recname = now.strftime("%Y_%m_%d_%H%M%S")
path='/mnt/sdcard/pyreminder/' + recname + '.wav'
recordinglength=3

droid.recorderStartMicrophone(path)

droid.dialogCreateHorizontalProgress('', '请说话', 100)
droid.dialogShow()
for x in range(0, 99):
  time.sleep(recordinglength/50.0)
  droid.dialogSetCurrentProgress(x)
droid.dialogDismiss()

droid.makeToast(path)

droid.recorderStop()
"""
# to recognize the speech
url = 'http://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=zh-CN&maxresults=10'
audio = open(path,'rb').read()

# for AMR format
headers = {'Content-Type' : 'audio/amr; rate=8000'}

req = urllib.request.Request(url, audio, headers)
response = urllib.request.urlopen(req)

red=json.loads(response.read())

if red['status']==0:
	n=[]
	msg=''
	for x in red['hypotheses']: n.append(x['utterance'])
	for x in n: msg=msg+x+'\n'
	msg = msg.encode('UTF-8')
else:
	msg=err_msg[red['status']]
droid.dialogCreateAlert('语音识别', msg)
droid.dialogSetPositiveButtonText('确定')
droid.dialogShow()

#print red
"""