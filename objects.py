import pygame as pg
import math
from settings import *
vec=pg.Vector2


class Polygon:
    def __init__(self,game,pos,originals):
        self.originals=originals
        self.vel=vec(0,0)
        self.pos=vec(pos)
        self.game=game
        self.angle=0
        self.image,_=self.render()
        self.rect=self.image.get_rect()
        self.hit_bourd_rect=self.rect.copy()
    def rotate(self):
        for n, point in enumerate(self.points):
            self.points[n].x = (self.originals[n].x * math.cos(self.angle) - self.originals[n].y * math.sin(
                self.angle))+self.pos.x
            self.points[n].y = (self.originals[n].x * math.sin(self.angle) + self.originals[n].y * math.cos(
                self.angle))+self.pos.y

    def update(self):

        self.pos+=self.vel*self.game.dt
        self.image,offset=self.render()
        self.rect=self.image.get_rect()
        self.rect.center=self.pos+offset
        self.hit_bourd_rect=self.image.get_rect()
        self.hit_bourd_rect.center=self.rect.center

        if self.rect.bottom< 0:
            self.pos.y = HEIGHT-(self.rect.height/2+offset.y)
        elif self.rect.top > HEIGHT:
            self.pos.y= self.rect.height/2-offset.y
        if self.rect.right< 0:
            self.pos.x = WIDTH-(self.rect.width/2+offset.x)
        elif self.rect.left> WIDTH:
            self.pos.x = self.rect.width/2-offset.x

    def move(self,val):
        # normal to the vector to the current vector
        vec_to_angle=vec(math.sin(self.angle),-math.cos(self.angle))
        vec_to_angle*=val/vec_to_angle.length()
        self.vel+=vec_to_angle

    def add_angle(self,val):
        self.angle+=val

    def render(self):
        points = [v.copy() for v in self.originals]
        for n, point in enumerate(points):
            points[n].x = (self.originals[n].x * math.cos(self.angle) - self.originals[n].y * math.sin(
                self.angle))
            points[n].y = (self.originals[n].x * math.sin(self.angle) + self.originals[n].y * math.cos(
                self.angle))
        x_vals = [v.x for v in points]
        y_vals = [v.y for v in points]
        min_x = min(x_vals)
        min_y = min(y_vals)
        max_x = max(x_vals)
        max_y = max(y_vals)
        width = max_x - min_x
        height = max_y - min_y
        image = pg.Surface((width+1, height+1),pg.SRCALPHA)

        points=[v-vec(min_x,min_y) for v in points]

        for n, p in enumerate(points):

            pg.draw.line(image, WHITE, points[n],
                         points[(n + 1) % len(points)])
        center=vec(0,0)
        for p in points:
            center+=p
        center/=len(points)

        offset=vec(width/2,height/2)-center
        return image,offset

    def draw(self,surf):
        surf.blit(self.image, self.rect)



        if self.rect.top<0:
            try:
                height= abs(self.rect.top) + self.vel.y * self.game.dt
                subs = self.image.subsurface(0, 0, self.image.get_width(), height)
                surf.blit(subs, (self.rect.left, HEIGHT - subs.get_height()))
                self.hit_bourd_rect.top=HEIGHT - subs.get_height()
                self.hit_bourd_rect.left=self.rect.left
            except:
                pass
        elif self.rect.bottom>HEIGHT:
            height=self.rect.bottom-HEIGHT-self.vel.y*self.game.dt
            try:
                subs = self.image.subsurface(0, self.image.get_height() - height, self.image.get_width(),height)
                surf.blit(subs, (self.rect.left, 0))
                self.hit_bourd_rect.bottom=height
                self.hit_bourd_rect.left = self.rect.left
            except:
                pass
        if self.rect.left<0:
            try:
                width=abs(self.rect.left)+self.vel.x*self.game.dt
                subs=self.image.subsurface(0, 0, width, self.image.get_height())
                surf.blit(subs, (WIDTH-subs.get_width(), self.rect.top))
                self.hit_bourd_rect.top = self.rect.top
                self.hit_bourd_rect.left= WIDTH-subs.get_width()
            except:
                pass
        elif self.rect.right>WIDTH:
            try:
                width=self.rect.right-WIDTH-self.vel.x*self.game.dt
                subs=self.image.subsurface(self.image.get_width() - width, 0, width, self.image.get_height())
                surf.blit(subs, (0, self.rect.top))
                self.hit_bourd_rect.top = self.rect.top
                self.hit_bourd_rect.right=width
            except:
                pass
        #pg.draw.rect(surf, RED, self.hit_bourd_rect, 1)

class Asteroid(Polygon):
    def __init__(self,game,pos,originals,size):
        super().__init__(game,pos,originals)
        self.size=size


class Bullet:
    def __init__(self,game,pos,radius,vel_scale,obj_angle):
        self.pos=vec(pos)
        self.radius=radius
        #self.vel=vec(math.cos(obj_angle),math.sin(obj_angle))*vel_scale
        self.vel = vec(-math.sin(obj_angle), math.cos(obj_angle)) * vel_scale*-1
        self.game=game
    def update(self):
        self.pos+=self.vel*self.game.dt

    def check_beyond_bound(self):
        if self.pos.x>WIDTH:
            return True
        elif self.pos.x<0:
            return True
        if self.pos.y>HEIGHT:
            return True
        elif self.pos.y<0:
            return True
        return False
    def draw(self,surf):
        pg.draw.circle(surf,WHITE,self.pos,self.radius,1)


