"""
做着玩的，挺多瑕疵。。
"""
import pygame
from pygame.locals import *
import sys
import os
import random
from pygame.color import THECOLORS
import math
import json

img_path = os.path.split(os.path.realpath(__file__))[0]+'/img/'
music_path = os.path.split(os.path.realpath(__file__))[0]+'/music/'
sound_path = os.path.split(os.path.realpath(__file__))[0]+'/sound/'
level_path = os.path.split(os.path.realpath(__file__))[0]+'/level/'
hcr_img_jz = [img_path+'xrk/xrk1.png', img_path+'xrk/xrk2.png', img_path+'xrk/xrk3.png', img_path+'xrk/xrk4.png']
wd_img_jz = [img_path+'wd/wd1.png', img_path+'wd/wd2.png', img_path+'wd/wd3.png']

#窗口大小
width = 900
height = 600
#框框位置
kk_location = [0, 0]
#代价为位置
cz_location = [705, 15]
#格子70*70
qp_location = [240, 170]
#种子框位置
zzb_location = [125, 20]
#函数大军
def sound(filename):
    sound = pygame.mixer.Sound(sound_path+filename)
    sound.play()
def music(filename):
    # 播放音乐
    pygame.mixer.music.load(music_path+filename)
    pygame.mixer.music.play(-1, 0)#循环次数，从第n秒开始播放
    #pygame.mixer.music.stop()#停止播放
def 画面显示():
    画背景()
    画内饰()   #上栅栏，草地边缘属于内饰
    画棋盘物体()
    画外饰()   #下栅栏，房子，树属于外饰
    画操作界面()
    画种子包()
    文字显示()
    鼠标跟随()
    画阳光和硬币()
    pygame.display.flip()
def 加载关卡(filename):
    with open(level_path + filename, 'r', encoding='utf-8') as file:
        关卡 = json.load(file)
    global 关卡名称, 关卡模式, 大波数, 总波数, 背景, 棋盘, bgm, 外饰, 内饰
    关卡名称 = 关卡['关卡名称']
    关卡模式 = 关卡['模式']
    大波数 = 关卡['大波数']
    总波数 = 关卡['总波数']
    背景 = 关卡['背景']
    棋盘 = 关卡['棋盘']
    bgm = 关卡['bgm']
    外饰 = 关卡['外饰']
    内饰 = 关卡['内饰']
    if not 背景:
        背景 = 'bj.png'
    if not 棋盘:
        棋盘 = 'qp.png'
    if 外饰:
        外饰 = pygame.image.load(img_path + 'ws/' + 外饰)
    else:
        外饰 = pygame.image.load(img_path + 'ws/ws1.png')
    if 内饰:
        内饰 = pygame.image.load(img_path + 'ns/' + 内饰)
    else:
        内饰 = pygame.image.load(img_path + 'ns/ns1.png')
    if not bgm:
        bgm = 'Laura Shigihara - Grasswalk.mp3'
    i = 1
    global coming_js, dq, bo
    while True:
        if 关卡['波'].get('%d'%i):
            bo.append(关卡['波']['%d'%i])
        else:
            break
        i += 1
    print('关卡解析完成:')
    print('关卡名称:', 关卡名称, '\n关卡模式:', 关卡模式)
def 波解析(dict):
    global time, dq, in_bo, bo, 最后一波, 波数, 大波, botext, bot
    if time >= dict['出现时间']:
        in_bo = True
        time = -1
        i = 1
        波数 += 1
        if 波数 == 1:
            sound('a lot of.wav')
        if dict['大波']:
            sound('hugewave.wav')
            botext = bofont.render('一大波僵尸正在靠近', True, THECOLORS['red'])
            bot = 50
            大波 = True
        else:
            大波 = False
        if dict['最后一波']:
            最后一波 = True
        while True:
            if dict['僵尸'].get('%d'%i):
                coming_js.append(dict['僵尸']['%d'%i])
            else:
                dq = i - 1
                break
            i += 1
        bo.pop(0)
    elif time == -1:
        global jstime
        if jstime == 10 and 大波:
            if 波数 != 1:
                sound('siren.wav')
                sound('sukhbir.wav')
        # 当前僵尸死光了（或被死亡）
        if dq == 0:
            jstime = -1
            in_bo = False
