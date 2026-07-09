from pygame import *
from random import choice

LEBAR, TINGGI = 700, 500
window = display.set_mode((LEBAR, TINGGI))
display.set_caption("Rakko's Journey")

bg = transform.scale(image.load('background.png'), (LEBAR, TINGGI))
gravitasi = 0.9

#Class
class GameSprite(sprite.Sprite):
  def __init__(self, img, x, y, w, h):
      super().__init__()
      self.image = transform.scale(image.load(img), (w, h))  
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y

  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)
        self.vel_y = 0
        self.on_ground =False
        self.jumppower = 18.3

    def update(self):
        keys = key.get_pressed()
        if keys[K_SPACE] and self.on_ground:
            self.vel_y = -self.jumppower
            self.on_ground = False
        self.vel_y += gravitasi
        self.rect.y += self.vel_y

        if self.rect.bottom >= TINGGI - 70:
            self.rect.bottom = TINGGI - 70
            self.vel_y = 0
            self.on_ground = True

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)

    def update(self):
        self.rect.x -= 7
        if self.rect.x < -90:
            self.rect.x = 800

class Awan(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)

    def update(self):
        self.rect.x -= 4
        if self.rect.x < -90:
            self.rect.x = 800

#objek
rakko = Player('rakko.webp', 100, 200, 90, 80)
mushi1 = Enemy('mushi.png', 600, 375, 70, 75)
mushi2 = Enemy('mushi2.png', 600, 355, 80, 90)
awan1 = Awan('awan.png', 600, 180, 90,90)
awan2 = Awan('awan.png', 650, 95, 195,210)

list_enemy = [mushi1, mushi2]
cur_enemy = choice(list_enemy)

score = 0 
hscore = 0

font.init()
f = font.SysFont('Arial', 36)
papan = f.render(f'Score: {score}', True, (0,0,0))
ulang = f.render('Press E to retry', True, (0,0,0))
high = f.render(f'Highscore:{hscore}', True, (0,0,0))

#FPS
clock = time.Clock()
FPS = 60

end = False
#Loop game
run = True
while run:
    clock.tick(60)

    #Mendeteksi event
    for e in event.get():
        if e.type == QUIT:
            run = False

    if end == False:
        high = f.render(f'Highscore:{hscore}', True, (0,0,0))
        papan = f.render(f'Score: {score}', True, (0,0,0))
        if sprite.collide_rect(rakko, cur_enemy):
            end = True
        if cur_enemy.rect.x < -40:
            cur_enemy = choice(list_enemy)
            cur_enemy.rect.x = 800
        window.blit(bg, (0,0)) 
        awan1.reset()
        awan1.update()
        awan2.reset()
        awan2.update()
        rakko.reset()
        rakko.update()
        cur_enemy.reset()
        cur_enemy.update()
        window.blit(papan, (10,10))
        window.blit(high, (10, 40))
        if cur_enemy.rect.x == rakko.rect.x :
            score += 1        
        if hscore < score:
            hscore = score
    if end == True:
        score = 0
        window.blit(ulang, (240,180))
        window.blit(high, (255, 210))
        keys = key.get_pressed()
        if keys[K_e]:
            end = False
            cur_enemy.rect.x = 800
        
    #Meletakkan Aset dan Objek
    display.update()
