import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF
import Bullet
import Slave
import global_var
import Effect
import Item

def polyByLength(bullets,type,length,sideNum,standardSpeed,standardAngle,pos,color='white',doCode=False,*args):
    halfAngle=360/sideNum/2
    counterAngle=90-halfAngle
    wholeAngle=halfAngle*2
    w=standardSpeed/math.sin(math.radians(counterAngle))
    sideLength=2*math.tan(halfAngle/180*math.pi)*standardSpeed
    for i in range(0,sideNum):
        for j in range(0,length):
            new_bullet=type(*args)
            #print(new_bullet)
            unitLength=sideLength/length
            dLength=j*unitLength
            dFromCenter=dLength-(sideLength/2)
            speed=math.sqrt(standardSpeed**2+dFromCenter**2)
            sinValue=math.sin(math.radians(counterAngle))*dLength/speed
            insideAngle=(math.asin(sinValue)/math.pi*180)
            if math.sqrt(w**2+speed**2)<dLength:
                insideAngle=180-insideAngle
            angle=standardAngle+wholeAngle*i+insideAngle
            new_bullet.initial(pos[0],pos[1],1)
            if not doCode:
                new_bullet.loadColor(color)
            else:
                new_bullet.doColorCode(color)
            new_bullet.setSpeed(angle,speed)
            bullets.add(new_bullet)
            #print(i,' ',j)

def ellipseByDeg(bullets,type,num,a,b,incline,speed,pos,color='white',doCode=False,*args):
    interval=360/num
    for i in range(num):
        theta=i*interval+incline  #in degree
        r=a*b/(math.sqrt(a**2*math.sin((theta+incline)*math.pi/180)**2+b**2*math.cos((theta+incline)*math.pi/180)**2))
        new_bullet=type(*args)
        nx=r*math.cos((theta)/180*math.pi)
        ny=r*math.sin((theta)/180*math.pi)
        new_bullet.initial(pos[0]+nx,pos[1]+ny,1)
        new_bullet.setSpeed(theta,speed*r/b)
        if not doCode:
            new_bullet.loadColor(color)
        else:
            new_bullet.doColorCode(color)
        bullets.add(new_bullet)




