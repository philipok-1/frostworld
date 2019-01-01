# Frostworld

import itertools, sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *

status="introscreen"
level=0
leveltarget=30

def calc_velocity(direction, vel=1.0):
    velocity = Point(0,0)
    if direction == 0: #north
        velocity.y = -vel
    elif direction == 2: #east
        velocity.x = vel
    elif direction == 4: #south
        velocity.y = vel
    elif direction == 6: #west
        velocity.x = -vel
    return velocity

def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2

def wall_collide(mover, wall_group):
        
        collidelist=pygame.sprite.spritecollideany(mover, wall_group)

        if collidelist!=None:
            
            if mover.rect.bottom>=collidelist.rect.top and mover.direction==4:
                mover.rect.bottom=collidelist.rect.top-1
            elif mover.rect.top<=collidelist.rect.bottom and mover.direction==0:
                mover.rect.top=collidelist.rect.bottom+1
            elif mover.rect.right>=collidelist.rect.left and mover.direction==2:
                mover.rect.right=collidelist.rect.left
            elif mover.rect.left<=collidelist.rect.right and mover.direction==6:
                mover.rect.left=collidelist.rect.right

            reverse_direction(mover)
            
        return mover.rect

def get_player_direction(player, z):

    original_direction=z.direction
    if z.X>player.X+5:
        return 6
    elif z.X<player.X-5:
        return 2

    elif z.X in range (player.X-3, player.X+3):
        if z.Y>player.Y:
            return 0
        elif z.Y<player.Y:
            return 4
        else:
            return original_direction
    else:
        return original_direction

width=1000
height=700
boundwidth=width-50
boundheight=height-100

def place_and_avoid(sprite, avoid_group, avoid_group2):

    position_good=False
          
    while position_good==False:
        
        sprite.position = random.randint(0,boundwidth), random.randint(0,boundheight)
        
        collidelist=pygame.sprite.spritecollideany(sprite, avoid_group)
        if collidelist!=None:
            if pygame.sprite.collide_rect_ratio(3) (sprite, collidelist):
                position_good=False
        collidelist=pygame.sprite.spritecollideany(sprite, avoid_group2)
        if collidelist!=None:
            if pygame.sprite.collide_rect_ratio(15) (sprite, collidelist):
                position_good=False
        else: position_good=True
    
   
    

#main program begins
pygame.init()
width=1000
height=700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision Demo")
font = pygame.font.Font(None, 36)
font2=pygame.font.SysFont("System", 30)
timer = pygame.time.Clock()
bg2= pygame.image.load("gameover.png").convert_alpha()
bg = pygame.image.load("introbackground.png").convert_alpha()
bg0=pygame.image.load("icebackground.png").convert_alpha()
bg3=pygame.image.load("levelup.png").convert_alpha()

pygame.mixer.init()
pickup=pygame.mixer.Sound("pickup.wav")
healthsound=pygame.mixer.Sound("health.wav")
teleport=pygame.mixer.Sound("teleport.wav")
hit=pygame.mixer.Sound("hit.wav")
scoresound=pygame.mixer.Sound("score.wav")
levelupsound=pygame.mixer.Sound("levelup.wav")
alloysound=pygame.mixer.Sound("alloysound.wav")

while True:

    while status=="introscreen":

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: sys.exit()
       
        elif keys[K_SPACE]:
            status="setup"

        score=0
        player_health = 100
        screen.blit(bg, (0,0))

        pygame.display.update() 
    
    while status=="setup":

        

        #create sprite groups
        player_group = pygame.sprite.Group()
        skeleton_group=pygame.sprite.Group()
        wall_group=pygame.sprite.Group()
        shield_group=pygame.sprite.Group()
        jewel_group=pygame.sprite.Group()
        health_group=pygame.sprite.Group()
        alloy_group=pygame.sprite.Group()
        nullgroup=pygame.sprite.Group()
             

        ticks = pygame.time.get_ticks()

        timenow=Timer(ticks)

        #create the player sprite
        player = MySprite()
        player.load("frostplayer.png", 32, 32, 3)
        player.position = 0, 50
        player.direction = 4
        player_group.add(player)

      
        #create walls

        for n in range (0,3):
            

            wall=MySprite()
            wall.load("icewall.png", 200,44,1)
            wall.position=random.randint(0,boundwidth), random.randint(0,boundheight-100)
            if not pygame.sprite.collide_rect(player, wall):   wall_group.add(wall)
            wall=MySprite()
            wall.load("icewallvert.png", 44,200,1)
            wall.position=random.randint(0,boundwidth), random.randint(0,boundheight-200)
            if not pygame.sprite.collide_rect(player, wall):   wall_group.add(wall)


        #place power-ups

        shieldicon=MySprite()
        shieldicon.load("shieldicon.png", 50, 60, 1)
        place_and_avoid(shieldicon, wall_group, nullgroup)
        health_group.add(shieldicon)

        health=MySprite()
        health.load("healthicon.png", 30,30,1)
        place_and_avoid(health, wall_group, nullgroup)
        health_group.add(health)
            
        #create skeleton group

       

        for n in range(0, (8+(level*2))):
            
            skeleton = MySprite()
            skeleton.load("skeletons.png", 32,48,4)
            place_and_avoid(skeleton, wall_group, player_group)
            skeleton.direction = random.randint(0,3) * 2
            
           
            
            
            skeleton_group.add(skeleton)
            
            

        #create jewels

        for n in range(0, leveltarget):
            
            jewel = MySprite()
            jewel.load("icejewel.png", 28,28,1)
            
            place_and_avoid(jewel, wall_group, nullgroup)
            jewel_group.add(jewel)

        #create bonuses

        for n in range (0, level+1):

            alloy=MySprite()
            alloy.load("alloy.png", 34,27,1)
            place_and_avoid(alloy, wall_group, nullgroup)
            alloy_group.add(alloy)

        #create shield icon
    
        
        player_moving = False
        
        player_start_y=player.Y
        


        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: sys.exit()
       

        status="Play"
            

        
        
