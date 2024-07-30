# imports -----------------------------------------
import pygame as pg
import math

# constants -----------------------------------------
constants = {"G": 6.67430e-11, "time_scale":10000}
# G : the gravitational constant
# time_scale : how much time passes in 1 frame (in seconds)
colors={"red":(255,0,0)}
# math functions -----------------------------------------
def euclidean_distance(first_point, second_point):
    return 1.0*math.sqrt(pow(first_point[0] - second_point[0], 2) + pow(first_point[1] - second_point[1], 2))


def gravitational_force_mangitude(mass_1, mass_2, distance):
    return constants["G"] * ((mass_1 * mass_2) / math.pow(distance, 2))


# celestial objects -----------------------------------------
class space_object:
    
    universe=[] # "universe" variable is needed to keep track of all objects in the space and estimate the gravitational force for everything so all things attract each other like in a real space time 
    # ----------------
    mass = 0
    position_x = 0
    position_y = 0
    # horizantal and vertical velocity
    v_x=0 
    v_y=0
    # ----------------
    def __init__(self, mass, x, y) -> None:
        self.mass = mass
        self.position_x = x
        self.position_y = y
        space_object.universe.append(self)
    def place_in_space(self):
        pg.draw.circle(screen, colors["red"], (self.position_x, self.position_y), self.mass)
    @classmethod
    def do_the_magic(cls) -> None: # change positions and velocities according to gravity :)
        for i in range (0,len(cls.universe)):
            for o in range (i+1,len(cls.universe)):
                object_1=cls.universe[i]
                object_2=cls.universe[o]
                if object_1 == object_2:
                    continue
                if object_1.position_x == object_2.position_x and object_1.position_y == object_2.position_y:
                    object_1.v_x /= 100
                    object_1.v_y /= 100
                    object_2.v_x /= 100
                    object_2.v_y /= 100
                    continue
                r=euclidean_distance((object_1.position_x,object_1.position_y),(object_2.position_x,object_2.position_y))
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
                object_1.position_x+=object_1.v_x*constants["time_scale"]
                object_1.position_y+=object_1.v_y*constants["time_scale"]
                object_2.position_x+=object_2.v_x*constants["time_scale"]
                object_2.position_y+=object_2.v_y*constants["time_scale"]
        for  celestial_body in cls.universe:
            celestial_body.place_in_space()
            
space_object(10,100,10)
space_object(10,300,100)
space_object(10,500,200)
# initialize game -----------------------------------------
pg.init()
# initialize the window -----------------------------------------

screen = pg.display.set_mode((800, 600))  # windows size
pg.display.set_caption("Space simulator")  # title text
icon = pg.image.load("assets/planet.png")  # load icon asset
pg.display.set_icon(icon)  # set the icon


# main loop -----------------------------------------
game_state = True
while game_state:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_state = False

    screen.fill((4, 12, 36))  # screen BG-color
    space_object.do_the_magic()
    pg.display.update()
