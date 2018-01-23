#!/usr/bin/env python -W ignore
# coding=utf-8

import os
#import image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import subprocess

def cmd_shell():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
def get_pic(num):
    cmd = 'adb shell screencap -p /sdcard/autojump/'+str(num)+'.png'
    os.system(cmd)
    print(cmd)
    time.sleep(1)
    os.system('adb pull /sdcard/autojump/'+str(num)+'.png D:\work\ijump')
    time.sleep(2)
    data = cv2.imread('D:\work\ijump\\'+str(num)+'.png')
    return data


def get_line(img):
    #imgss= zeros_img(img)
    #show(imgss)
    lines = cv2.HoughLinesP(img,1,np.pi/180,90,minLineLength=30,maxLineGap=170)
    lines1 = lines[:,0,:]#提取为为二维
    line_end=[]
    '''
    ms=[]
    ns=[]
    nt=[]

    for x1,y1,x2,y2 in lines1[:]:
        flag = True
        m = x1 - ((x2-x1)*y1)/(y2-y1)
        n = y1 - ((y2-y1)*x1)/(x2-x1)
        if m in ms:
            for n_t in ns:
                if n_t -50 < n < n_t+50 :
                    flag = False
                    break
        else:
            ms.append(m)
        if flag :
            print(n)
            ns.append(n)
            line_end.append([m,n,0])
            cv2.line(imgss,(x1,y1),(x2,y2),(0,0,0),1)
            show(imgss,"line")
    '''
    k=0
    ks=[]
    bs=[]
    for x1,y1,x2,y2 in lines1[:]:
        k = (((y2-y1)/(x2-x1))//0.01 )*0.01
        b = y1 - k*x1
        flag = True
        if k in ks:
            for btmp in bs:
               if btmp - 50 <b<btmp +50 :
                   flag = False
                   break
        else:
            ks.append(k)
        if flag :
            bs.append(b)
            line_end.append([k,b])
            #cv2.line(imgss,(x1,y1),(x2,y2),(0,0,0),1)
            #show(imgss,"line")

    #print(line_end)
    return line_end
def get_line_point(lines):
    #lines=get_line(img)
    points=[]
    for l1 in lines :
        for l2 in lines:
            if l1[0] !=l2[0] and l1[1] != l2[1] :
                x = (l2[1]-l1[1])/(l1[0]-l2[0])
                y = x*l1[0]+l1[1]
                if x>2000 or y>2000 or x<0 or y<0 or math.isnan(x) or math.isnan(y):
                    pass
                else:
                    points.append([x, y])
    #print("交点",points)
    return points

def get_midpoint(points):
    midpoint=[]
    for a in points:
        for b in points:
            if 100 < abs(a[0]-b[0]) <500  :
                x=(a[0]+b[0])/2
                y=(a[1]+b[1])/2
                if not math.isnan(x):
                    midpoint.append([x,y])
    return midpoint



def get_circles(img):
    circles1 = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=23,minRadius=20,maxRadius=80)
    circles = circles1[0,:,:] #提取为二维
    mm=[]
    for i in circles[:]:
        mm.append([i[0],i[1],i[2]])

    return mm
def len_point(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def check_point_time(img1):
    #img1 = get_img(1)
    gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    thresh1 = cv2.adaptiveThreshold(gray1, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 3)
    cir1 = get_circles(thresh1)
    line1 = get_line(thresh1)
    line1_point = get_line_point(line1)
    midpoint=get_midpoint(line1_point)
    #print("line1:\n",cir1,"\n")
    my_tuch()
    time.sleep(3)

    img2 = get_pic("tmp")
    gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    thresh2 = cv2.adaptiveThreshold(gray2, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 3)
    cir2 = get_circles(thresh2)
    line2 = get_line(thresh2)
    print("line2:\n",line2,"\n")
    for m in line1 :
        print(m)
        cv2.line(img2,(int(m[0]+1),int(m[1]+1)),(int(m[0]-1),int(m[1]-1)),(0,255,0),3)


    cir = cir1[:]
    cir.extend(cir2)
    line_for=[]
    for m in cir:
        if (m in cir1) and (m in cir2) :
            pass
        else:
            line_for.append([m[0],m[1]])
            i=m
            cv2.circle(img2,(i[0],i[1]),i[2],(255,0,0),5)#画圆
            #cv2.circle(img1,(i[0],i[1]),1,(250,0,0),3)#画圆心
            #print(m)
            #show(img1)
    x1 = line_for[0][0]
    y1 = line_for[0][1]
    x2 = line_for[1][0]
    y2 = line_for[1][1]
    k = (((y2-y1)/(x2-x1))//0.01 )*0.01
    b = y1 - k*x1 + 160
    #print(k,b)

    ok={}
    for i in midpoint :
        md = ((i[0]*k+b-i[1])**2)/(k**2 + 1)
        if md < 30 :
            len_d = len_point(i,[x1,y1+160])//0.1*0.1
            ok[len_d]=i
    #print(ok)
    ok_tmp = sorted(ok.keys(),reverse=True)
    #time = ok_tmp[1]/len_point(line_for[0],line_for[1])
    #print(math.sqrt(time))
    m=ok[ok_tmp[1]]
    cv2.line(img2,(int(m[0]),int(m[1])),(int(m[0])+1,int(m[1])+1),(0,0,255),5)
    show(img2)



    return {"me":{"x":x2,"y":y2+160}, "to":{"x":m[0],"y":m[1]}}
def show(img,name = "tmp"):
    img  = rotate(img,90)
    cv2.imshow(str(name),img)
    cv2.waitKey (10)
    cv2.destroyWindow(str(name))


def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]

    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)

    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # 返回旋转后的图像
    return rotated


'''
def check_me(pic):
    return {'x':200,'y':700}

def check_next(pic_list):
    return {'x':500,'y':600}

def get_point(pic_list):
    me = check_me(pic_list[-1])
    to = check_next(pic_list)
    return [me,to]
'''

def get_tuch_time(jump_data):
    me = jump_data['me']
    to = jump_data['to']
    lang = (to['x'] - me['x'])*2 + (to['y'] - me['y'])*2
    print(lang)
    return lang

def my_tuch(x=550,y=1600,time=1):
    x=int(x)
    y=int(y)
    time = int(time)
    os.system('adb shell input swipe %s %s %s %s %s' %(x,y,x,y,time))

def main():
    jump_data={}
    jump_data['sleep'] = 0
    jump_data['pic_list'] = []
    jump_data['me']={'x':0,'y':0}
    jump_data['to']={'x':0,'y':0}
    i = 0
    cv2.namedWindow("Image")
    while True :
        now_pic = get_pic(i)
        data=check_point_time(now_pic)
        #jump_data['pic_list'].append(now_pic)
        #point_tmp = get_point(jump_data['pic_list'])
        jump_data['me'] = data['me']
        jump_data['to'] = data['to']
        jump_data['time'] = get_tuch_time(jump_data)
        my_tuch(jump_data['me']['x'],jump_data['me']['y'],jump_data['time'])
        time.sleep(3)
        if i > 5:
            i=-1
            jump_data['pic_list'].reverse()
            jump_data['pic_list'].pop()
            jump_data['pic_list'].reverse()
            pass
        i += 1
    


if __name__ == '__main__':
    #get_pic(11)
    #my_tuch(500,500,1)
    #time.sleep(1)
    #get_pic(12)
    main()