#repeating loop
    while status=="Play":

        timer.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
       
        elif keys[K_UP]:
            player.direction = 0
            player_moving = True
        elif keys[K_RIGHT]:
            player.direction = 2
            player_moving = True
        elif keys[K_DOWN]:
            player.direction = 4
            player_moving = True
        elif keys[K_LEFT]:
            player.direction = 6
            player_moving = True
        elif keys[K_t]:
            play_sound(teleport)
            player.position=(random.randint(0,boundwidth), random.randint(0,boundheight))
            player_moving = False
        elif keys[K_l]:
            score=leveltarget
      
        else:
            player_moving = False


      
            #set animation frames based on player's direction
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns-1
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        if not player_moving:
            #stop animating when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            #move player in direction 
            player.velocity = calc_velocity(player.direction, 1.5)
            player.velocity.x *= 1.5
            player.velocity.y *= 1.5



        #manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > boundwidth: player.X = boundwidth
            if player.Y < 0: player.Y = 0
            elif player.Y > boundheight: player.Y = boundheight

        
        for z in skeleton_group:
            #set the skeleton's animation range
            z.first_frame = z.direction* z.columns
            z.last_frame = z.first_frame + z.columns-1
            if z.frame < z.first_frame:
                z.frame = z.first_frame
            z.velocity = calc_velocity(z.direction)

            #keep the skeleton on the screen        
            z.X += z.velocity.x
            z.Y += z.velocity.y
            if z.X < 0 or z.X > boundwidth or z.Y < 0 or z.Y > boundheight:
                reverse_direction(z)

            
            if pygame.sprite.collide_circle_ratio(3) (z, player) and not shield_group.__nonzero__():
                z.direction=get_player_direction(player, z)
            z.velocity = calc_velocity(z.direction)
            z.X += z.velocity.x
            z.Y += z.velocity.y
                
        

        #check wall collision

        player.rect=wall_collide(player, wall_group)

        for skeleton in skeleton_group:
            skeleton.rect=wall_collide(skeleton, wall_group)


        #check jewel pickup

        pickup_list=pygame.sprite.spritecollideany(player, jewel_group)

        if pickup_list!=None:

            if pygame.sprite.collide_rect_ratio(0.75) (player, pickup_list):
                play_sound(scoresound)
                score+=1
                pickup_list.kill()
                

        #check alloy pick up

        pickup_list=pygame.sprite.spritecollideany(player, alloy_group)

        if pickup_list!=None:

            if pygame.sprite.collide_rect_ratio(0.5) (player, pickup_list):
                play_sound(alloysound)
                score+=10
                pickup_list.kill()
            
        
        #check skeleton proximity

        collide_list=pygame.sprite.spritecollideany(player, skeleton_group)

        if collide_list!=None:

            if pygame.sprite.collide_rect_ratio(0.75) (player, collide_list):
                
                if not shield_group.__nonzero__():
                        
                        player_health-=1
                        play_sound(hit)
    
                if not shield_group.__nonzero__(): collide_list.X+=(random.randint(-10,10))

        #check health pickup

        if pygame.sprite.collide_rect_ratio(0.75) (player, health):
            player_health+=30
            play_sound(healthsound)
            if player_health>100: player_health=100
            place_and_avoid(health, wall_group, wall_group)

        #check shield pickup

        if pygame.sprite.collide_rect_ratio(0.75) (player, shieldicon) and not shield_group.__nonzero__():
            shield=PlayerEffect(12, player)
            shield.load("shield.png", 70,70,3)
            shield_group.add(shield)
            play_sound(pickup)
            place_and_avoid(shieldicon, wall_group, wall_group)
        
        #is player dead?
        if player_health <= 0:
            player_health=0
            status="gameover"
            player.kill()
            
        #has player won?

        if score==leveltarget:
            status="win"
            reset=True
            level+=1
            play_sound(levelupsound)
            leveltarget=score+45

        #clear the screen
        screen.blit(bg0, (0,0))

        #update and draw sprites

        skeleton_group.update(ticks, 50)
        player_group.update(ticks, 50)
        shield_group.update(ticks)
        jewel_group.update(ticks)
        alloy_group.update(ticks)
        wall_group.update(ticks, 50)
        health_group.update(ticks)
        timenow.update(ticks)
        
        jewel_group.draw(screen)
        alloy_group.draw(screen)
        wall_group.draw(screen)
        player_group.draw(screen)
        skeleton_group.draw(screen)
        health_group.draw(screen)
        shield_group.draw(screen)
        

        #draw energy bar

        
        print_text(font2, screen,650,650, ("Score: "+str(score)))
        print_text(font2, screen, 750,650, ("Level: "+str(level)))
       
        pygame.draw.rect(screen, (35,81,196,0), Rect(350,652,player_health*2,10))
        pygame.draw.rect(screen, (176,195,245,0), Rect(350,652,200,10), 2)

        print_text(font2, screen, 5,650, ("Survived  "+str(timenow)))

        

        pygame.display.update()

    while status=="win":
        
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: sys.exit()
   
        
      

        screen.blit(bg3, (400,300))

        pygame.display.update()

        pygame.time.wait(3000)

        screen.blit(bg0, (0,0))

        
        status="setup"
        

    while status=="gameover":
        
        screen.blit(bg2, (400,300))

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]: sys.exit()
   
        pygame.time.wait(2000)
        
        level=0
        score=0
        leveltarget=30
        
        status="introscreen"
        
        
    

