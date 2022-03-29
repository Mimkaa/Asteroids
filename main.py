import pygame as pg
import sys
from settings import *
from objects import *
from os import path
import random
import time
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.paused=False


    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.score=0

        self.player=Polygon(self,(WIDTH//2,HEIGHT//2),[vec(-15,20),vec(0,-30),vec(15,20)])
        angle = random.uniform(0, math.pi * 2)
        self.player.vel = vec(math.cos(angle), math.sin(angle)) * random.uniform(100, 150)


        # create some asteroids
        self.asteroids = []
        theta = (math.pi * 2) / 20
        surcom_points = []
        for j in range(20):
            surcom_points.append(vec( math.cos(theta * j), math.sin(theta * j))*128*random.uniform(0.8,1))

        for i in range(2):
            if i==0:
                dir_vec_player = vec(-math.sin(self.player.angle), math.cos(self.player.angle))
                dir_vec = vec(-dir_vec_player.y, dir_vec_player.x)*256
                self.asteroids.append(Asteroid(self,self.player.pos+dir_vec,surcom_points,128))
            else:
                dir_vec_player =vec(-math.sin(self.player.angle), math.cos(self.player.angle))
                dir_vec = vec(-dir_vec_player.y, dir_vec_player.x) *256
                dir_vec*=-1

                self.asteroids.append(Asteroid(self, self.player.pos+dir_vec, surcom_points, 128))
        for ast in self.asteroids:
            angle=random.uniform(0,math.pi*2)
            ast.vel=vec(math.cos(angle),math.sin(angle))*random.uniform(100,150)

        # projectiles
        self.projectiles=[]


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:

                self.dt = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop

        self.player.update()
        for ast in self.asteroids:
            ast.update()

        for n, ast in enumerate(self.asteroids):
            if math.sqrt((ast.pos.x - self.player.pos.x) ** 2 + (ast.pos.y - self.player.pos.y) ** 2) < ast.size:
                self.paused=True
                self.show_go_screen()

        if not self.asteroids:
            theta = (math.pi * 2) / 20
            surcom_points = []
            for j in range(20):
                surcom_points.append(vec(math.cos(theta * j), math.sin(theta * j)) * 128 * random.uniform(0.8, 1))

            for i in range(2):
                if i == 0:
                    dir_vec_player = vec(-math.sin(self.player.angle), math.cos(self.player.angle))
                    dir_vec = vec(-dir_vec_player.y, dir_vec_player.x) * 256
                    self.asteroids.append(Asteroid(self, self.player.pos + dir_vec, surcom_points, 128))
                else:
                    dir_vec_player = vec(-math.sin(self.player.angle), math.cos(self.player.angle))
                    dir_vec = vec(-dir_vec_player.y, dir_vec_player.x) * 256
                    dir_vec *= -1

                    self.asteroids.append(Asteroid(self, self.player.pos + dir_vec, surcom_points, 128))
            for ast in self.asteroids:
                angle = random.uniform(0, math.pi * 2)
                ast.vel = vec(math.cos(angle), math.sin(angle)) * random.uniform(100, 150)
            self.score+=1000


        if self.projectiles and self.asteroids:
            for n,p in enumerate(self.projectiles):
                p.update()
                if p.check_beyond_bound():
                    self.projectiles.pop(n)



            for n,ast in enumerate(self.asteroids):
                for m,b in enumerate(self.projectiles):
                    if math.sqrt((b.pos.x-ast.pos.x)**2+(b.pos.y-ast.pos.y)**2)<ast.size:
                        self.asteroids.pop(n)
                        if ast.size>32:
                            for i in range(2):

                                theta = (math.pi * 2) / 20
                                surcom_points = []
                                for j in range(20):
                                    surcom_points.append(vec(math.cos(theta * j), math.sin(theta * j)) * ast.size/2*random.uniform(0.8,1))
                                aster_n=Asteroid(self, ast.pos, surcom_points,ast.size/2)
                                angle = random.uniform(0, math.pi * 2)
                                aster_n.vel = vec(math.cos(angle), math.sin(angle)) * random.uniform(100, 150)
                                self.asteroids.append(aster_n)
                        self.projectiles.pop(m)
                        self.score+=100







    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)


        self.player.draw(self.screen)

        for ast in self.asteroids:
            ast.draw(self.screen)

        if self.projectiles:
            for p in self.projectiles:
                p.draw(self.screen)

        # double check for the case when a bullet collide a subsurf
        for n, ast in enumerate(self.asteroids):
            for m, b in enumerate(self.projectiles):
                if ast.hit_bourd_rect.topleft != ast.rect.topleft:
                    r_pos = vec(ast.hit_bourd_rect.center)
                    if math.sqrt((b.pos.x - r_pos.x) ** 2 + (b.pos.y - r_pos.y) ** 2) < ast.size:
                        self.asteroids.pop(n)
                        if ast.size > 32:
                            for i in range(2):

                                theta = (math.pi * 2) / 20
                                surcom_points = []
                                for j in range(20):
                                    surcom_points.append(vec(math.cos(theta * j),
                                                             math.sin(theta * j)) * ast.size / 2 * random.uniform(
                                        0.8, 1))
                                aster_n = Asteroid(self, r_pos, surcom_points, ast.size / 2)
                                angle = random.uniform(0, math.pi * 2)
                                aster_n.vel = vec(math.cos(angle), math.sin(angle)) * random.uniform(100, 150)
                                self.asteroids.append(aster_n)
                        self.projectiles.pop(m)
                        self.score += 100


        for n, ast in enumerate(self.asteroids):
            if ast.hit_bourd_rect.topleft != ast.rect.topleft:
                r_pos = vec(ast.hit_bourd_rect.center)
                if math.sqrt((r_pos.x - self.player.pos.x) ** 2 + (r_pos.y - self.player.pos.y) ** 2) < ast.size:
                    self.paused=True
                    self.show_go_screen()

        # dir_vec_player = vec(-math.sin(self.player.angle), math.cos(self.player.angle))
        #
        # dir_vec=vec(-dir_vec_player.y,dir_vec_player.x)*64
        # pg.draw.line(self.screen,RED,self.player.pos,self.player.pos+dir_vec)

        # fps
        r=self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        self.draw_text(f"SCORE:{self.score}", self.font, 40, WHITE, 50, 50+r.height+10)
        pg.display.flip()

    def events(self):
        # catch all events here

        keys = pg.key.get_pressed()
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.player.add_angle(0.1)
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.player.add_angle(-0.1)
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.player.move(50)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_SPACE:
                    self.projectiles.append(Bullet(self,self.player.pos,3,500,self.player.angle))




    def show_go_screen(self):
        self.screen.fill(BLACK)
        r=self.draw_text( 'GAME OVER', self.font, 100, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text(f"YOUR SCORE:{self.score}", self.font, 50, WHITE, WIDTH / 2, HEIGHT /2 + r.height+10,
                       align='center')
        self.draw_text("Press a key to start or ESCAPE to exit", self.font, 50, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                       align='center')

        while self.paused:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

                if event.type==pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = False
                        self.quit()
                if event.type == pg.KEYUP:

                        self.new()
                        self.run()
                        self.paused=False


            pg.display.flip()
            self.clock.tick(FPS)

    def show_start_screen(self):
        # game splash/start screen

        self.screen.fill(BLACK)
        self.draw_text('ASTEROIDS', self.font, 100, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
        pg.display.flip()
        time.sleep(1)
        self.wait_for_key()


    def wait_for_key(self):

        waiting = True
        count = 0

        while waiting:
            count += 1
            if count % 2 == 0:
                self.draw_text("Press a key to start ", self.font, 50, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                          align='center')
            else:
                self.draw_text("Press a key to start " , self.font, 50, BLACK, WIDTH / 2, HEIGHT * 3 / 4,
                          align='center')
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    waiting = False
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()

            pg.display.flip()
            self.clock.tick(5)

g = Game()
g.show_start_screen()
g.new()
g.run()




