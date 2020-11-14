import pygame
import pygame.freetype
import time
import random
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from math import pi, cos, sin, atan2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)
RED_2 = (255,0,0)
GREEN =(0,200,0)
GREEN_2 = (71, 161, 42)
RED = (161, 48, 42)
FONDO =  (55, 102, 196)
WIN_FONDO = (201, 116, 24)


#textos a mostrar
bienvenida = ''
teclas = ''

clock = pygame.time.Clock()


#paredes 1 y 2 ladrillo, 3 puertas
textures = {
  "1": pygame.image.load('Lab3\walls1.jpg'),
  "2": pygame.image.load('Lab3\walls1.jpg'), 
  "3": pygame.image.load('Lab3\p1.jpg'),
  "4": pygame.image.load('Lab3\heil.jpg')

}

#Jugador porque no encontre un sprite bonito de varita magica
player = pygame.image.load('Lab3\player.png')

enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": pygame.image.load('Lab3\g.png')
  },
  {
    "x": 280,
    "y": 190,
    "texture": pygame.image.load('Lab3\s1.png')
  }
]

out = [
  {
    "x": 430,
    "y": 430,
    "texture": pygame.image.load('Lab3\key.png')
  }
]

class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "a": pi/3,
      "fov": pi/3
    }
    self.map = []
    self.zbuffer = [-float('inf') for z in range(0, 500)]
    # self.clear()

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 50):
      for cy in range(y, y + 50):
        tx = int((cx - x)*128 / 50)
        ty = int((cy - y)*128 / 50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  #vision del jugador
  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)

      i = int(x/50)
      j = int(y/50)

      if self.map[j][i] != ' ':
        hitx = x - i*50
        hity = y - j*50

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / 50)

        return d, self.map[j][i], tx

      self.point(int(x), int(y), (255, 255, 255))

      d += 1

  def draw_stake(self, x, h, texture, tx):
    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      ty = int(((y - start)*128)/(end - start))
      c = texture.get_at((tx, ty))
      self.point(x, y, c)

  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

    sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
    sprite_size = (500/sprite_d) * 70

    sprite_x = 500 + (sprite_a - self.player["a"])*500/self.player["fov"] + 250 - sprite_size/2
    sprite_y = 250 - sprite_size/2

    sprite_x = int(sprite_x)
    sprite_y = int(sprite_y)
    sprite_size = int(sprite_size)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
          tx = int((x - sprite_x) * 128/sprite_size)
          ty = int((y - sprite_y) * 128/sprite_size)
          c = sprite["texture"].get_at((tx, ty))
          #color enemigoS
          if c != (191, 191, 191, 255):
            self.point(x, y, c)
            self.zbuffer[x - 500] = sprite_d

  def draw_player(self, xi, yi, w = 256, h = 256):
    for x in range(xi, xi + w):
      for y in range(yi, yi + h):
        tx = int((x - xi) * 32/w)
        ty = int((y - yi) * 32/h)
        c = player.get_at((tx, ty))
        if c != (152, 0, 136, 255):
          self.point(x, y, c)

  #codigo extraido del hint: https://pythonprogramming.net/pygame-start-menu-tutorial/
  def menu_screen(self):
    menu = True

    while menu:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            self.game_start()
        
      
      gameDisplay.fill(FONDO)
      largeText = pygame.font.Font('freesansbold.ttf',50)
      TextSurf, TextRect = self.text_objects("Welcome to Hounted Castle", largeText)
      TextRect.center = (500,200)
      gameDisplay.blit(TextSurf, TextRect)
      smallText =  pygame.font.Font('freesansbold.ttf',20)
      TextSurf, TextRect = self.text_objects("Click or press SPACE for start", smallText)
      TextRect.center = (500,300)
      gameDisplay.blit(TextSurf, TextRect)
      TextSurf, TextRect = self.text_objects("Reach the key and the door", smallText)
      TextRect.center = (500,250)
      gameDisplay.blit(TextSurf, TextRect)


      #BUTTON PLAY 
      self.button('Start', 300, 400, 80, 50, GREEN_2, GREEN, 'play')
      self.button('Quit', 600, 400, 80, 50, RED, RED_2, 'quit')
      pygame.display.update()
      clock.tick(15)

  def win_screen(self):
    menu = True

    while menu:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quit()
      
      gameDisplay.fill(WIN_FONDO)
      largeText = pygame.font.Font('freesansbold.ttf',50)
      TextSurf, TextRect = self.text_objects("You Won!!", largeText)
      TextRect.center = ((int(1000/2)),(int(400/2)))
      gameDisplay.blit(TextSurf, TextRect)

      #BUTTON PLAY 
      #self.button('AGAIN!', 300, 400, 80, 50, GREEN_2, GREEN, 'play')
      self.button('Quit', 500, 400, 80, 50, RED, RED_2, 'quit')
      pygame.display.update()
      clock.tick(15)

  def pause_screen(self):
    menu = True

    while menu:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          quit()
      
      gameDisplay.fill(WHITE)
      largeText = pygame.font.Font('freesansbold.ttf',50)
      TextSurf, TextRect = self.text_objects("We are paused", largeText)
      TextRect.center = ((int(1000/2)),(int(400/2)))
      gameDisplay.blit(TextSurf, TextRect)

      #BUTTON PLAY 
      self.button('Start', 300, 400, 80, 50, BLACK, GREEN, 'play')
      self.button('Quit', 600, 400, 80, 50, BLACK, RED, 'quit')
      pygame.display.update()
      clock.tick(15)
			


  def button(self, msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
          if action == 'play':
            self.game_start()
          elif action == 'quit':
            pygame.quit()
            quit()
          elif action == 'pause':
            print('pause button')

    else:
      pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText =  pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = self.text_objects(msg, smallText)
    TextRect.center = ((int(x+(w/2))),(int(y+(h/2))))
    gameDisplay.blit(TextSurf, TextRect)


  def text_objects(self, text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

  def game_start(self):
    while True:
      screen.fill((113, 113, 113))
      self.render()

      for e in pygame.event.get():
        if self.player["x"] >= 400 and self.player["x"] >= 400:
          self.win_screen()

        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
          exit(0)
        if e.type == pygame.KEYDOWN:
          if e.key == pygame.K_a:
            self.player["a"] -= pi/10
          elif e.key == pygame.K_d:
            self.player["a"] += pi/10

          elif e.key == pygame.K_RIGHT:
            self.player["x"] += 10
          elif e.key == pygame.K_LEFT:
            self.player["x"] -= 10
          elif e.key == pygame.K_UP:
            self.player["y"] += 10
          elif e.key == pygame.K_DOWN:
            self.player["y"] -= 10
          elif e.key == pygame.K_p:
            self.win_screen()

          if e.key == pygame.K_f:
            if screen.get_flags() and pygame.FULLSCREEN:
                pygame.display.set_mode((1000, 500))
            else:
                pygame.display.set_mode((1000, 500),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

      pygame.display.flip()

  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, textures[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(0, 500):
      try:
        a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
        d, c, tx = self.cast_ray(a)
        x = 500 + i
        h = 500/(d*cos(a-self.player["a"])) * 70
        self.draw_stake(x, h, textures[c], tx)
        self.zbuffer[i] = d
      except:
        pass

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (0, 0, 0))
      self.draw_sprite(enemy)

    for outs in out:
      self.point(outs["x"], outs["y"], (0, 0, 0))
      self.draw_sprite(outs)

    self.draw_player(1000 - 256 - 128, 500 - 256)

pygame.init()
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('Lab3\hola2.txt')
gameDisplay = pygame.display.set_mode((1000, 500))
r.menu_screen()
c = 0