def 刷新僵尸(dict):
    global jstime, coming_js
    if jstime >= dict['出现时间']:
        if dict['出现位置'] == 0:
            dict['出现位置'] = random.randint(1, 5)
        if dict['id'] == 1:
            #id 1 戴帽子僵尸
            js.append(hatjsClass(dict['出现位置'], dict['被死亡时间'], dict['帽子'], dict['帽子生命']))
        print(dict)
        return dict
def 扣血(s, hp):
    if s.type == 'pl':
        s.扣血(hp)
    elif s.type == 'zb':
        s.扣血(hp)
def 鼠标跟随():
    #铲子跟随
    if 铲子选中态:
        mx, my = pygame.mouse.get_pos()
        screen.blit(cz, [mx - 25, my - 45])
    else:
        screen.blit(cz, cz_location)
    #种子跟随
    if 种子选中态:
        mx, my = pygame.mouse.get_pos()
        screen.blit(zzb[选中种子-1].i, [mx - 25, my - 40])
def 文字显示():
    screen.blit(suntext, (15, 87))
    screen.blit(warmtext, (200, 500))
    screen.blit(botext, (250, 250))
    surface2 = screen.convert_alpha()
def 进入cd(n):
    zzb[n].oncd = zzb[n].cd
def 收集阳光():
    for s in sun_move:
        s.move(s.wei2)
def 画背景():
    global 背景, 棋盘
    #screen.fill(THECOLORS['white'])
    screen.blit(pygame.image.load(img_path + 'background/' + 背景), (0, 0))
    screen.blit(pygame.image.load(img_path + 'qp/' + 棋盘), qp_location)
def 画外饰():
    screen.blit(外饰, (0, 0))
def 画操作界面():
    screen.blit(kk, kk_location)  # 上方操作框
def 画内饰():
    screen.blit(内饰, (0, 0))
