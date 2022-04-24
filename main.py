import os
import pygame
import random
import threading
pygame.init()

size = (1280,720)
title = "Сердечки"

class heart:
    def __init__(self,path):
        self.recreate(path)
    def _create(self):
        self.scale = random.randint(50,100)
        self.sprite = pygame.transform.scale(
            pygame.image.load(self.path),
            (self.scale,self.scale))
        self.speed = random.randint(5,25)
        self.x = random.randint(0,size[0]-self.scale)
        self.y = -self.scale
        self.alpha = self._alpha()
        self.ready = True
    def recreate(self,path):
        self.ready = False
        self.path = path
        threading.Thread(target=self._create,daemon=1).start()
    def _alpha(self):
        a = pygame.Surface((self.scale,self.scale),pygame.SRCALPHA)
        a.fill((0,0,0,255/(size[1]/self.speed)))
        for x in range(self.scale):
            for y in range(self.scale):
                if self.sprite.get_at((x,y))[3] == 0:
                    a.set_at((x,y),(0,0,0,0))
        return a
    def move(self):
        if not self.ready: return
        self.y += self.speed
        self.sprite.blit(self.alpha,(0,0))
        if self.y >= size[1]:
            self.recreate(self.path)
    def draw(self,surf):
        if not self.ready: return
        surf.blit(self.sprite,(self.x,self.y))

def gradient(c1,c2,w,h):
    s = pygame.Surface((1,2))
    s.set_at((0,0),c1)
    s.set_at((0,1),c2)
    return pygame.transform.smoothscale(s,(w,h))

hearts = [heart("sprites/"+random.choice(os.listdir("sprites"))) for i in range(25)]

win = pygame.display.set_mode(size)
pygame.display.set_caption(title+" [0 FPS]")

clock = pygame.time.Clock()

back = gradient((128,0,0),(8,0,0),*size)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.blit(back,(0,0))
    for i in hearts:
        i.move()
        i.draw(win)
    pygame.display.set_caption(f"{title} [{clock.get_fps()} FPS]")
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
