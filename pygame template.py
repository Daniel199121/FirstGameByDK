# DESTROYER GAME

import random
from os import path
import pygame
from settings import *

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'sounds')
expl_dir = path.join(path.dirname(__file__), 'img\\explosion')
dir = path.dirname(__file__)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
level = 1


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rec = text_surface.get_rect()
    text_rec.midtop = (x, y)
    surf.blit(text_surface, text_rec)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def newEnemies():
    e = Enemies()
    all_sprites.add(e)
    enemies.add(e)

def newUfo():
    u = Ufo()
    all_sprites.add(u)
    ufos.add(u)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        #timeout power up
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        if self.hidden:
            return

        self.speedx, self.speedy = 0, 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.speedy != 0 and self.speedx != 0:
            self.speedx /= 1.414
            self.speedy /= 1.414
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > HEIGHT - 50:
            self.rect.top = HEIGHT - 50
        if self.rect.bottom < 50:
            self.rect.bottom = 50

    def powerup(self):
        self.power +=1
        self.power_time = pygame.time.get_ticks()

    def getPower(self):
        return self.power

    def levelup(self):
        self.level += 1
        self.level_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power < 3:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.power >= 3 and self.power <= 6:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.power > 6:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        #hide playe temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(enemies_images), (50, 38))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([0, WIDTH])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5
        self.shoot_delay = ENEMIES_SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        self.shoot()
        self.rect.x += self.vx
        self.vy += self.dy
        if self.rect.centerx >= WIDTH+10:
            self.vx *= -1
        elif self.rect.centerx <= -10:
            self.vx *= -1
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
            if self.rect.centery < 50:
                self.vy = 2
                self.dy = 0.5
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemybullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemybullet)
            enemyBullets.add(enemybullet)
            shoot_sound.play()

