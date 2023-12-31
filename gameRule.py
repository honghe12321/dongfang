import pygame,sys
import random
import math
from pygame.locals import *
from pygame.sprite import Group
import gF 
import Bullet
import DADcharacter
import Slave
import global_var
import Effect
import Item
import gameRule

# returnScoreFormat(string) takes a string and returns it in the 
# format of: a comma between every other 3 digits
# e.g.: 1003756 -> 1,003,756
# efficiency: O(n) with n is the string length
def returnScoreFormat(string):
    zeroNum=9-len(string)
    zeroString=''
    for i in range(0,zeroNum):
        zeroString+='0'
    scoreString=zeroString+string
    scoreFinal=''
    for i in range(0,3):
        scoreFinal+=scoreString[i*3:i*3+3]
        if i!=2:
            scoreFinal+=','
    return scoreFinal

# addLastingCancel(tx,ty,slaves,maxFrame,doBonus) takes the position tx, and ty
# creating a slave at the given position which cancels all the bullet gruadually
# from the centre in maxFrame. doBonus controls if the cancelled bullet will drop
# points
# effect: create a slave in the slave group
# efficency: O(1)
# requires: maxFrame>0, maxFrame is integer
def addLastingCancel(tx,ty,slaves,maxFrame,doBonus):
        new_slave=Slave.bulletCancelLasting()
        new_slave.initial(tx,ty,maxFrame,900,doBonus)
        slaves.add(new_slave)

