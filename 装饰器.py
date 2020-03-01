#-*-coding:utf8;-*-
#qpy:console
import os
import time
def outer(func):
    def inter():
       res=func() 
       return res+1
    return inter
    

def foo(): 
    return 2
f=outer(foo)
print(f())
#使用 @ 标识符将装饰器应用到函数
def outer2(func):
    def inter():
       res=func() 
       return res+2
    return inter
@outer2
def foo2(): 
    return 3
print(foo2())


#*args and **kwargs
def outer3(func):
    def inter(*args): 
        res=func(args[0])
        return res+3
    return inter
@outer3
def foo3(n): 
    return n
print(foo3(4))

#三层
def log(text):
    def decorator(func):
        def wraper(*args,**kw):
            print('begin call %s %s'%(text,func.__name__))
            return func(*args,**kw)
        print('end call %s %s'%(text,func.__name__))
        return wraper
    return decorator 
@log('hello')
def ac():
    pass 
ac()

#一个典型的例子
def log2(func):
    def wraper(*args,**kw):
        print('%s call %s'%(args[0],func.__name__))
        return func(*args,**kw)
    return wraper


@log2
def w(n):
    if n=='17:30':exit()
    elif n.split(':')[-1]=='30':
        os.system('termux-vibrate -d 3000')
        os.system("termux-toast '起来走走了'")
        time.sleep(1)
        return w(time.ctime()[11:16])
    else:
        time.sleep(1)
        return w(time.ctime()[11:16])
w(time.ctime())