class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(random.choice(ufo_images), (65, 65))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([0, WIDTH])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = ENEMIES_SHOOT_DELAY
        self.last_shot = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.shoot()
        self.rect.x += self.vx
        self.vy += self.dy
        if self.rect.centerx >= WIDTH+10:
            self.vx *= -1
        elif self.rect.centerx <= -10:
            self.vx *= -1
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
            if self.rect.centery < 50:
                self.vy = 2
                self.dy = 0.5
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemybullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemybullet1 = EnemyBullet(self.rect.left, self.rect.centery)
            enemybullet2 = EnemyBullet(self.rect.right, self.rect.centery)

            all_sprites.add(enemybullet)
            all_sprites.add(enemybullet1)
            all_sprites.add(enemybullet2)
            enemyBullets.add(enemybullet)
            enemyBullets.add(enemybullet1)
            enemyBullets.add(enemybullet2)
            shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/ 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "DESTROYER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "High Score: "+str(round(highscore)), 22, WIDTH / 2, 15)
    draw_text(screen, "Press a key to begin, Press Q to quit", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keystate[pygame.K_q]:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def ufo_or_enemy_hit_us(enemy, score ):
    hits = pygame.sprite.spritecollide(player, enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= random.randrange(50, 100)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

def mob_hit_us():
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

def bullet_hit_enemy(enemy, min, max, chance, score):
    hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
    for hit in hits:
        score += random.randrange(min, max)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > chance:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

def bullet_hit_mob(score):
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

def take_powerup():
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            shield_sound.play()
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            power_sound.play()
            player.powerup()

def draw(score, highscore):
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(round(score)), 18, WIDTH / 2, 10)
    draw_text(screen, str(round((pygame.time.get_ticks() - beginning_time) / 1000)) + " s", 18, WIDTH - 50, 50)
    draw_text(screen, "LEVEL: " + str(level), 20, 60, HEIGHT - 50)
    draw_text(screen, "POWER: " + str(player.getPower()), 20, WIDTH - 60, HEIGHT - 50)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    if score >= highscore - 1:
        highscore = score
        draw_text(screen, "NEW HIGH SCORE: " + str(round(highscore)), 22, WIDTH / 2, HEIGHT / 2 + 40)
        with open(path.join(dir, HS_FILE), 'w') as f:
            f.write(str(score))
    else:
        draw_text(screen, "High Score: " + str(round(highscore)), 22, WIDTH / 2, 40)
    # *after* drawing everything, flip the display
    pygame.display.flip()



#Load graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip3_red.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "Meteors\meteorGrey_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "Lasers\laserBlue16.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "Lasers\laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png',
               'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png',
               'meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png',
               'meteorGrey_big4.png', 'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png',
               'meteorGrey_small2.png', 'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, 'Meteors\\'+img)).convert())
enemies_images = []
enemies_list = ['enemyBlack1.png', 'enemyBlack2.png', 'enemyBlack3.png', 'enemyBlack4.png', 'enemyBlack5.png',
            'enemyBlue1.png', 'enemyBlue2.png', 'enemyBlue3.png', 'enemyBlue4.png', 'enemyBlue5.png',
            'enemyGreen1.png', 'enemyGreen2.png', 'enemyGreen3.png', 'enemyGreen4.png', 'enemyGreen5.png',
            'enemyRed1.png', 'enemyRed2.png', 'enemyRed3.png', 'enemyRed4.png', 'enemyRed5.png']
for img in enemies_list:
    enemies_images.append(pygame.image.load(path.join(img_dir, 'Enemies\\'+img)).convert())
ufo_images = []
ufo_list = ['ufoBlue.png', 'ufoGreen.png', 'ufoRed.png', 'ufoYellow.png']
for img in ufo_list:
    ufo_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(10):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(path.join(expl_dir, filename)).convert()
    img.set_colorkey(BLACK)
    #img.set_colorkey(WHITE)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(expl_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'Power-ups\\shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'Power-ups\\bolt_gold.png')).convert()

#Load all games sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "weaponfire9.wav"))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, "plasmahit.wav"))
power_sound = pygame.mixer.Sound(path.join(snd_dir, "weapon1probl.wav"))
expl_sounds = []
for snd in ['explosion1.wav', 'explosion2.wav', 'explosion3.wav', 'explosion4.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir,snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'lowlife.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'Orbitron.wav'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)
#Load data of high score
with open(path.join(dir, HS_FILE), 'r') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0
#initializing lvl time
level_time = pygame.time.get_ticks()
# Game loop
game_over = True
running = True
while running:
    if game_over:
        level=1
        beginning_time = pygame.time.get_ticks()
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemyBullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        ufos = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(NUMBER_OF_MOBS+LVL_MOBS*level):
            if i < 12:
                newmob()
        score = 0
    #update level
    if pygame.time.get_ticks() - level_time > LEVEL_TIME:
        level += 1
        level_time = pygame.time.get_ticks()
        newmob()
        if level % 3 == 0:
            for i in range (1, level):
                if i < 6 and level <= 15:
                    newEnemies()
                if i < 10 and level > 15:
                    newEnemies()
        if level % 5 == 0:
            for i in range(1, level):
                if i < 3 and level <= 10:
                    newUfo()
                if i >= 3 and i <=6 and level <= 20:
                    newUfo()
                if i > 6 and i < 8 and level <=30:
                    newUfo()

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        keystate = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keystate[pygame.K_q]:
            running = False
    # Update
    all_sprites.update()

    # check to see if enemy bullet hit us
    hits = pygame.sprite.spritecollide(player, enemyBullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= random.randrange(10, 30)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    #check to see if bullet hit ufo
    bullet_hit_enemy(ufos, 50, 150, 0.85, score)

    # check to see if bullet hit enemy
    bullet_hit_enemy(enemies, 10, 50, 0.85, score)

    #check to see if bullet hit the mob
    bullet_hit_mob(score)

    #check to see if mob hit the player
    mob_hit_us()

    # check to see if enemy hit the player
    ufo_or_enemy_hit_us(enemies, score)

    # check to see if ufo hit the player
    ufo_or_enemy_hit_us(ufos, score)

    #check if the player hit a powerup
    take_powerup()

    #if the player died and explosion finished
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Draw / render
    draw(score, highscore)

pygame.quit()