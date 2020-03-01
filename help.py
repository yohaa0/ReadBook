#-*-coding:utf8;-*-
#qpy:console
"""
将模块帮助文件打印到文档
"""

import os
import sys
import androidhelper
out = sys.stdout
sys.stdout = open("androidhelper.txt", "w")
 
help(androidhelper)
 
sys.stdout.close()
sys.stdout = out