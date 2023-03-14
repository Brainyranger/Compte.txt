import time
import math
from threading import Thread
from projet_robot.Simulation.Robot import Robot
from projet_robot.Controller.Toolbox_IA import Constante,Decorator

global WHEEL_DIAMETER 
global WHEEL_BASE_WIDTH   
WHEEL_DIAMETER = 5
WHEEL_BASE_WIDTH= 60

class IA(Thread):

    def __init__(self,ia_command):
        """ constructeur de notre classe IA
            initialisation de notre liste de commandes
            initialisation de l'état de notre commande courante"""


        super(IA,self).__init__()
        self.status = True
        self.ia_command = ia_command
        self.curr_command = -1
        
    def update(self,dt):
        """ Parcoure notre liste de commandes et éxécute commande par commande """

        if len(self.ia_command) == 0:
            self.status = False
            
        if self.stop():
            self.status = False
            return
            
        if self.curr_command < 0 or self.ia_command[self.curr_command].stop():
            self.curr_command += 1
            self.ia_command[self.curr_command].start()
        
        self.ia_command[self.curr_command].update(dt)       

    def ajout_commandes(self,command):
        """ Ajout d'une commande à la liste de commandes """

        self.ia_command.append(command)
        
    def stop(self):
        """ Arret de l'IA """
        return self.curr_command == len(self.ia_command)-1 and self.ia_command[self.curr_command].stop()
        
        
    def getStatus(self):
        """ Renvoie l'état de l'IA """

        return self.status

    def	select_commandes(self,indice):
        """ selectionne par indice notre commande """

        if indice < 0 or indice > len(self.ia_command):
    	    return
        return self.ia_command[indice]



class Avancer:

    def __init__(self,vitesse,distance,robot):
        """ constructeur de notre classe Avancer
        initialisation de la vitesse de nos roues 
        initialisation de la distance à parcourir
        initialisation de notre robot pour lequel on applique la comande"""

        self.robot = Decorator(robot)
        self.vitesse = vitesse*3800
        self.distance = distance
        self.distance_parcouru = 0
        self.status = False

    def update(self,dt) :
        """ Fais la mise à jour de notre déplacement en ligne droite """
	
        
        if self.stop():
        	self.robot.set_motor_dps(0,0)
        	self.status = False
        	return
        	
        self.distance_parcouru += Avancer_deux.get_distance_parcourue(self,dt)
        Avancer_decorator.avancer(self,dt)
         	
        	
    def getStatus(self):
        """ Renvoie l'état de la commande """

        return self.status

    def start(self):
        """ Lance la commande """
        self.distance_parcouru = 0
        self.status = True

    def stop(self):
        """ Arret de la commande en cours"""
        return self.distance_parcouru >= self.distance


class Tourner:

    def __init__(self,angle,dps,robot):
        """ Constructeur de notre classe Tourner 
        initialisation de la vitesse de nos roues
        initialisation de l'angle qu'on doit parcourir 
        initialisation de la distance à parcourir en degré/s pour parcourir l'angle
        initialisation de notre robot pour lequel on applique la comande"""

        self.robot = Decorator(robot)
        self.angle = angle
        self.dps = dps
        self.angle_parcouru = 0
        self.status = True

    def update(self,dt):
        """ Fais la mise à jour de notre commande """

        if self.stop():
        	self.robot.set_motor_dps(0,0)
        	self.status = False
        	print("j'ai fini de parcourir "+str(self.angle_parcouru)+" degré")
        	return
      
        self.angle_parcouru += self.dps*dt
        Decorator.tourner(self,self.dps,dt)
	
    def getStatus(self):
        """ Renvoie l'état de la commande """

        return self.status

    def start(self):
        """ Lance la commande """
        self.angle_parcouru = 0
        self.status = True

    def stop(self):
        """ Arrête la commande en cours """

        return self.angle_parcouru > self.angle
        

