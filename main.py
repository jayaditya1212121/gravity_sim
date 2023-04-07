import pygame, math, random
# screen size
width=1440
height= 810


timeframe= 1  #timestep multiplier

G=0.00003 #gravitational constant

#intiating pygame
pygame.init()

#display surface
screen= pygame.display.set_mode([width, height])
screen.fill((30, 30, 30))
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Gravity simulator xd")

# making it cute for liu

sun_surface=pygame.image.load('sun.png')

image_list=[]
for i in range(0,8):
    image_list.append(pygame.image.load(f'p{i}.png'))

#game clock
clock= pygame.time.Clock()
running= True


# planets class
planets_list= list()

class Planet:
    num=0
    def __init__(self,x,y,mass,radius, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.color= color
        self.tx=[]
        self.ty=[]
        self.instance = Planet.num
        Planet.num+=1



    def draw(self):
        if count%300 == 0:
            self.tx.append(self.x)
            self.ty.append(self.y)
        self.x= self.x + 1*self.dx*timeframe*timeframe
        self.y = self.y + 1*self.dy*timeframe*timeframe
        for i in range(0, len(self.tx)):
            pygame.draw.circle(screen,self.color, (self.tx[i], self.ty[i]), 1, 0)
        if animated == False:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
        else:
            planet_rect = image_list[self.instance%8].get_rect(center=(self.x, self.y))
            screen.blit(image_list[self.instance%8], planet_rect)


# Sun class
sun_list=[]
class Sun:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.mass=30000
        self.color= (230,255,106)
        self.radius= 35

    def draw(self):
        if animated== False:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)

        else:
            sun_rect = sun_surface.get_rect(center=(self.x, self.y))
            screen.blit(sun_surface, sun_rect)

# n random planets spawn
def spawn_planets(no_of_spawns):
    for _ in range(0, no_of_spawns):
        p = Planet(random.randint(50,width-50), random.randint(50, height-50), random.randint(1000,5000),random.randint(5,12),(random.randint(50,255),random.randint(50,255),random.randint(50,255)) )
        planets_list.append(p)

def spawn_planet(x,y):
    p = Planet(x, y, random.randint(1000, 5000),random.randint(5, 17), (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
    planets_list.append(p)

def spawn_sun(x,y):
    sun_list.append(Sun(x,y))
# resultant area for collisions
def resultant_area(p,q):
    return math.pi*(p.radius**2)+math.pi*(q.radius**2)


# resultant color for collisions
def color_avg(p,q):
    a=p.color
    b=q.color
    c=list()
    for i in range(0,3):
        c.append((a[i]+b[i])/2)
    return c

def area(p):
    return math.pi*(p.radius)**2

# inelastic collision solver
def collision(p,q):
    if type(p).__name__ == 'Planet' and type(q).__name__ == 'Planet' and planet_collisions== True:
        mass = p.mass + q.mass
        x = (p.x*area(p)+ q.x*area(q))/(area(p)+area(q))
        y = (p.y * area(p) + q.y * area(q)) / (area(p) + area(q))
        dx = ((p.dx * p.mass) + (q.dx * q.mass)) / mass
        dy = ((p.dy * p.mass) + (q.dy * q.mass)) / mass
        radius = math.sqrt(resultant_area(p,q)/math.pi)
        color= color_avg(p,q)

        planets_list.remove(p)
        planets_list.remove(q)

        new_planet= Planet(x,y, mass, radius, color )
        new_planet.dx=dx
        new_planet.dy=dy
        planets_list.append(new_planet)

    elif type(q).__name__ == 'Sun' and sun_collisions== True:
        planets_list.remove(p)




def distance(p,q):
    dist = math.dist((p.x, p.y), (q.x, q.y))
    if dist > p.radius+q.radius:
        return dist
    else:
        collision(p,q)
        return 0

def force(p,q):
    dist=distance(p,q)
    if dist != 0:
        force=-p.mass*q.mass*G/(dist**2)
        return force
    else:
        return 0

def acc(p,q):
    f=force(p,q)
    if f !=0:
        acc=f/p.mass

        return acc
    else:
        return 0

def angle(p,q):
    if p.x==q.x and p.y>q.y:
        angle=math.pi/2
    elif p.x==q.x and p.y<q.y:
        angle=math.pi*3/2
    else:
        angle=math.atan((q.y-p.y)/(q.x-p.x))

    return angle

def components(p,q):# acc x and y components
    a=acc(p,q)

    if p.x < q.x:
        p.dx -= a * math.cos(angle(p, q))
        p.dy -= a * math.sin(angle(p, q))
    else:
        p.dx += a * math.cos(angle(p, q))
        p.dy += a * math.sin(angle(p, q))

# driver code
#spawn_planets(10)
planet_collisions= False
sun_collisions= False
animated = False

#game loop
count = 0
c1=0
c2=0
c3=0
while running== True:
    count+=1
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running= False

            if event.key == pygame.K_p:
                c1+=1
                if c1%2 ==0:
                    planet_collisions = False
                if c1%2 ==1:
                    planet_collisions = True

            if event.key == pygame.K_s:
                c2+=1
                if c2%2 ==0:
                    sun_collisions = False
                if c2%2 ==1:
                    sun_collisions = True

            if event.key == pygame.K_a:
                c3+=1
                if c3%2 ==0:
                    animated = False
                if c3%2 ==1:
                    animated = True

            if event.key == pygame.K_r:
                planets_list.clear()
                sun_list.clear()


        if event.type== pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 3:
                spawn_sun(x,y)

            if event.button == 1:
                spawn_planet(x,y)


    # background surface render
    screen.fill((30, 30, 30))


    # physics
    for rp in planets_list:
        for s in sun_list:
            components(rp,s)
        for p in planets_list:
            if rp != p:
                components(rp, p)
            if rp not in planets_list:
                break

    #rendering
    for g in planets_list:
        g.draw()
    for s in sun_list:
        s.draw()

    pygame.display.update()