def 点击判断():
    x = event.pos[0]
    y = event.pos[1]
    if x >= cz_location[0] + 5 and x <= cz_location[0] + 75 and y >= cz_location[1] and y <= cz_location[1] + 75:
        #print('铲子')
        return ['铲子', 1]
    elif x >= qp_location[0] and x <= 70*9 + qp_location[0] and y >= qp_location[1] and y <= 70*5 + qp_location[1]:
        #print('选择格子:')
        #print((x - qp_location[0])//70 + 1, (y - qp_location[1])//70 + 1)
        return ['格子', [(x - qp_location[0])//70 + 1, (y - qp_location[1])//70 + 1]]
    elif x >= zzb_location[0] and x <= zzb_location[0] + 540 and y >= zzb_location[1] and y <= zzb_location[1] + 80:
        #print('选择种子:')
        #print((x - zzb_location[0])//60 + 1)
        global warmtext, wt
        if zzb[(x - zzb_location[0])//60].oncd:
            warmtext = warmfont.render('种子cd中', True, THECOLORS['orange'])
            wt = 30
            return ['种子cd中', (x - zzb_location[0])//60 + 1]
        elif zzb[(x - zzb_location[0])//60].cost > sum_sun:
            warmtext = warmfont.render('费用过高', True, THECOLORS['orange'])
            wt = 30
            return ['费用过高', (x - zzb_location[0])//60 + 1]
        return ['种子', (x - zzb_location[0])//60 + 1]
def 慢动画播放():
    #植物行为
    for xrk in qp:
        xrk.jz(xrk.pd(), xrk.wei)
    #阳光行为
    for s in sun:
        s.jz(s.wei)
    #拾取的阳光行为
    for s in sun_move:
        s.jz(s.wei)
def 快动作播放():
    global wt, warmtext, bot, botext
    #僵尸动,来自动画播放，为提高流畅性，移动至此处
    for j in js:
        j.jz(j.pd(), j.wei)
    #豌豆动
    for s in shoot:
        s.jz(s.pd(), s.wei)
    #攻击特效动
    for s in shoot_move:
        s.jz(s.wei)
    #肢体动
    for s in sz:
        s.jz(s.wei)
    #阳光下落
    for s in sun:
        if s.sunfrom == 'flower':
            s.down1(s.wei2)
        elif s.sunfrom == 'sun':
            s.down2(s.wei2)
    #警告标语显示与消失
    if wt > 0:
        wt -= 1
    else:
        warmtext = warmfont.render('', True, THECOLORS['orange'])
    if bot > 0:
        bot -= 1
    else:
        botext = bofont.render('', True, THECOLORS['orange'])
def 画种子包():
    global zzb
    for b in zzb:
        if b.oncd > 0:
            b.oncd -= 1
            apa = int((1 - b.oncd/b.cd) * 200)
            if b.oncd == 0:
                apa = 255
            pygame.draw.rect(screen, THECOLORS['gray'], [zzb_location[0] + b.wei * 60, zzb_location[1], 60, 82], 0)
            source = b.image
            temp = pygame.Surface((source.get_width(), source.get_height())).convert()
            temp.blit(source, (0, 0))
            temp.set_alpha(apa)
            screen.blit(temp, [zzb_location[0] + b.wei * 60, zzb_location[1]])
        else:
            screen.blit(b.image, [zzb_location[0] + b.wei * 60, zzb_location[1]])
def 画棋盘物体():
    #越后生成越上层
    h1 = []
    h2 = []
    h3 = []
    h4 = []
    h5 = []
    h = [h1, h2, h3, h4, h5]
    #放到h里的是有行层次的
    #棋盘上的植物
    for xrk in qp:
        if xrk != 0:
            h[xrk.hang - 1].append(xrk)
    #僵尸
    for j in js:
        if j != 0:
            h[j.hang - 1].append(j)
    #肢体
    for s in sz:
        if s != 0:
            h[s.hang - 1].append(s)
    #豌豆等攻击
    for s in shoot:
        if s != 0:
            h[s.hang - 1].append(s)
    #攻击特效
    for s in shoot_move:
        if s != 0:
            h[s.hang - 1].append(s)
    for i in h:
        for j in i:
            if j != 0:
                screen.blit(j.image, j.rect)
                if j.type == 'zb':
                    if j.imgin == 1:
                        screen.blit(j.hat_img, j.rect)
                    elif j.imgin == 4:
                        screen.blit(j.hat_img, [j.rect.left, j.rect.top + 1])
                    elif j.imgin == 5:
                        screen.blit(j.hat_img, [j.rect.left + 1, j.rect.top])
                    else:
                        screen.blit(j.hat_img, [j.rect.left, j.rect.top - 2])
def 画阳光和硬币():
    #场上的阳光
    for s in sun:
        if s != 0:
            screen.blit(s.image, s.rect)
    #拾取的阳光
    for s in sun_move:
        if s != 0:
            screen.blit(s.image, s.rect)
def click_sun():
    x = event.pos[0]
    y = event.pos[1]
    i = 0
    for s in sun:
        if x >= s.rect.left and x <= s.rect.left + 50 and y >= s.rect.top and y <= s.rect.top + 50:
            sun_move.append(sunmoveClass([s.rect.top, s.rect.left]))
            sun.remove(s)
            if random.randint(0, 1):
                sound('clicksun.wav')
            else:
                sound('clicksun2.wav')
            i += 1
    return i * 25
def 移动事件():
    global sum_sun
    add = click_sun()
    if add:
        sum_sun += add
def 右击事件():
    global djq, suntext, 铲子选中态, 种子选中态, 选中种子
    djq = 5
    if 铲子选中态:
        铲子选中态 = False
    if 种子选中态:
        种子选中态 = False
def 左击事件():
    #上层先判断
    global djq, suntext, 铲子选中态, 种子选中态, 选中种子, sum_sun
    djq = 5  # 5帧的点击延迟
    add = click_sun()   #以后改成捡硬币
    if add:
        sum_sun += add
    else:
        位置 = 点击判断()  # 如果没点到阳光（或硬币），返回点击了个啥
        if 位置:
            if 位置[0] == '铲子':
                if not 铲子选中态:
                    sound('shovel.wav')
                铲子选中态 = not 铲子选中态
                种子选中态 = False
                选中种子 = 0
            if 位置[0] == '种子':
                if not 种子选中态:
                    sound('seedlift.wav')
                种子选中态 = not 种子选中态
                铲子选中态 = False
                选中种子 = 位置[1]
            if 位置[0] == '格子':
                if 种子选中态:
                    apd(位置[1][0], 位置[1][1], 选中种子)
                if 铲子选中态:
                    rmv(位置[1][0], 位置[1][1])
                选中种子 = 0
                种子选中态 = False
                铲子选中态 = False
        else:
            #点到空白的地方
            if 铲子选中态:
                铲子选中态 = False
            if 种子选中态:
                种子选中态 = False
def 发光(y, x):
    sun.append(sunClass([qp_location[1] + y * 70 + 10 - 70, qp_location[0] + x * 70 + 10 - 70], 'flower'))
def 自然光(x, y):
    sun.append(sunClass([x, y], 'sun'))
def apd(x, y, 选中种子):
    global sum_sun
    global suntext
    if 选中种子:
        if gezi[x-1][y-1] == 0:
            zzb[选中种子-1].apd([x, y])#添加植物
            sum_sun = sum_sun - zzb[选中种子-1].cost
            suntext = myfont.render(str(sum_sun), True, THECOLORS['orange'])
            gezi[x-1][y-1] = 1
            进入cd(选中种子-1)
            if random.randint(0, 1):
                sound('plant.wav')
            else:
                sound('plant2.wav')
        else:
            print('已存在')
def rmv(x, y):
    if gezi[x-1][y-1] == 1:
        for xrk in qp:
            if xrk.hang == y and xrk.lie == x:
                qp.remove(xrk)
        gezi[x-1][y-1] = 0
        if random.randint(0, 1):
            sound('plant.wav')
        else:
            sound('plant2.wav')
    else:
        print('不存在')

#类
class zzb_jianguoClass(pygame.sprite.Sprite):
    def __init__(self, wei):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'zzb/jg.png').convert_alpha()
        self.wei = wei
        self.type = 'zzb'
        self.i = pygame.image.load(img_path+'jg/jg1.png')
        self.cd = 900 #30s
        self.oncd = 450 #开局一半cd
        self.cost = 50
    def apd(self, location):
        qp.append(jianguoClass(location))
class jianguoClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path + 'jg/jg1.png')
        self.rect = self.image.get_rect()
        self.hang = location[1]
        self.lie = location[0]
        self.rect.top = qp_location[1] + location[1] * 70 + 10 - 70
        self.rect.left = qp_location[0] + location[0] * 70 + 10 - 70
        self.wei = 0
        self.hp = 4000
        self.maxhp = 4000
        self.type = 'pl'
        self.pw = ""
    def jz(self, return_list, wei=0):
        if wei >= 4:
            wei = 0
        if wei < 4:
            if wei == 0:
                self.image = pygame.image.load(img_path + 'jg/' + self.pw + 'jg1.png')
            elif wei == 1:
                self.image = pygame.image.load(img_path + 'jg/' + self.pw + 'jg2.png')
            elif wei == 2:
                self.image = pygame.image.load(img_path + 'jg/' + self.pw + 'jg1.png')
            elif wei == 3:
                self.image = pygame.image.load(img_path + 'jg/' + self.pw + 'jg3.png')
            wei += 1
        self.wei = wei
    def 扣血(self, hp):
        self.hp -= hp
        if self.hp >= self.maxhp * 2/3:
            self.pw = ""
        elif self.hp >= self.maxhp / 3:
            self.pw = "pw1/"
        else:
            self.pw = "pw2/"
        if self.hp <= 0:
            sound('plantdied.wav')
            gezi[self.lie - 1][self.hang - 1] = 0
            qp.remove(self)
    def pd(self):
        pass
class zzb_PeaShooterClass(pygame.sprite.Sprite):
    def __init__(self, wei):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'zzb/wd.png').convert_alpha()
        self.wei = wei
        self.type = 'zzb'
        self.i = pygame.image.load(img_path+'wd/wd2.png')
        self.cd = 225 #7.5s
        self.oncd = 0
        self.cost = 100
    def apd(self, location):
        qp.append(PeaShooterClass(location))
class PeaShooterClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(wd_img_jz[1])
        self.rect = self.image.get_rect()
        self.hang = location[1]
        self.lie = location[0]
        self.rect.top = qp_location[1] + location[1] * 70 + 10 - 70 #70为格子宽,10为50*50植物图片大小补正
        self.rect.left = qp_location[0] + location[0] * 70 + 10 - 70
        self.wei = 4    #第一发时间减半
        self.hp = 300
        self.maxhp = 300
        #self.speed = 1.4  #1.4s/发
        self.type = 'pl'
    def jz(self, return_list, wei=0):
        if wei >= 8:
            if return_list[0]:
                shoot.append(PeaClass([self.lie, self.hang]))
                sound('throw%d.wav'%random.randint(1, 2))
            wei = 0
        if wei % 4 == 0:
            self.image = pygame.image.load(wd_img_jz[1])
        elif wei % 4 == 1:
            self.image = pygame.image.load(wd_img_jz[2])
        elif wei % 4 == 2:
            self.image = pygame.image.load(wd_img_jz[1])
        elif wei % 4 == 3:
            self.image = pygame.image.load(wd_img_jz[0])
        wei += 1
        self.wei = wei
    def pd(self):
        global js
        #遍历僵尸，寻找范围内的僵尸
        for j in js:
            #同行
            if self.hang == j.hang:
                #35为格子的一半，寻找豌豆中点右边的僵尸
                if self.rect.left + 35 - j.rect.left <= 20:
                    #返回True,和该僵尸
                    return [True, j]
        return [False, 0]
    def 扣血(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            sound('plantdied.wav')
            gezi[self.lie - 1][self.hang - 1] = 0
            qp.remove(self)
class PeaClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'shoot/ptwd1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.hang = location[1]
        self.lie = location[0]
        self.rect.top = qp_location[1] + location[1] * 70 + 10 - 70
        self.rect.left = qp_location[0] + location[0] * 70 + 10 - 70 + 15#体长补正
        self.speed = 10#速度
        self.wei = 0
        self.ad = 27 #普通僵尸hp:270
        self.type = 'ad'
    def jz(self, return_list, wei = 0):
        if wei < 100:
            if not return_list[0]:
                self.rect.left += self.speed
                wei += 1
            else:
                shoot_move.append(PeamoveClass(self))
                扣血(return_list[1], self.ad)
        else:
            shoot.remove(self)
        self.wei = wei
    def pd(self):
        global js
        collide_list = pygame.sprite.spritecollide(self, js, False)
        if collide_list:
            hang = self.hang
            for i in collide_list:
                if hang == i.hang:
                    if i:
                        #返回第一个碰撞的
                        shoot.remove(self)
                        return [True, i]
        return [False, 0]
class PeamoveClass(pygame.sprite.Sprite):
    def __init__(self, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path + 'shoot/ptwd2.png')
        self.rect = self.image.get_rect()
        self.rect.top = j.rect.top
        self.rect.left = j.rect.left + 10 #10为距离补正
        self.hang = j.hang
        self.wei = 0
        self.type = 'pt'
    def jz(self, wei = 0):
        if wei < 2:
            if wei == 1:
                self.image = pygame.image.load(img_path+'shoot/ptwd3.png')
        else:
            sound('splat%d.wav'%random.randint(1, 3))
            shoot_move.remove(self)
        wei += 1
        self.wei = wei
class zzb_SunFlowerClass(pygame.sprite.Sprite):
    def __init__(self, wei):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'zzb/xrk.png').convert_alpha()
        self.wei = wei
        self.i = pygame.image.load(img_path+'xrk/xrk2.png')
        self.cd = 225 #7.5s
        self.oncd = 0
        self.cost = 50
        self.type = 'zzb'
    def apd(self, location):
        qp.append(SunFlowerClass(location))
class SunFlowerClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(hcr_img_jz[1])
        self.rect = self.image.get_rect()
        self.hang = location[1]
        self.lie = location[0]
        self.rect.top = qp_location[1] + location[1] * 70 + 10 - 70
        self.rect.left = qp_location[0] + location[0] * 70 + 10 - 70
        self.wei = 90   #第一个阳光6s,后面24s一个(不计动作时间)
        self.hp = 300
        self.maxhp = 300
        self.type = 'pl'
    def jz(self, return_list, wei=0):
        if wei < 120:
            if wei % 4 == 0:
                self.image = pygame.image.load(hcr_img_jz[1])
            elif wei % 4 == 1:
                self.image = pygame.image.load(hcr_img_jz[2])
            elif wei % 4 == 2:
                self.image = pygame.image.load(hcr_img_jz[1])
            elif wei % 4 == 3:
                self.image = pygame.image.load(hcr_img_jz[0])
        else:
            if wei == 120:
                self.image = pygame.image.load(hcr_img_jz[3])
            if wei == 123:
                self.image = pygame.image.load(hcr_img_jz[1])
                发光(self.hang, self.lie)
            if wei == 125:
                wei = 0
        wei += 1
        self.wei = wei
    def 扣血(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            sound('plantdied.wav')
            gezi[self.lie - 1][self.hang - 1] = 0
            qp.remove(self)
    def pd(self):
        pass
class sunClass(pygame.sprite.Sprite):
    def __init__(self, location, sunfrom):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'yg/dyg1.png')
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = location
        self.type = 'wp'
        self.wei = 0
        self.sunfrom = sunfrom
        self.wei2 = 0
        self.wmax = 0
    def jz(self, wei=0):
        if wei < 75:
            if wei % 2 == 0:
                self.image = pygame.image.load(img_path+'yg/dyg1.png')
            elif wei % 2 == 1:
                self.image = pygame.image.load(img_path+'yg/dyg2.png')
        else:
            if wei == 75:
                sun.remove(self)
        wei += 1
        self.wei = wei
    def down1(self, wei2=0):
        if wei2 <= 10:
            self.rect.top -= 2
            self.rect.left += 1
        elif wei2 <= 30:
            self.rect.top += 1
        if wei2 <= 30:
            wei2 += 1
        self.wei2 = wei2
    def down2(self, wei2=0):
        if self.wmax == 0:
            self.wmax = random.randint(60, 160)
        if wei2 < self.wmax:
            self.rect.top += 3
        if wei2 <= self.wmax:
            wei2 += 1
        self.wei2 = wei2
class sunmoveClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'yg/dyg1.png')
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = location
        self.type = 'pt'
        #从当前位置到(20, 20)
        self.sx = int((location[0] - 20)/20)
        self.sy = int((location[1] - 20)/20)
        self.wei2 = 0
        self.wei = 0
    def move(self, wei2 = 0):
        global suntext
        if wei2 < 20:
            self.rect.top -= self.sx
            self.rect.left -= self.sy
        if wei2 == 20:
            sun_move.remove(self)
            suntext = myfont.render(str(sum_sun), True, THECOLORS['orange'])
        wei2 += 1
        self.wei2 = wei2
    def jz(self, wei = 0):
        if wei < 75:
            if wei % 2 == 0:
                self.image = pygame.image.load(img_path+'yg/dyg1.png')
            elif wei % 2 == 1:
                self.image = pygame.image.load(img_path+'yg/dyg2.png')
        else:
            if wei == 75 and self.wei2 == 0:
                sun.remove(self)
        wei += 1
        self.wei = wei
class hatjsClass(pygame.sprite.Sprite):
    def __init__(self, hang, killed, hat, maxhat):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path+'js/ptjs/ptjs1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.hang = hang
        self.weight = 70
        self.rect.top = qp_location[1] + hang * 70 - 70 - 45
        self.rect.left = width
        self.wei2 = 0
        self.wei = 0
        self.speed = 70/25  #5s/格
        self.hp = 270
        self.maxhp = 270
        self.type = 'zb'
        self.ad = 50
        self.killed = killed
        self.dead = False
        self.pw = 0 #破位0为完整，1为断手，2为断头
        self.hat = maxhat   #帽子当前血量
        self.maxhat = maxhat    #帽子总血量
        self.hat_path = img_path + 'js/hat/' + hat  #帽子图片的位置
        self.hat_img = pygame.image.load(img_path + 'js/hat/' + hat + '/1.png').convert_alpha()
        self.hw = 0
        self.imgin = 1
    def jz(self, return_list ,wei = 0):
        #每次动都减少被死亡时间，如果为0则名义上死亡
        if self.killed > 0:
            self.killed -= 1
        elif self.killed == 0:
            self.killed = -1
            #当前僵尸数减少
            global dq
            dq -= 1
            self.dead = True
        #如果有植物在前面
        if return_list[0]:
            if wei == 0:
                self.imgin = 4
                if self.pw:
                    self.image = pygame.image.load(img_path + 'js/ptjs/pw/ptjs4.png').convert_alpha()
                else:
                    self.image = pygame.image.load(img_path + 'js/ptjs/ptjs4.png').convert_alpha()
                扣血(return_list[1], self.ad)
                sound('chomp%d.wav' % random.randint(1, 3))
                # 断点
            elif wei == 18:
                self.imgin = 5
                if self.pw:
                    self.image = pygame.image.load(img_path + 'js/ptjs/pw/ptjs5.png').convert_alpha()
                else:
                    self.image = pygame.image.load(img_path + 'js/ptjs/ptjs5.png').convert_alpha()
                扣血(return_list[1], self.ad)
                sound('chomp%d.wav'%random.randint(1, 3))
            if wei > 36:
                wei = -1
        else:
            #1/121概率叫
            if not random.randint(0, 120 * 6):
                sound('groan%d.wav'%random.randint(1, 6))
            if wei <= 24:
                if wei == 6:
                    self.imgin = 1
                    if self.pw:
                        self.image = pygame.image.load(img_path+'js/ptjs/pw/ptjs1.png').convert_alpha()
                    else:
                        self.image = pygame.image.load(img_path + 'js/ptjs/ptjs1.png').convert_alpha()
                    self.rect.left -= self.speed
                elif wei == 12:
                    self.imgin = 2
                    if self.pw:
                        self.image = pygame.image.load(img_path+'js/ptjs/pw/ptjs2.png').convert_alpha()
                    else:
                        self.image = pygame.image.load(img_path + 'js/ptjs/ptjs2.png').convert_alpha()
                    self.rect.left -= self.speed
                elif wei == 18:
                    self.imgin = 1
                    if self.pw:
                        self.image = pygame.image.load(img_path+'js/ptjs/pw/ptjs1.png').convert_alpha()
                    else:
                        self.image = pygame.image.load(img_path + 'js/ptjs/ptjs1.png').convert_alpha()
                    self.rect.left -= self.speed
                elif wei == 24:
                    self.imgin = 3
                    if self.pw:
                        self.image = pygame.image.load(img_path+'js/ptjs/pw/ptjs3.png').convert_alpha()
                    else:
                        self.image = pygame.image.load(img_path + 'js/ptjs/ptjs3.png').convert_alpha()
                    self.rect.left -= self.speed
            else:
                wei = 0
        wei += 1
        self.wei = wei
    def 扣血(self, hp):
        if self.hat > 0:
            self.hat = self.hat - hp
            if self.hat <= 0:
                self.hp += self.hat
                self.hat_img = pygame.image.load(img_path + 'js/hat/no/1.png').convert_alpha()
                sz.append(hatClass(self))
            if self.hat >= self.maxhat * 2/3 and self.hw == 0:
                self.hat_img = pygame.image.load(self.hat_path + '/1.png').convert_alpha()
                self.hw += 1
            elif self.hat <= self.maxhat * 2/3 and self.hw == 1:
                self.hat_img = pygame.image.load(self.hat_path + '/2.png').convert_alpha()
                self.hw += 1
            elif self.hw == 2:
                self.hat_img = pygame.image.load(self.hat_path + '/3.png').convert_alpha()
                self.hw += 1
        else:
            self.hp -= hp
        if self.hp <= 135:
            if self.pw == 0:
                sz.append(handClass(self))
                self.pw = 1
        if self.hp <= 0:
            sz.append(bodyClass(self))
            sz.append(headClass(self))
            if not self.dead:
                global dq
                dq -= 1
            js.remove(self)
    def pd(self):
        global qp
        #遍历植物，寻找范围内的植物
        for xrk in qp:
            #同行
            if xrk.hang == self.hang:
                #35为格子的一半，允许15px误差
                if abs(xrk.rect.left + 35 - (self.rect.left + self.weight/2)) <= 15:
                    #返回True,和该植物
                    return [True, xrk]
        return [False, 0]
class handClass(pygame.sprite.Sprite):
    def __init__(self, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path + 'js/hand/hand1.png')
        self.type = 'sz'
        self.rect = j.rect
        self.hang = j.hang
        self.wei = 0
    def jz(self, wei = 0):
        if wei < 18:
            if wei == 0:
                sound('shoop.wav')
            if wei == 6:
                self.image = pygame.image.load(img_path+'js/hand/hand2.png')
            elif wei == 12:
                self.image = pygame.image.load(img_path + 'js/hand/hand3.png')
        else:
            sz.remove(self)
        wei += 1
        self.wei = wei
class headClass(pygame.sprite.Sprite):
    def __init__(self, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path + 'js/head/head1.png')
        self.type = 'sz'
        self.rect = j.rect
        self.hang = j.hang
        self.wei = 0
    def jz(self, wei = 0):
        if wei < 18:
            if wei == 0:
                sound('shoop.wav')
            if wei == 6:
                self.image = pygame.image.load(img_path+'js/head/head2.png')
            elif wei == 12:
                self.image = pygame.image.load(img_path + 'js/head/head3.png')
        else:
            sz.remove(self)
        wei += 1
        self.wei = wei
class bodyClass(pygame.sprite.Sprite):
    def __init__(self, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path + 'js/body/body1.png')
        self.type = 'sz'
        self.rect = j.rect
        self.hang = j.hang
        self.wei = 0
    def jz(self, wei = 0):
        if wei <= 37:
            if wei == 12:
                self.image = pygame.image.load(img_path + 'js/body/body2.png')
            elif wei == 22:
                self.image = pygame.image.load(img_path+'js/body/body3.png')
            elif wei == 32:
                self.image = pygame.image.load(img_path + 'js/body/body4.png')
                self.rect.left -= 20 #图片大小补正
                sound('falling%d.wav' % random.randint(1, 2))
        else:
            sz.remove(self)
        wei += 1
        self.wei = wei
class hatClass(pygame.sprite.Sprite):
    def __init__(self, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(j.hat_path + '/4.png')
        self.hat_path = j.hat_path
        self.type = 'sz'
        self.rect = j.rect
        self.hang = j.hang
        self.wei = 0
    def jz(self, wei = 0):
        if wei < 18:
            if wei == 0:
                sound('shoop.wav')
            if wei == 6:
                self.image = pygame.image.load(self.hat_path + '/5.png')
            elif wei == 12:
                self.image = pygame.image.load(self.hat_path + '/6.png')
        else:
            sz.remove(self)
        wei += 1
        self.wei = wei
#主程序
pygame.init()
#创建Clock的实例
clock = pygame.time.Clock()
#构建屏幕
screen = pygame.display.set_mode((width, height), 0, 32)

coming_js = []
dq = 0
bo = []
in_bo = False
总波数 = 0
大波数 = 0
关卡名称 = ''
关卡模式 = ''
背景 = ''
棋盘 = ''
bgm = ''
最后一波 = False
大波 = False
波数 = 0
加载关卡('1_1.json')

pygame.mixer.init()

#阳光
sum_sun = 50
sun = []
sun_move = []
#攻击
shoot = []
#攻击命中特效
shoot_move = []
#种子包
zzb = []
zzb.append(zzb_SunFlowerClass(0))
for i in range(1, 8):
    zzb.append(zzb_PeaShooterClass(i))
zzb.append(zzb_jianguoClass(8))



# 创建一个字体
myfont = pygame.font.Font(None, 40)
warmfont = pygame.font.Font('SC.otf', 60)
bofont = pygame.font.Font('SC.otf', 60)

suntext = myfont.render(str(sum_sun), True, THECOLORS['orange'])
warmtext = warmfont.render('', True, THECOLORS['gray'])
botext = bofont.render('', True, THECOLORS['red'])

kk = pygame.image.load(img_path + 'zzb/kk.png')
cz = pygame.image.load(img_path + 'zzb/cz.png')

random.seed()
music(bgm)
qp = []
#植物50*50，（不一定）
gezi = [[0 for i in range(5)] for i in range(9)] #5*9

js = []
sz = []#碎肢
#for i in range(5):
    #js.append(ptjsClass(i+1,0))

wt = 0  #标语存在时间
bot = 0 #波数提示存在时间
铲子选中态 = False
种子选中态 = False
w = 0 #自然光时间7.5s
djq = 0 #点击cd
time = 0    #波外进度0.2s+1，
jstime = 0  #波内进度0.2s+1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            # 接收到退出时间后退出程序
            exit()
            #检查帧速率
            frame_rate = clock.get_fps()
            print('frame rate =', frame_rate)
        #鼠标点击
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and djq == 0:
                左击事件()
            if event.button == 3 and djq == 0:
                右击事件()
        elif event.type == pygame.MOUSEMOTION:
            移动事件()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_1:
                #if 位置[0] == '铲子':
                if not 铲子选中态:
                    sound('shovel.wav')
                铲子选中态 = not 铲子选中态
                种子选中态 = False
                选中种子 = 0

    if w % 6 == 0:
        # 判定波是否达到
        if bo:
            波解析(bo[0])
        else:
            if jstime == 10 and 大波:
                if 最后一波:
                    sound('finalwave.wav')
                    botext = bofont.render('               最后一波      ', True, THECOLORS['red'])
                    bot = 50
                    sound('sukhbir.wav')
            # 当前僵尸死光了（或被死亡）
            if dq == 0:
                jstime = -1
                in_bo = False
                if 最后一波:
                    botext = bofont.render('        你赢了        ', True, THECOLORS['red'])
                    bot = 50
        # 把僵尸放出来！！！倒序删除法
        for i in range(len(coming_js) - 1, -1, -1):
            if 刷新僵尸(coming_js[i]):
                coming_js.pop(i)
        慢动画播放()
        if in_bo:
            jstime += 1
        else:
            time += 1
    快动作播放()

    #阳光收集移动
    收集阳光()

    w += 1
    if w == 225:#7.5s每个
        自然光(0, random.randint(150, 800))
        w = 0

    if djq > 0:
        djq -= 1

    画面显示()
    clock.tick(30)

pygame.quit()