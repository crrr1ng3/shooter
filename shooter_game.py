#Створи власний Шутер!
from pygame import *
from random import randint
mixer.init()
font.init()

win_width, win_height = 700, 500
window = display.set_mode((win_width, win_height))
display.set_caption('Space shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 60
score = 0
max_lost = 3
goal = 7


mixer_music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, imageName, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(imageName), (65, 65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', -15, self.rect.centerx, self.rect.top)
        bullets.add(bullet)


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0






font2 = font.SysFont("comicsansms", 50)
font3 = font.SysFont("comicsansms", 15)

win = font2.render("Перемога!", 1, (255, 255, 255))
lose = font2.render("Поразка!", 1, (255, 255, 255))


spaceship = Player('rocket.png', 10, 300, 400)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(1, 3), randint(80, win_width-80), -40)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid("asteroid.png", randint(1, 7), randint(30, win_width -30), -40)
    asteroids.add(asteroid)

run = True
finish = False

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                spaceship.fire()

    if not finish:
        window.blit(background, (0, 0))
        spaceship.reset()
        spaceship.update()

        monsters.update()
        monsters.draw(window)
        
        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        lost_text = font3.render(f'Пропущено: {lost}', 1, (255, 255, 255))
        kills_text = font3.render(f'Збито: {score}', 1, (255, 255, 255))
        window.blit(kills_text, (0, 0))
        window.blit(lost_text, (0, 20))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(1, 5), randint(80, win_width-80), -40)
            monsters.add(monster)


        if sprite.spritecollide(spaceship, monsters, False) or sprite.spritecollide(spaceship, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        clock.tick(FPS)
        display.update()