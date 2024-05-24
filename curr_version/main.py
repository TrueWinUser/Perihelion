import time
from math import sqrt
import pygame
import random
import json

import template_maker

pygame.init()


TA = 500
G = 6.7e-11 * TA
k = 50000000
SR = 696340000 / k
SM = 1.99 * 10**30

def cord(x, y, skale=1):
    return [(x/k)*skale + 500, (y/k)*skale+500]

def vcr_sum(v1: [], v2: []):
    ans = []
    for i in range(min(len(v1), len(v2))):
        ans.append(v1[i]+v2[i])
    return ans

class body:

    def __init__(self, mass: int, x: int, y: int, vel: [int, int], radius: int, color: int):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity = vel
        self.aclrt = [0, 0]
        self.force = [0, 0]
        self.radius = radius
        self.color = color

    
    def change_aclrt(self):
        self.aclrt = [self.force[0]/self.mass, self.force[1]/self.mass]

    def update_pos(self):
        self.velocity = [self.velocity[0] + self.aclrt[0], self.velocity[1] + self.aclrt[1]]
        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]
        self.force = [0, 0]
    
    def change_force(self, m1: int, r1: [int, int]):

        if(sqrt(r1[0]**2 + r1[1]**2) < 5*k):
            f1v = [0, 0]
        elif(r1[0] == 0):
            f1 = (G * self.mass * m1) / (r1[0]**2 + r1[1]**2)
            f1v = [0, [-f1, f1][r1[1] > 0]]   
        elif(r1[1] == 0):
            f1 = (G * self.mass * m1) / (r1[0]**2 + r1[1]**2)
            f1v = [[-f1, f1][r1[0] > 0], 0]
        else:
            f1 = (G * self.mass * m1) / (r1[0]**2 + r1[1]**2)
            sin1 = r1[1]/(sqrt(r1[0]**2 + r1[1]**2))
            cos1 = r1[0]/(sqrt(r1[0]**2 + r1[1]**2))
            f1v = [f1 * cos1, f1 * sin1]
        
        self.force = vcr_sum(f1v, self.force)
        self.change_aclrt()



def main():

    templates_list = open("templates\\templates_list.txt", "r")
    templates = []
    for name in templates_list:
        with open(f"templates\\{name[:-1]}") as f:
            template = json.load(f)
            templates.append(template)

    print("\n-----------TEMPLATES-----------\n")
    print("0: make new template")
    for i in range(len(templates)):
        name = templates[i]["temp_name"]
        print(f"{i+1}: {name}")
    print("\n-------------------------------\n")
    print("Ctrl+C to quit")
    curr_temp_idx = int(input("Select template: "))

    if(curr_temp_idx == 0):
        template_maker.make_new_template()
        return

    curr_temp = templates[curr_temp_idx-1]

    bodies = []
    for bd in curr_temp.keys():
        if(bd == "temp_name"): continue
        bodies.append(body(curr_temp[bd]["mass"]*SM,
                            curr_temp[bd]["x"]*k,
                            curr_temp[bd]["y"]*k,
                            curr_temp[bd]["vel"],
                            curr_temp[bd]["rad"]*SR,
                            curr_temp[bd]["color"]))


    screen = pygame.display.set_mode((1000, 1000))
    screen.fill((255, 255, 255))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


        collapsed = set()
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if(i == j): continue
                if(sqrt((bodies[j].x - bodies[i].x)**2 + (bodies[j].y - bodies[i].y)**2) < ((bodies[i].radius*k + bodies[j].radius*k)/3)*2):
                    collapsed.add((max(i, j), min(i, j)))
                    continue

                bodies[i].change_force(bodies[j].mass, [bodies[j].x - bodies[i].x, bodies[j].y - bodies[i].y])

        for (i, j) in collapsed:
            p1 = [bodies[i].mass*bodies[i].velocity[0], bodies[i].mass*bodies[i].velocity[1]]
            p2 = [bodies[j].mass*bodies[j].velocity[0], bodies[j].mass*bodies[j].velocity[1]]
            sp = vcr_sum(p1, p2)
            v = [sp[0]/(bodies[i].mass + bodies[j].mass), sp[1]/(bodies[i].mass + bodies[j].mass)]

            bodies.append(body(bodies[i].mass + bodies[j].mass,
                            (bodies[i].x*bodies[i].mass + bodies[j].x*bodies[j].mass)/(bodies[i].mass + bodies[j].mass), 
                            (bodies[i].y*bodies[i].mass + bodies[j].y*bodies[j].mass)/(bodies[i].mass + bodies[j].mass), 
                            v, 
                            sqrt(bodies[j].radius**2 + bodies[i].radius**2), 
                            (250, 221, 77)))      
            bodies.pop(i)
            bodies.pop(j)

        screen.fill((0, 0, 0))

        for i in bodies:
            i.update_pos()
            pygame.draw.circle(screen, i.color, cord(i.x, i.y), i.radius)

        pygame.display.flip()



while(True):
    main()
