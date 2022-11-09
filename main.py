import pygame, sys, math, time

height = 600
width = 600
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def line(start_pos, end_pos, w = 1, col = 'white'):
    pygame.draw.line(screen, col, start_pos, end_pos, w)

def circle(cent, rad, col = 'white', w = 0):
    pygame.draw.circle(screen, col, cent, rad, w)

class Point():
    def __init__(self, center, color='white'):
        self.color = color
        self.center = center
        self.radius = 1
        self.vel = 50

    def render(self):
        circle(self.center, self.radius, self.color)

    def update(self, dt):
        self.center[0] += self.vel * dt

class CircularMotion():
    def __init__(self, radius):
        self.radius = radius
        self.color = 'white'
        self.point_color = 'red'
        self.center = (self.radius, height/2)
        self.angle = 0
        self.d_angle = 1
        self.v = (self.radius * math.cos(math.radians(self.angle)), -self.radius * math.sin(math.radians(self.angle)))
        self.p = (self.center[0] + self.v[0], self.center[1] + self.v[1])

        self.tg_stp = [self.radius*2, self.center[1]-self.radius]
        self.tg_enp = [self.radius*2, self.center[1]+self.radius]
        self.tg_cp = [self.radius*2, self.p[1]]

        self.sinps = list()

    def render(self, dt):
        circle(self.center, self.radius, w=1)
        line(self.tg_stp, self.tg_enp)

        self.angle += self.d_angle * dt
        self.angle = (self.angle + 1) % 360
        self.v = (self.radius * math.cos(math.radians(self.angle)), -self.radius * math.sin(math.radians(self.angle)))
        self.p = (self.center[0] + self.v[0], self.center[1] + self.v[1])
        line(self.center, self.p)
        circle(self.p, 4, 'red')

        self.tg_cp = [self.radius*2, self.p[1]]
        line(self.p, self.tg_cp, col='green')
        circle(self.tg_cp, 4, 'blue')

        self.update(dt)
        self.show_sinps()

    def update(self, dt):
        for p in self.sinps:
            p.update(dt)

        if len(self.sinps) > 400:
            self.sinps.pop(0)

        self.sinps.append(Point(self.tg_cp))


    def show_sinps(self):
        for p in self.sinps:
            p.render()


c = CircularMotion(100) 
pt = time.time()

while True:

    now = time.time()
    dt = now - pt
    pt = now

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((25, 25, 25))

    c.render(dt)

    pygame.display.flip()
    clock.tick(fps)