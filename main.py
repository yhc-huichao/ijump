#!/usr/bin/env python
# coding=utf-8

import os
import image
import time
import cv2

def get_pic(num):
    cmd = 'adb shell screencap -p /sdcard/autojump/'+str(num)+'.png'
    os.system(cmd)
    print(cmd)
    time.sleep(1)
    os.system('adb pull /sdcard/autojump/'+str(num)+'.png D:\work\ijump')
    time.sleep(2)
    data = cv2.imread('D:\work\ijump\\'+str(num)+'.png')
    return data

def check_me(pic):
    return {'x':200,'y':700}

def check_next(pic_list):
    return {'x':500,'y':600}

def get_point(pic_list):
    me = check_me(pic_list[-1])
    to = check_next(pic_list)
    return [me,to]

def get_tuch_time(jump_data):
    me = jump_data['me']
    to = jump_data['to']
    lang = (to['x'] - me['x'])*2 + (to['y'] - me['y'])*2
    return lang

def my_tuch(x,y,time):
    os.system('adb shell input swipe %s %s %s %s %s' %(x,y,x,y,time))

def main():
    jump_data={}
    jump_data['sleep'] = 0
    jump_data['pic_list'] = []
    jump_data['me']={'x':0,'y':0}
    jump_data['to']={'x':0,'y':0}
    i = 0
    while True :
        now_pic = get_pic(i%5)
        jump_data['pic_list'].append(now_pic)
        point_tmp = get_point(jump_data['pic_list'])
        jump_data['me'] = point_tmp[0]
        jump_data['to'] = point_tmp[1]
        jump_data['time'] = get_tuch_time(jump_data)
        my_tuch(jump_data['me']['x'],jump_data['me']['y'],jump_data['time'])
        time.sleep(3)
        if i > 5:
            jump_data['pic_list'].reverse()
            jump_data['pic_list'].pop()
            jump_data['pic_list'].reverse()
            pass
        i += 1
        
    

if __name__ == '__main__':
    main()

