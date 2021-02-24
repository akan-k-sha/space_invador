import pygame
import random
import math
from pygame import mixer
#initializing the pygame
pygame.init()

#creating the screen
screen=pygame.display.set_mode((800,600))

#background
background=pygame.image.load("space.jpg")

#backround sound
mixer.music.load("background.wav")
mixer.music.play(-1)
#-1 to make it play on loop

#Title and Icon
pygame.display.set_caption("Space Invader")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon )

#adding player
player_img=pygame.image.load("player.png")
player_x=370
player_y=480
x_pos_change=0

#adding enemy
enemy_img=[]
enemy_x=[]
enemy_y=[]
enemy_xchange=[]
enemy_ychange=[]
count_enemy=6

for i in range(count_enemy):
    enemy_img.append(pygame.image.load("space-monster.png"))
    enemy_x.append(random.randint(0,736))
    enemy_y.append(random.randint(50,150))
    enemy_xchange.append(0.3)
    enemy_ychange.append(40)


#adding bullets
bullet_img=pygame.image.load("bullet.png")
bullet_x=0
bullet_y=480        #the bullet will always be shot from the spaceship whose y cordinate is fixed at 480
bullet_ychange=0.8 
bullet_state="ready"
#ready- we cant see the bullet on the screen
#fire-the bullet is currently moving

#score board
score=0
font=pygame.font.Font('freesansbold.ttf',28)
test_x=15
test_y=15

#game_over
over_font=pygame.font.Font("freesansbold.ttf",64)

def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

#will be called when ever a space bar is pressed
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet_img,(x+16,y+10))

#detecting the collision
def is_collision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance=math.sqrt(((enemy_x-bullet_x)**2)+((enemy_y-bullet_y)**2))
    if distance<=20:
        return True
    return False 

def display_score(x,y):
    result=font.render("Score:-" + str(score),True,(255,255,255))
    screen.blit(result,(x,y))

def game_over():
    over_stat=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_stat,(200,250))
#gaming loop
running=True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False 
        #detecting a keystroke
        if event.type==pygame.KEYDOWN:
            print("KEY PRESSED")
            if event.key==pygame.K_LEFT:
                print("Left arrow pressed")
                x_pos_change=-0.8
            if event.key==pygame.K_RIGHT:
                print("Right arrow pressed")
                x_pos_change=0.8

            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    #to get the currrent x co ordinae of space ship so that bullet doesnt moves along the space ship
                    bullet_x =player_x
                    fire_bullet(bullet_x,bullet_y)
        #detecting key_release
        if event.type==pygame.KEYUP:
            print("KEY RELEASED")
            x_pos_change=0
    
    #spaceshp movement
    player_x+=x_pos_change 
    if player_x<=0:
        player_x=0
    elif player_x>=736:
        player_x=736
    player(player_x,player_y)
    #enemy movement
    for i in range(count_enemy):
        if enemy_y[i]>460:
            for j in range(count_enemy):
                enemy_y[j]=2000
            game_over()
            break
        enemy_x[i]+=enemy_xchange[i]
        if enemy_x[i]<=0:
            enemy_xchange[i]=0.3
            enemy_y[i]+=enemy_ychange[i]
        elif enemy_x[i]>=739:
            enemy_xchange[i]-=0.3
            enemy_y[i]+=enemy_ychange[i]

        #game over
        

        #collision mechanics
        collision=is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_y=480
            bullet_state="ready"
            enemy_x[i]=random.randint(0,736)
            enemy_y[i]=random.randint(50,150)
            score+=1
        enemy(enemy_x[i],enemy_y[i ],i)

    #bullet movement
    if bullet_y<=0:
        bullet_y=480
        bullet_state="ready"
    if bullet_state=="fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y-=bullet_ychange

    display_score(test_x,test_y)
    pygame.display.update()