# cancalAllBullet(bullets,items,effects,doBonus) immediately cancels all the bullet
# objects in bullets group.  doBonus controls if the cancelled bullet will drop points
# Efficency: O(n), n is the length of bullets group
def cancalAllBullet(bullets,items,effects,doBonus):
    for bullet in bullets:
        if bullet.cancalable and bullet.type!=15:
            new_effect=Effect.bulletVanish()
            exception=(5,7,10,11,12,13)
            if not bullet.type in exception:
                new_effect.initial(bullet.image,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==5:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==7:
                if bullet.color=='red':
                    new_effect.initial(bullet.red[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                else:
                    new_effect.initial(bullet.blue[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==10 or bullet.type==11 or bullet.type==12 or bullet.type==13:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)

            effects.add(new_effect)
            if doBonus:
                Bullet.createItem(bullet.tx,bullet.ty,items)
            bullet.kill()

# addStars(screen,stars) adds 3 stars in title screen
# effects: creates star objects in group stars
def addStars(screen,stars):
    new_star=gF.star_effect()
    new_star.initial(780,550)
    stars.add(new_star)

    new_star=gF.star_effect()
    new_star.initial(790,620)
    stars.add(new_star)

    new_star=gF.star_effect()
    new_star.initial(820,660)
    stars.add(new_star)

# missDetect(player,bullets,enemys,effects,miss_sound,items,slaves) detects if
# the player get hit by a bullet. If so, it will complete the death settlement
# and create a bullet cancelling object along with its effect
# effect: delete bullet objects from bullets
#         create slave objects in slaves
#         create effect objects in effects
def missDetect(player,bullets,enemys,effects,miss_sound,items,slaves):
    miss=pygame.sprite.spritecollideany(player,bullets)
    if miss!=None and player.immune!=1 and not player.unhitable:
        if player.deadStatu!=1:
            miss_sound.play()
            playerDeathEffect(player,effects)
        player.deadStatu=1
        player.bulletSurpress=60
        if miss.type!=15:
            new_effect=Effect.bulletVanish()
            exception=(5,7,10,11,12,13,14,15,16)
            if not miss.type in exception:
                new_effect.initial(miss.image,miss.rect.centerx,miss.rect.centery,miss.dx,miss.dy)
            elif miss.type==5:
                new_effect.initial(miss.tempImage,miss.rect.centerx,miss.rect.centery,miss.dx,miss.dy)
            elif miss.type==7:
                if miss.color=='red':
                    new_effect.initial(miss.red[0],miss.rect.centerx,miss.rect.centery,miss.dx,miss.dy)
                else:
                    new_effect.initial(miss.blue[0],miss.rect.centerx,miss.rect.centery,miss.dx,miss.dy)
            elif miss.type==10 or miss.type==11 or miss.type==12 or miss.type==13:
                new_effect.initial(miss.tempImage,miss.rect.centerx,miss.rect.centery,miss.dx,miss.dy)

            effects.add(new_effect)
            miss.kill()

    if player.deadStatu==1 and player.deadFrame<=0 and player.immune!=1:
        player.life-=1
        if player.__class__.__name__=="Marisa":
            player.power-=100
        elif player.__class__.__name__=="Reimu":
            player.power-=50
        player.immune=1
        player.deadFrame=10
        player.boom=3
        player.spellBonus=False

        x_sign=[-1,+1]
        y_sign=[-1,+1]
        width=60
        maxFrame=90
        new_effect=Effect.wave()
        new_effect.rainbow=True
        new_effect.initial([player.cx+width*1,player.cy],900,maxFrame,(160,160,160),10)
        effects.add(new_effect)
        new_effect=Effect.wave()
        new_effect.rainbow=True
        new_effect.initial([player.cx+width*-1,player.cy],900,maxFrame,(160,160,160),10)
        effects.add(new_effect)
        new_effect=Effect.wave()
        new_effect.rainbow=True
        new_effect.initial([player.cx,player.cy+width*1],900,maxFrame,(160,160,160),10)
        effects.add(new_effect)
        new_effect=Effect.wave()
        new_effect.rainbow=True
        new_effect.initial([player.cx,player.cy+width*-1],900,maxFrame,(160,160,160),10)
        effects.add(new_effect)
        addLastingCancel(player.cx+width*1,player.cy,slaves,90,False)
        addLastingCancel(player.cx+width*-1,player.cy,slaves,90,False)
        addLastingCancel(player.cx,player.cy+width*1,slaves,90,False)
        addLastingCancel(player.cx,player.cy+width*-1,slaves,90,False)
       
            
    if player.immune==1 and player.bulletSurpress>0:
        #gameRule.cancalAllBullet(bullets,items,effects,False)
        for enemy in enemys:
            enemy.health-=4
        player.bulletSurpress-=1

# playerDeathEffect(player,effects) create player death effect
# effect: add a player death effect to effects
# efficiency: O(1) 
def playerDeathEffect(player,effects):
    for i in range(0,20):
        new_effect=Effect.grazeEffect()
        new_effect.initial([player.cx,player.cy],6,25,(255,255,255),6,1,20,4,2)
        effects.add(new_effect)

# doBoom(player,booms,pressed_keys,slash_sound,items) justify if boom available to be
# released, and preventing multiple release of boom
# effect: add boom object to booms, retrive and modify global values
# efficiency: O(n), n is the length of group items
def doBoom(player,booms,pressed_keys,slash_sound,items):
    if pressed_keys[K_x] and player.boomStatu==0 and player.boom>0 and not global_var.get_value('pressingX'):
        player.boom-=1
        global_var.get_value('nep_sound').play(-1)
        global_var.set_value('boomStatu',1)
        player.deadStatu=0
        player.deadFrame=10
        if player.__class__.__name__=="Reimu":
            for i in range(0,6):
                new_boom=Bullet.reimuBoomOrb(i)
                new_boom.wAngle=60*i
                new_boom.tx=player.cx
                new_boom.ty=player.cy
                booms.add(new_boom)
        elif player.__class__.__name__=="Marisa":
            new_boom=Bullet.boomSquare()
            new_boom.tx=player.cx
            new_boom.ty=player.cy
            booms.add(new_boom)
        slash_sound.play()
        player.spellBonus=False
        player.unhitFrame=player.boomUnhitMax
        for item in items:
            if item.lastFrame>=5:
                item.followPlayer=1
                item.followSpeed=9 

# hitEnemy(enemys,playerGuns,booms,bullets,effects,frame,player,items,bosses,slaves)
# deal with hit of bullets by player, substract health accordingly from enemies
# effect: modify slaves, playerGuns, bullets, effects, items, enemies
# efficiency: O(mn), m is the length of emeny, n is the length of single_hit
def hitEnemy(enemys,playerGuns,booms,bullets,effects,frame,player,items,bosses,slaves):
    enemy_hit=pygame.sprite.groupcollide(enemys,playerGuns,0,0)
    bullet_hit=pygame.sprite.groupcollide(playerGuns,enemys,0,0)
    for enemy in enemy_hit:
        single_hit=pygame.sprite.spritecollide(enemy,bullet_hit,False)
        for bullet in single_hit:
            enemy.health-=bullet.hit
            for boss in bosses:
                if boss.cardNum==10:
                    boss.health-=0.5*bullet.hit
    
    

    for bullet in bullet_hit:
        if player.__class__.__name__=="Marisa":
            new_effect=Effect.fire_effect_player()
            new_effect.initial(bullet.rect.centerx,bullet.rect.centery,bullet.color)
            effects.add(new_effect)
        elif player.__class__.__name__=="Reimu":
            if bullet.__class__.__name__=="reimuMainSatsu":
                new_effect=Effect.fire_effect_reimu_main()
                new_effect.initial(bullet.tx,bullet.ty)
                effects.add(new_effect)
            elif bullet.__class__.__name__=="reimuTargetSatsu":
                new_effect=Effect.fire_effect_reimu_target()
                new_effect.initial(bullet.tx,bullet.ty)
                effects.add(new_effect)

        player.score+=50
        bullet.kill()


    boss_hit=pygame.sprite.groupcollide(bosses,playerGuns,0,0)
    bullet_hit=pygame.sprite.groupcollide(playerGuns,bosses,0,0)

    for boss in boss_hit:
        single_hit=pygame.sprite.spritecollide(boss,bullet_hit,False)
        for bullet in single_hit:
            boss.health-=bullet.hit
        if round(boss.health/boss.maxHealth,2)<=0.25:
            if not global_var.get_value('hitting'):
                global_var.get_value('hit_sound2').stop()
                global_var.get_value('hit_sound2').play()
                global_var.set_value('hitting',True)
        else:
            if not global_var.get_value('hitting'):
                global_var.get_value('hit_sound1').stop()
                global_var.get_value('hit_sound1').play()
                global_var.set_value('hitting',True)
    
    for bullet in bullet_hit:
        if player.__class__.__name__=="Marisa":
            new_effect=Effect.fire_effect_player()
            new_effect.initial(bullet.rect.centerx,bullet.rect.centery,bullet.color)
            effects.add(new_effect)
        elif player.__class__.__name__=="Reimu":
            if bullet.__class__.__name__=="reimuMainSatsu":
                new_effect=Effect.fire_effect_reimu_main()
                new_effect.initial(bullet.tx,bullet.ty)
                effects.add(new_effect)
            elif bullet.__class__.__name__=="reimuTargetSatsu":
                new_effect=Effect.fire_effect_reimu_target()
                new_effect.initial(bullet.tx,bullet.ty)
                effects.add(new_effect)
        player.score+=100
        bullet.kill()

    #detect boom-cancelled bullets
    bullet_cancel=pygame.sprite.groupcollide(bullets,booms,0,0)  
    for bullet in bullet_cancel:
        if bullet.cancalable and bullet.type!=15:
            new_effect=Effect.bulletVanish()
            exception=(5,7,10,11,12,13,15)
            if not bullet.type in exception:
                new_effect.initial(bullet.image,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==5:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==7:
                if bullet.color=='red':
                    new_effect.initial(bullet.red[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
                else:
                    new_effect.initial(bullet.blue[0],bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)
            elif bullet.type==10 or bullet.type==11 or bullet.type==12 or bullet.type==13:
                new_effect.initial(bullet.tempImage,bullet.rect.centerx,bullet.rect.centery,bullet.dx,bullet.dy)

            effects.add(new_effect)
            Bullet.createItem(bullet.tx,bullet.ty,items)
            bullet.kill()
    
    #detect boom-hit enemy
    enemy_boomed=pygame.sprite.groupcollide(enemys,booms,0,0)
    for enemy in enemy_boomed:
        enemy.health-=100
    
    if player.__class__.__name__=="Reimu":
        boom_collide=pygame.sprite.groupcollide(booms,enemys,0,0)
        for boom in boom_collide:
            if boom.collidable:
                single_boom=pygame.sprite.spritecollide(boom,enemys,False)
                for enemy in single_boom:
                    enemy.health-=boom.expDamage
                global_var.set_value('shakeFrame',20)
                global_var.get_value("reimuBoom_sound").stop()
                global_var.get_value("reimuBoom_sound").play()
                new_slave=Slave.bulletCancelLasting()
                new_slave.initial(boom.tx,boom.ty,5,300,True)
                slaves.add(new_slave)
                new_effect=Effect.bulletCreate(boom.colorNum)
                new_effect.initial(boom.tx,boom.ty,160,300,20)
                effects.add(new_effect)
                new_fire=Bullet.reimuBoomAoe()
                new_fire.initial(boom.tx,boom.ty)
                playerGuns.add(new_fire)
                boom.doKill()
    
    #detect boom-hit boss
    if player.__class__.__name__=="Reimu":
        boom_collide=pygame.sprite.groupcollide(booms,bosses,0,0)
        for boom in boom_collide:
            if boom.collidable:
                single_boom=pygame.sprite.spritecollide(boom,bosses,False)
                for boss in single_boom:
                    if (not boss.boomImmune) or (not boss.ifSpell):
                        boss.health-=boom.expDamage*0.5
                        global_var.set_value('shakeFrame',20)
                        global_var.get_value("reimuBoom_sound").stop()
                        global_var.get_value("reimuBoom_sound").play()
                        new_slave=Slave.bulletCancelLasting()
                        new_slave.initial(boom.tx,boom.ty,5,300,True)
                        slaves.add(new_slave)
                        new_effect=Effect.bulletCreate(boom.colorNum)
                        new_effect.initial(boom.tx,boom.ty,160,300,20)
                        effects.add(new_effect)
                        new_fire=Bullet.reimuBoomAoe()
                        new_fire.initial(boom.tx,boom.ty)
                        playerGuns.add(new_fire)
                        boom.doKill()

# drawPlayer(screen,player,frame)
# draw player on the screen, when player is unhitable draw every other 2 frames
# effect: modify screen
# efficiency: O(1)
def drawPlayer(screen,player,frame):
    if player.immune!=1 and not player.unhitable:
        player.draw(screen)
    else:
        if frame%4<2:
            player.draw(screen)

# displayUi(screen,player,myfont,frame) displays all ui shown during game process
# including scores, player life, spell, bonus, and graze
# will show scores in a continous increasing every frame when the score increases
# effect: modify screen
# efficiency: O(log n), n is the number of score
def displayUi(screen,player,myfont,frame):
    life=player.life
    spell=player.boom
    lifeImage=global_var.get_value('lifeSign')
    speelImage=global_var.get_value('spellSign')
    lifeText=global_var.get_value('lifeText')
    spellText=global_var.get_value('spellText')
    #grazeText=pygame.transform.scale(global_var.get_value('graze_text'),(64,16))
    grazeText=global_var.get_value('graze_text')
    #screen.blit(lifeText,(690,170))
    #screen.blit(spellText,(690,204))
    if life>=0:
        for i in range(0,life):
            screen.blit(lifeImage,(760+i*24,170))
    if spell>=0:
        for i in range(0,spell):
            screen.blit(speelImage,(760+i*24,204))
    powerText=global_var.get_value('powerText')
    #screen.blit(powerText,(690,244))
    if player.power%100!=0:
        if player.power%100<10:
            powerNum=myfont.render(str(player.powerLevel)+'.0'+str(player.power%100)+'/4.00', True, (255, 255, 255))
            powerShadow=myfont.render(str(player.powerLevel)+'.0'+str(player.power%100)+'/4.00', True, (23, 23, 23))
        else:
            powerNum=myfont.render(str(player.powerLevel)+'.'+str(player.power%100)+'/4.00', True, (255, 255, 255))
            powerShadow=myfont.render(str(player.powerLevel)+'.'+str(player.power%100)+'/4.00', True, (23, 23, 23))
    else:
        powerNum=myfont.render(str(player.powerLevel)+'.00'+'/4.00', True, (255, 255, 255))
        powerShadow=myfont.render(str(player.powerLevel)+'.00'+'/4.00', True, (23, 23, 23))
    screen.blit(powerShadow,(789+3,244+2))
    screen.blit(powerNum,(789,244))
    

    #score part
    scoreTemp=str(player.score)
    #scoreFinal=returnScoreFormat(scoreTemp)
    scoreShown=global_var.get_value('scoreShown')
    if frame%1==0:
        minimumScoreStep=1
        scoreSub=player.score-scoreShown
        if scoreSub<=1:
            scoreShown=player.score
        else:
            while minimumScoreStep<=scoreSub:
                minimumScoreStep=minimumScoreStep*10+1
            minimumScoreStep=round((minimumScoreStep-1)/10)
            scoreShown+=minimumScoreStep
    global_var.set_value('scoreShown',scoreShown)
    #print(scoreShown,scoreTemp)
    scoreFinal=returnScoreFormat(str(scoreShown))

    scoreText=myfont.render('         '+scoreFinal, True, (255, 255, 255))
    shadowText=myfont.render('         '+scoreFinal, True, (23, 23, 23))

    if global_var.get_value('levelSign')==0:
        highScore=global_var.get_value('highScore_0')
    elif global_var.get_value('levelSign')==1:
        highScore=global_var.get_value('highScore_1')
    
    '''if highScore<=player.score:
        if global_var.get_value('levelSign')==0:
            global_var.set_value('highScore_0',player.score)
        elif global_var.get_value('levelSign')==1:
            global_var.set_value('highScore_1',player.score)'''
    if player.score>highScore:
        highScoreText=myfont.render('         '+scoreFinal, True, (255, 255, 255))
        highShadowText=myfont.render('         '+scoreFinal, True, (23, 23, 23))
    else:
        highScoreText=myfont.render('         '+returnScoreFormat(str(highScore)), True, (255, 255, 255))
        highShadowText=myfont.render('         '+returnScoreFormat(str(highScore)), True, (23, 23, 23))

    screen.blit(highShadowText,(673+3+20,130+2-30))
    screen.blit(highScoreText,(673+20,130-30))
    screen.blit(shadowText,(673+3+20,130+2))
    screen.blit(scoreText,(673+20,130))

    grazeNumText=myfont.render(str(global_var.get_value('grazeNum')), True, (255, 255, 255))
    g_w=grazeNumText.get_width()
    #screen.blit(grazeText,(682,276))
    grazeNumShadow=myfont.render(str(global_var.get_value('grazeNum')), True, (23, 23, 23))
    screen.blit(grazeNumShadow,(888-g_w+3,276+2))
    screen.blit(grazeNumText,(888-g_w,276))
    
    screen.blit(global_var.get_value('textArea'),(663,105))
    
# itemAllGet(items,player,effects) sucks all items to player's position
# effect: modify item objects in items group
# efficiency: O(n), n is the length of items
def itemAllGet(items,player,effects):
    if player.ty<=player.itemGetLine:
        for item in items:
            if item.lastFrame>=30 and item.type!=7:
                item.followPlayer=1
                #item.followSpeed=9
                #if not global_var.get_value('item_getting'):
                 #   global_var.get_value('item_get').play()
                #new_effect=Effect.itemFade()
                #new_effect.initial(item.image,item.rect.centerx,item.rect.centery)
                #effects.add(new_effect)
                #item.kill()

# checkLife(player,screen) aborts game when life is below 0
# effect: retrive and modify global values
# efficiency: O(1)
def checkLife(player,screen):
    if player.life<0:
        global_var.set_value('ifGameOver',True)
        global_var.set_value('pause',True)
        global_var.get_value('pause_sound').stop()
        global_var.get_value('pause_sound').play()
        #global_var.set_value('bgmPauseFlag',pygame.mixer.music.get_pos())
        cPos=global_var.get_value('bgmContinuePos')
        if global_var.get_value('ifBoss'):
            cPos[1]+=pygame.mixer.music.get_pos()
            if global_var.get_value('levelSign')==0:
                length=277.23755102040815
            elif global_var.get_value('levelSign')==1:
                length=262.452
            while cPos[1]>=length*1000:
                cPos[1]-=length*1000
            global_var.set_value('bgmContinuePos',cPos)
        else:
            cPos[0]+=pygame.mixer.music.get_pos()
            if global_var.get_value('levelSign')==1:
                length=198.164
                while cPos[0]>=length*1000:
                    cPos[0]-=length*1000
            global_var.set_value('bgmContinuePos',cPos)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/playerScore.mp3')
        pygame.mixer.music.play(loops=-1)
        global_var.get_value('nep_sound').stop()
        new_image=pygame.Surface((960,720)).convert_alpha()
        new_image.fill((0,0,0))
        new_image.blit(screen,(0,0))
        new_image=pygame.transform.smoothscale(new_image,(480,360))
        new_image=pygame.transform.smoothscale(new_image,(960,720))
        global_var.set_value('pauseScreen',new_image)

# checkLife(player,screen) aborts game when stage ends
# effect: retrive and modify global values
# efficiency: O(1)
def checkPass(player,screen):
    if global_var.get_value('levelPassSign'):
        global_var.set_value('pause',True)
        global_var.get_value('pause_sound').stop()
        global_var.get_value('pause_sound').play()
        pygame.mixer.music.stop()
        pygame.mixer.music.load('resource/bgm/playerScore.mp3')
        pygame.mixer.music.play(loops=-1)
        global_var.get_value('nep_sound').stop()
        new_image=pygame.Surface((960,720)).convert_alpha()
        new_image.fill((0,0,0))
        new_image.blit(screen,(0,0))
        new_image=pygame.transform.smoothscale(new_image,(480,360))
        new_image=pygame.transform.smoothscale(new_image,(960,720))
        global_var.set_value('pauseScreen',new_image)
        global_var.set_value('pauseSelectNum',1)