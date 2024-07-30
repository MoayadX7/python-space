# imports -----------------------------------------
import pygame as pg
from pygame import gfxdraw
import math , random

# constants -----------------------------------------
constants = {"G": 6.67430e-11, "time_scale":20000}
# G : the gravitational constant
# time_scale : how much time passes in 1 frame (in seconds)
colors={"red":(255,0,0),"white":(255,255,255)}
# math functions -----------------------------------------
def euclidean_distance(first_point, second_point):
    return 1.0*math.sqrt(pow(first_point[0] - second_point[0], 2) + pow(first_point[1] - second_point[1], 2))


def gravitational_force_mangitude(mass_1, mass_2, distance):
    return constants["G"] * ((mass_1 * mass_2) / math.pow(distance, 2))

# object drawer ----------------------------------------- to draw text
class drawer:
    radius=1
    mass=1
    def __init__(self,radius,mass) -> None:
        drawer.radius=radius
        drawer.mass=mass
    @classmethod
    def draw(cls):
     
        radius_image=font.render("Radius: "+str(cls.radius),True,colors["red"])
        mass_image=font.render("mass: "+str(cls.mass),True,colors["red"])
        screen.blit(radius_image,(10,10))
        screen.blit(mass_image,(150,10))
        
    


# celestial objects -----------------------------------------
class space_object:
    universe=[] # "universe" variable is needed to keep track of all objects in the space and estimate the gravitational force for everything so all things attract each other like in a real space time 
    # ----------------

    # ----------------
    def __init__(self, radius, x, y) -> None:
        self.radius=radius
        self.mass = 3.14*(radius/2)**2
        self.position_x = x
        self.position_y = y
        self.v_x=0
        self.v_y=0
        self.golem=False
        space_object.universe.append(self)
    def place_in_space(self):
        if self.position_x-self.radius/2>800 or self.position_x+self.radius/2<0 or self.position_y-self.radius/2>600 or self.position_y+self.radius/2<0:
            return
        x_cord=int(self.position_x)
        y_cord=int(self.position_y)
        gfxdraw.aacircle(screen, x_cord, y_cord,int(self.radius), colors["white"])
        gfxdraw.filled_circle(screen,  x_cord, y_cord,int(self.radius), colors["white"])
    @classmethod
    def do_the_magic(cls) -> None: # change positions and velocities according to gravity :)
        if not pause_game:
            for i in range (0,len(cls.universe)):
                for o in range (i+1,len(cls.universe)):
                    
                    object_1=cls.universe[i]
                    object_2=cls.universe[o]
                    if object_1 == object_2:
                        continue
                    r=euclidean_distance((object_1.position_x,object_1.position_y),(object_2.position_x,object_2.position_y))
         
                    if r <= object_1.radius+object_2.radius:
                        if object_1.golem!=True: # universe center index is 0 and it must not move
                            object_1.position_x+=object_1.v_x*constants["time_scale"]
                            object_1.position_y+=object_1.v_y*constants["time_scale"]
                        if object_2.golem!=True: # universe center index is 0 and it must not move
                            object_2.position_x+=object_2.v_x*constants["time_scale"]
                            object_2.position_y+=object_2.v_y*constants["time_scale"]
                        continue
                    F=gravitational_force_mangitude(object_1.mass,object_2.mass,r)
                    Fx=F*((object_2.position_x-object_1.position_x)/r)
                    Fy=F*((object_2.position_y-object_1.position_y)/r)
                    ax1=Fx/object_1.mass
                    ax2=Fx/object_2.mass
                    ay1=Fy/object_1.mass
                    ay2=Fy/object_2.mass
                    # ------------------
                    object_1.v_x+=ax1*constants["time_scale"]
                    object_1.v_y+=ay1*constants["time_scale"]
                    object_2.v_x-=ax2*constants["time_scale"]
                    object_2.v_y-=ay2*constants["time_scale"]
                    # ------------------
                    if object_1.golem!=True: # universe center index is 0 and it must not move
                        object_1.position_x+=object_1.v_x*constants["time_scale"]
                        object_1.position_y+=object_1.v_y*constants["time_scale"]
                    if object_2.golem!=True: # universe center index is 0 and it must not move
                        object_2.position_x+=object_2.v_x*constants["time_scale"]
                        object_2.position_y+=object_2.v_y*constants["time_scale"]
            
        for  celestial_body in cls.universe:
            celestial_body.place_in_space()
            


# initialize game -----------------------------------------
pg.init()
font=pg.font.SysFont("Arial",30)
# initialize the window -----------------------------------------

screen = pg.display.set_mode((800, 600))  # windows size
pg.display.set_caption("Space simulator")  # title text
icon = pg.image.load("assets/planet.png")  # load icon asset
pg.display.set_icon(icon)  # set the icon

# main loop -----------------------------------------
pause_game=False
game_state = True
while game_state:
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            game_state = False
        elif event.type == pg.KEYDOWN:
            if event.key== pg.K_SPACE:
                pause_game=not pause_game
            elif event.key== pg.K_r:
                drawer.radius+=10
            elif event.key== pg.K_t:
                drawer.mass+=10
            elif event.key== pg.K_f:
                drawer.radius-=10
            elif event.key== pg.K_g:
                drawer.mass-=10
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            space_object(drawer.radius,mouse_x,mouse_y)
            space_object.universe[-1].mass=drawer.mass
    screen.fill((4, 12, 36))  # screen BG-color
    space_object.do_the_magic()
    drawer.draw()
    
    pg.display.update()
    
    
    
