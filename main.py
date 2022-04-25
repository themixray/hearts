import os
import pygame
import random
import threading
pygame.init()

size = (1280,720)
title = "Сердечки"

class heart:
    def __init__(self,path,
                 z,pos=None,
                 temp=False):
        self.destroyed = False
        self.ready = False
        self.path = path
        self.temp = temp
        self.reload(z)
        self.recreate(pos)
    def reload(self,z):
        self.z = z
        self.scale = int((z/hearts_len*100)+50)
    def _create(self):
        self.sprite = pygame.transform.scale(
	        pygame.image.load(self.path),
	        (self.scale,self.scale))
        self.sprite.convert_alpha()
        self.speed = random.randint(5,25)
        self.alpha = 0
        self.ready = True
    def recreate(self,pos=None):
        if self.destroyed: return
        if pos == None:
            self.x = random.randint(0,size[0]-self.scale)
            self.y = -self.scale
        else:
            self.x, self.y = pos
        threading.Thread(target=self._create,daemon=1).start()
    def move(self):
        if self.destroyed: return
        if not self.ready: return
        self.y += self.speed
        self.alpha += 255/(size[1]/self.speed)
        self.sprite.set_alpha(255-self.alpha)
        if self.y >= size[1]:
            if not self.temp:
                self.reload(self.z)
                self.recreate()
            else:
                self.destroy()
    def draw(self,surf):
        if self.destroyed: return
        if not self.ready: return
        surf.blit(self.sprite,(self.x,self.y))
    def destroy(self):
        self.destroyed = True
        hearts.remove(self)
    def contains(self,pos):
        return pos[0] > self.x and pos[1] > self.y and pos[0] < self.x+self.scale and pos[1] < self.y+self.scale

def gradient(c1,c2,w,h):
    s = pygame.Surface((1,2))
    s.set_at((0,0),c1)
    s.set_at((0,1),c2)
    return pygame.transform.smoothscale(s,(w,h))

def make_heart(center):
    global hearts_len
    hearts.append(heart(
        "sprites/"+random.choice(os.listdir("sprites")),
        hearts_len,(center[0]-25,center[1]-25),True))
    hearts_len += 1
    for i in hearts:
        i.reload(i.z)
def delete_heart(center):
    h = None
    for i in hearts:
        if i.contains(center):
            h = i
            break
    if h != None:
        h.destroy()

win = pygame.display.set_mode(size)
pygame.display.set_caption(title+" [LOADING]")

hearts_len = 125
hearts = [heart("sprites/"+random.choice(os.listdir("sprites")),i) for i in range(hearts_len)]

clock = pygame.time.Clock()

back = gradient((192,0,0),(64,0,0),*size)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                make_heart(event.pos)
            if event.button == 1:
                delete_heart(event.pos)
    win.blit(back,(0,0))
    for i in hearts:
        i.move()
        i.draw(win)
    pygame.display.set_caption(f"{title} [{clock.get_fps()} FPS]")
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
